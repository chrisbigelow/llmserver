from prisma import Prisma
from contextlib import asynccontextmanager
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
import json
import ipaddress
from starlette.responses import RedirectResponse
import os
import httpx
from enum import Enum
from datetime import datetime  # Import the datetime module

prisma = Prisma()
github_client_id = os.getenv('GITHUB_CLIENT_ID')
github_client_secret = os.getenv('GITHUB_CLIENT_SECRET')
GITHUB_IPS_ONLY = os.getenv("GITHUB_IPS_ONLY", "True").lower() in ["true", "1"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup prisma
    print('connecting to db')
    await prisma.connect()
    print('connected to db')
    yield
    # disconnect prisma
    await prisma.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"version": "1.0.0"}

async def gate_by_github_ip(request: Request):
    # Allow GitHub IPs only
    if GITHUB_IPS_ONLY:
        try:
            src_ip = ipaddress.ip_address(request.client.host)
        except ValueError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Could not hook sender ip address"
            )
        async with httpx.AsyncClient() as client:
            allowlist = await client.get("https://api.github.com/meta")
        for valid_ip in allowlist.json()["hooks"]:
            if src_ip in ipaddress.ip_network(valid_ip):
                return
        else:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "Not a GitHub hooks ip address"
            )

@app.post("/webhook", dependencies=[Depends(gate_by_github_ip)])
async def receive_payload(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(...),
):
    if x_github_event == "push":
        payload = await request.json()
        default_branch = payload["repository"]["default_branch"]
        # check if event is referencing the default branch
        if "ref" in payload and payload["ref"] == f"refs/heads/{default_branch}":
            return {"message": "Ignoring push event on default branch"}
    elif x_github_event == "ping":
        return {"message": "pong"}
        # comment
    else:
        return {"message": "Unable to process action"}

@app.get("/github-login")
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302);

@app.get("/github-code")
async def github_code(code: str):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
        response_json = response.json()
        access_token = response_json['access_token']
        async with httpx.AsyncClient() as client:
           headers.update({'Authorization': f'Bearer {access_token}'})
           response = await client.get(url='https://api.github.com/user', headers=headers)
        return response.json()

def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  # Convert datetime objects to a string representation
    raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')

@app.get("/items/")
async def read_item():
    found = await prisma.requirement.find_unique(where={'id': 191})
    if found:
        # Convert the model to a dictionary and then serialize it to JSON with custom formatting
        found_dict = found.dict()
        found_json = json.dumps(found_dict, indent=2, sort_keys=True, default=default_converter)
        print(f'found post: {found_json}')
    else:
        print('Post not found')
