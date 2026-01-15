from agent import get_agent
from rich.console import Console

console = Console()

def main():
    agent = get_agent()
    
    console.print("[bold green]Welcome to the Recommendations Agent MVP![/bold green]")
    console.print("Ask for recommendations (e.g., 'Recommend a thriller TV series artist') or ask 'why?'.")
    console.print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ['exit', 'quit']:
                break

            # Check if the user is asking "why" to prevent redundant searches
            original_tools = None
            if "why" in user_input.lower() or "reason" in user_input.lower():
                original_tools = agent.tools
                agent.tools = []
            
            console.print("\n[bold yellow]Agent is thinking...[/bold yellow]")
            agent.print_response(user_input, stream=True)
            
            # Restore tools
            if original_tools is not None:
                agent.tools = original_tools
            print("\n" + "-"*50 + "\n")
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Exiting...[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
