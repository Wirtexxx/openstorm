import typer
from openstorm.settings import settings
from openstorm.handler import mongodb

app = typer.Typer(help="Manage MongoDB")

# -------------------
# START
# -------------------


@app.command()
def start(
    image: str = typer.Option("mongo:latest", help="Docker image"),
    name: str = typer.Option(settings.DEFAULT_CONTAINER_NAME, "--container", "-c", help="Container name"),
    bind_dir: str = typer.Option(settings.DEFAULT_BIND_HOST_DIR, "--bind-dir", "-b", help="Host bind directory"),
    port: int = typer.Option(27017, "--port", "-p", help="Port mapping"),
    use_named_volume: bool = typer.Option(False, "--named-volume", "-v", help="Use named Docker volume")
):
    """Start MongoDB container"""
    success = mongodb.start_container(
        image=image,
        name=name,
        bind_dir=bind_dir,
        port=port,
        use_named_volume=use_named_volume
    )
    if not success:
        raise typer.Exit(code=1)

# -------------------
# STOP
# -------------------


@app.command()
def stop(
    name: str = typer.Option(settings.DEFAULT_CONTAINER_NAME, "--container", "-c", help="Container name"),
    remove: bool = typer.Option(False, "--remove", "-r", help="Remove container after stop")
):
    """Stop MongoDB container"""
    success = mongodb.stop_container(name=name, remove=remove)
    if not success:
        raise typer.Exit(code=1)

# -------------------
# STATUS
# -------------------


@app.command()
def status(
    uri: str = typer.Option(settings.MONGO_URI, "--uri", help="URI for mongodb connection")
):
    """Check MongoDB container status"""
    success = mongodb.status_mongo(uri=uri)
    if not success:
        raise typer.Exit(code=1)


@app.command()
def shell(
    name: str = typer.Option(settings.DEFAULT_CONTAINER_NAME, "--container", "-c", help="Container name"),
    uri: str = typer.Option(settings.MONGO_URI, "--uri", help="URI for mongodb connection")
):
    """Open Shell for mongodb"""
    success = mongodb.open_shell(name=name, uri=uri)
    if not success:
        raise typer.Exit(code=1)
