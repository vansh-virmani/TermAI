import typer
from rich.console import Console
from app.environment import get_os,get_shell
from app.llm import generate_command
from app.safety import validate_command, SafetyLevel
from app.execution import execute_command


app = typer.Typer()
console = Console()
#typer is used for cli application just to pass directly pass args in python application and return in cli
#rich is used for good terminal ui/presentation

@app.command()
def ask(query: str):
    os_name=get_os()
    shell=get_shell()
    

    console.print(f"[bold cyan]You asked:[/bold cyan] {query}")
    console.print(f"[bold cyan]Operating System is:[/bold cyan] {os_name}")
    console.print(f"[bold cyan]Shell is:[/bold cyan] {shell}")
   

    result = generate_command(
        query=query,
        os_name=os_name,
        shell=shell,
    )

    safety_result = validate_command(result.command)

    console.print()
    console.print("[bold green]Generated Command:[/bold green]")
    console.print(result.command)

    console.print()
    console.print("[bold yellow]Explanation:[/bold yellow]")
    console.print(result.explanation)

    console.print()
    console.print("[bold cyan]Safety Check:[/bold cyan]")
    console.print(safety_result.level.value)
    console.print(safety_result.reason)

    if safety_result.level == SafetyLevel.BLOCKED:
        console.print()
        console.print("[bold red]Command blocked.[/bold red]")
        return
    
    confirmed = typer.confirm("Execute this command?")

    if not confirmed:
     console.print("[yellow]Execution cancelled.[/yellow]")
     return

    execution_result = execute_command(
    result.command,
    shell,
)

    console.print()
    console.print("[bold green]Execution Result:[/bold green]")

    if execution_result.stdout:
        console.print(execution_result.stdout)

    if execution_result.stderr:
        console.print("[bold red]Error:[/bold red]")
        console.print(execution_result.stderr)

    console.print(
        f"[bold cyan]Exit Code:[/bold cyan] "
        f"{execution_result.return_code}")


    
    

        


