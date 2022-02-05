import typer
from IPython import embed

typer_app = typer.Typer()


@typer_app.command()
def shell():
    embed()


@typer_app.command()
def runserver():
    # TODO: run the server
    print("hello from ugc app.")


if __name__ == "__main__":
    typer_app()
