from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box

console = Console()

BANNER = r"""
    ___   ___  ____  ____  ____    __   ____  
   / _ | / _ \/ __ \/ __ \/ __/  / /  / __/  
  / __ |/ , _/ /_/ / /_/ /\ \   / /___\ \    
 /_/ |_/_/|_|\____/\____/___/  /____/___/    
  __  __ ___________ _____  __  __           
 /  |/  /  _/ __/ __/  _/ \  \/ /           
/ /|_/ // /_\ \_\ \ _/ /   \   /            
/_/  /_/___/___/___/___/   /_/             
   ___  ____  _  ________________  __ 
  / _ |/ __ \/ |/ /_  __/ __/ __ \/ / 
 / __ / /_/ /    / / / / _// /_/ / /__
/_/ |_\____/_/|_/ /_/ /___/\____/____/
"""

def print_banner():
    console.print(f"[bold green]{BANNER}[/bold green]")
    console.print(
        Panel.fit(
            "[bold white]🛰️  AgroSat Mission Control AI[/bold white]\n"
            "[dim]Monitoramento Inteligente de Satélite de Sensoriamento Agrícola[/dim]\n"
            "[dim]Global Solution 2026.1 — FIAP[/dim]",
            border_style="green",
            box=box.DOUBLE,
        )
    )
    console.print()
