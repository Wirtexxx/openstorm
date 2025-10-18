from rich.console import Console
from rich.markup import escape
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from openstorm.settings import settings
from openstorm.lib import run_cmd
import pathlib

console = Console()


def start_container(
    image: str,
    name: str,
    bind_dir: str,
    port: int = 27017,
    use_named_volume: bool = False
) -> bool:
    console.print(f"[bold cyan]Starting MongoDB container '{name}'...[/bold cyan]")

    def container_exists(running_only: bool = True) -> bool:
        cmd = ["docker", "ps"] + (["-a"] if not running_only else [])
        cmd += ["--filter", f"name=^{name}$", "--format", "{{.Names}}"]
        cp = run_cmd(cmd, capture_output=True)
        return cp and cp.stdout and name in cp.stdout.splitlines()

    if container_exists(running_only=True):
        console.print(f"[yellow][INFO][/yellow] Container '{name}' is already running")
        return True

    if container_exists(running_only=False):
        console.print(f"Container '{name}' exists. Starting it...")
        result = run_cmd(["docker", "start", name])
        if result and result.returncode == 0:
            console.print(f"[green][SUCCESS][/green] Container '{name}' started")
            return True
        console.print(f"[red][ERROR][/red] Failed to start container")
        return False

    if not use_named_volume:
        try:
            pathlib.Path(bind_dir).mkdir(parents=True, exist_ok=True)
        except OSError as e:
            console.print(f"[red][ERROR][/red] Failed to create directory: {e}")
            return False

    volume_arg = f"{name}_data:/data/db" if use_named_volume else f"{bind_dir}:/data/db"
    cmd = ["docker", "run", "-d", "--name", name, "-p", f"{port}:27017", "-v", volume_arg, image]

    result = run_cmd(cmd, capture_output=True)
    if result and result.returncode == 0:
        console.print(f"[green][SUCCESS][/green] Container started: {escape(result.stdout.strip())}")
        return True

    console.print(f"[red][ERROR][/red] Failed to start container")
    if result and result.stderr:
        console.print(f"Error: {escape(result.stderr)}")
    return False


def stop_container(name: str, remove: bool) -> bool:
    console.print(f"[bold cyan]Stopping container '{name}'...[/bold cyan]")
    result = run_cmd(["docker", "stop", name])
    if not result or result.returncode != 0:
        console.print(f"[red][ERROR][/red] Failed to stop container")
        return False

    console.print(f"[green][SUCCESS][/green] Container stopped")
    if remove:
        result = run_cmd(["docker", "rm", name])
        if result and result.returncode == 0:
            console.print(f"[green][SUCCESS][/green] Container removed")
            return True
        console.print(f"[red][ERROR][/red] Failed to remove container")
        return False
    return True


def status_mongo(uri: Optional[str] = None) -> bool:
    uri = uri or settings.MONGO_URI
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.admin.command("ping")
        console.print(f"[green][SUCCESS][/green] MongoDB is running at {uri}")
        client.close()
        return True
    except PyMongoError as e:
        console.print(f"[red][ERROR][/red] MongoDB is not reachable: {e}")
        return False


def open_shell(name: str, uri: Optional[str]) -> bool:
    console.print(f"[bold cyan]Opening MongoDB shell...[/bold cyan]")
    for shell_cmd in ["mongosh", "mongo"]:
        result = run_cmd(["docker", "exec", "-it", name, shell_cmd], capture_output=False)
        if result and result.returncode == 0:
            return True

    uri = uri or settings.MONGO_URI
    result = run_cmd(["mongosh", uri], capture_output=False)
    return result.returncode == 0 if result else False
