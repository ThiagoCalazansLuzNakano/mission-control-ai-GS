"""
main.py
Ponto de entrada do AgroSat Mission Control AI.
Execute: python main.py
"""

import sys
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

from banner_ascii import print_banner, console
from src.telemetria import gerar_telemetria
from src.alertas import avaliar_telemetria, nivel_geral
from src.engine import analisar_telemetria
from src import ui


def executar_ciclo(cenario: str):
    """Executa um ciclo completo: gera telemetria → avalia alertas → IA → chat."""

    # 1. Gerar dados de telemetria
    t = gerar_telemetria(cenario)
    alertas = avaliar_telemetria(t)
    ng = nivel_geral(alertas)

    # 2. Exibir telemetria
    ui.imprimir_separador("📡 DADOS DE TELEMETRIA", cor=ui.cor_nivel(ng))
    ui.imprimir_telemetria(t, ng)

    # 3. Exibir alertas
    ui.imprimir_separador("🔔 ALERTAS DO SISTEMA")
    ui.imprimir_alertas(alertas)

    # 4. Análise da IA
    ui.imprimir_separador("🤖 ANÁLISE DA IA", cor="cyan")
    with ui.spinner_ia("AgroSat Mission AI analisando a missão..."):
        analise = analisar_telemetria(t, alertas)
    ui.imprimir_analise_ia(analise)

    # 5. Modo chat
    ui.imprimir_separador("💬 CHAT COM A IA")
    ui.loop_chat(t, alertas)


def main():
    print_banner()

    while True:
        cenario = ui.menu_cenario()

        if cenario == "sair":
            console.print("\n[bold green]👋 Encerrando Mission Control AI. Boa missão capitão![/bold green]\n")
            sys.exit(0)

        executar_ciclo(cenario)
        console.print()


if __name__ == "__main__":
    main()
