import typer

from openstorm.cli import mongodb
app = typer.Typer()



@app.command()
def config():
    print("config")


app.add_typer(mongodb.app, name="mongodb")



if __name__ == "__main__":
    app()
