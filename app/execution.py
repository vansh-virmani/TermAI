from app.models import ExecutionResult
import subprocess



def execute_command(command: str, shell: str) -> ExecutionResult:

    if shell == "PowerShell":
        args = [
            "powershell.exe",
            "-NoProfile",
            "-Command",
            command,
        ]

    elif shell == "CMD":
        args = [
            "cmd.exe",
            "/c",
            command,
        ]

    else:
        raise ValueError(f"Unsupported shell: {shell}")

    try:
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,
        )

        return ExecutionResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
        )

    except subprocess.TimeoutExpired:
        return ExecutionResult(
            stdout="",
            stderr="Command timed out after 30 seconds.",
            return_code=-1,
        )
    

