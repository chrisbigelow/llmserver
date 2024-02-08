import typer
import os
import json
from pathlib import Path

CONFIG_DIR = os.path.join(Path.home(), '.myapp')  # Replace '.myapp' with your app's name
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.json')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}
    
def save_config(config):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)