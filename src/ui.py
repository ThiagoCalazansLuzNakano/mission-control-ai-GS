"""
ui.py
Interface CLI estilo Claude Code usando Rich.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.live import Live
from rich import box
import time

from src.alertas import Alerta, cor_nivel, emoji_nivel, NIVEL_OK
from src.telemetria import TelemetriaAgroSat, formatar_telemetria
from typing import List

console = Console()


# ── Helpers visuais ──────────────────────────────────────────────────────────

def imprimir_separador(titulo: str = "", cor: str = "green"):
    if titulo:
        console.rule(f"[bold {cor}]{titulo}[/bold {cor}]", style=cor)
    else:
        console.rule(style=cor)
    console.print()


def imprimir_telemetria(t: TelemetriaAgroSat, nivel_geral: str):
    cor = cor_nivel(nivel_geral)
    emoji = emoji_nivel(nivel_geral)

    painel = Panel(
        formatar_telemetria(t),
        title=f"[bold {cor}]{emoji} TELEMETRIA AgroSat-1 — {nivel_geral}[/bold {cor}]",
        border_style=cor,
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(painel)
    console.print()


def imprimir_alertas(alertas: List[Alerta]):
    if not alertas:
        console.print(Panel(
            "[bold green]✅ Todos os parâmetros dentro da faixa operacional normal.[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        ))
        console.print()
        return

    for a in alertas:
        cor = cor_nivel(a.nivel)
        emoji = emoji_nivel(a.nivel)
        conteudo = (
            f"[bold]Parâmetro:[/bold] {a.parametro}\n"
            f"[bold]Valor Atual:[/bold] {a.valor_atual}\n"
            f"[bold]Diagnóstico:[/bold] {a.mensagem}\n\n"
            f"[bold yellow]🌾 Impacto Terrestre:[/bold yellow]\n{a.impacto_terrestre}"
        )
        console.print(Panel(
            conteudo,
            title=f"[bold {cor}]{emoji} {a.nivel} — {a.parametro}[/bold {cor}]",
            border_style=cor,
            box=box.ROUNDED,
            padding=(1, 2),
        ))
        console.print()


def imprimir_analise_ia(texto: str):
    painel = Panel(
        Markdown(texto),
        title="[bold cyan]🤖 Análise da IA — AgroSat Mission AI[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    )
    console.print(painel)
    console.print()


def imprimir_resposta_ia(texto: str):
    console.print()
    console.print(Panel(
        Markdown(texto),
        title="[bold cyan]🤖 AgroSat Mission AI[/bold cyan]",
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2),
    ))
    console.print()


def spinner_ia(mensagem: str = "Consultando IA..."):
    """Context manager que exibe um spinner enquanto a IA processa."""
    return Live(
        Spinner("dots", text=f"[cyan]{mensagem}[/cyan]"),
        console=console,
        refresh_per_second=10,
        transient=True,
    )


def menu_cenario() -> str:
    console.print("[bold]Escolha o cenário de telemetria:[/bold]")
    console.print("  [green]1[/green] — Normal")
    console.print("  [yellow]2[/yellow] — Alerta")
    console.print("  [red]3[/red] — Crítico")
    console.print("  [blue]4[/blue] — Aleatório")
    console.print("  [dim]5[/dim] — Sair")
    console.print()

    escolha = Prompt.ask(
        "[bold green]>[/bold green] Selecione",
        choices=["1", "2", "3", "4", "5"],
        default="4",
    )
    mapa = {"1": "normal", "2": "alerta", "3": "critico", "4": "aleatorio", "5": "sair"}
    return mapa[escolha]


def loop_chat(t: TelemetriaAgroSat, alertas: List[Alerta]):
    """
    Modo chat interativo estilo Claude Code.
    O usuário digita perguntas e a IA responde com contexto de telemetria.
    """
    from src.engine import responder_pergunta

    historico = []

    console.print(Panel(
        "[dim]Modo chat ativo. Digite sua pergunta ou [bold]sair[/bold] para voltar ao menu.[/dim]",
        border_style="cyan",
        box=box.SIMPLE,
    ))
    console.print()

    while True:
        try:
            pergunta = Prompt.ask("[bold cyan]Você[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            break

        if pergunta.strip().lower() in ("sair", "exit", "quit", "q"):
            break

        if not pergunta.strip():
            continue

        with spinner_ia("AgroSat Mission AI está analisando..."):
            resposta = responder_pergunta(pergunta, t, alertas, historico)

        imprimir_resposta_ia(resposta)

        historico.append({"role": "user",      "content": pergunta})
        historico.append({"role": "assistant", "content": resposta})

    console.print()
