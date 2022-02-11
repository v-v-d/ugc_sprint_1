import typer
import uvicorn
from IPython import embed

from app.settings import settings

typer_app = typer.Typer()


@typer_app.command()
def shell():
    embed()


@typer_app.command()
def runserver():
    uvicorn.run(**settings.UVICORN.dict())


if __name__ == "__main__":
    typer_app()
