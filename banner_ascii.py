import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

# Gera as duas linhas do banner em ASCII art
linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")

# Pinta em ciano (estilo Claude Code) e centraliza
console.print(Align.center(Text(linha1, style="bold #A855F7")))
console.print(Align.center(Text(linha2, style="bold #06B6D4")))
console.print(Align.center(
    Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
    style="italic #8484A0")
))

# Rodar o banner padrão
#$ python banner_ascii.py

# Listar as 570+ fontes disponíveis no PyFiglet
#$ python banner_ascii.py --fonts

# Testar uma fonte específica
#$ python banner_ascii.py --font slant --text "Mission Control AI"

# Demonstrar 8 fontes diferentes lado a lado
#$ python banner_ascii.py --demo

