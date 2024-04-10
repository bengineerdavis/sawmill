import typer

app = typer.Typer()


@app.command()
def hello():
    typer.echo("Hello from sawmill!")


if __name__ == "__main__":
    hello()
