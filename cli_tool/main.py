import typer
from dotenv import load_dotenv
from commands.translate import translate
from commands.hello import hello
from utils.config import load_config
from commands.configure_product_key import configure
from commands.configure_product_key import get_key_or_configure
from commands.testgen import testgen

app = typer.Typer()

app.command()(translate)
app.command()(hello)
app.command()(configure)
app.command()(testgen)

@app.callback()
def main():
    """
    This function runs before any other commands.
    """
    print("Welcome to the PrecisionQA CLI tool, let's get building!")
    get_key_or_configure()

if __name__ == "__main__":
    load_dotenv()
    app()