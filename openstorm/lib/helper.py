import sys
import subprocess
from typing import List, Optional


def clear_terminal():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def run_cmd(cmd: List[str], capture_output: bool = False, check: bool = False) -> Optional[subprocess.CompletedProcess]:
    """
    Run a shell command.

    Args:
        cmd: List of command arguments, e.g. ["docker", "ps"]
        capture_output: If True, capture stdout/stderr
        check: If True, raise CalledProcessError on non-zero exit

    Returns:
        subprocess.CompletedProcess or None on error
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"\033[91m[ERROR]\033[0m Command failed ({' '.join(cmd)}): {e}")
        if e.stdout:
            print("Output:", e.stdout)
        if e.stderr:
            print("Error output:", e.stderr)
        return None
    except FileNotFoundError:
        print(f"\033[91m[ERROR]\033[0m Command not found: {cmd[0]}")
        return None
    except Exception as e:
        print(f"\033[91m[ERROR]\033[0m Unexpected error running command {cmd}: {e}")
        return None
