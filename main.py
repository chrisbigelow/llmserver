from prisma import Prisma
from contextlib import asynccontextmanager
from fastapi import FastAPI
import json
from datetime import datetime  # Import the datetime module

prisma = Prisma()

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
