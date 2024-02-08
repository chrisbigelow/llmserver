import typer
import os
import json
from pathlib import Path
from typing import Optional
from utils.config import load_config
from utils.config import save_config

def configure(product_key: Optional[str] = typer.Option(None, prompt=True)):
    """
    Configure the product key.
    """
    config = load_config()
    config['product_key'] = product_key
    save_config(config)
    typer.echo("Product key saved successfully!")

def get_key_or_configure():
    config = load_config()
    if 'product_key' in config:
        typer.echo("Using previously stored product key: " + config['product_key'])
    else:
        typer.echo("Product key not found. Please configure your product key.")
        configure()  # Directly calling the configure function
