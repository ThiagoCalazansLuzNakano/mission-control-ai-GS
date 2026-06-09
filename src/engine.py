"""Motor de análise da Mission Control AI."""
import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src.telemetria import gerar_telemetria, formatar_telemetria
from src.alertas import avaliar_telemetria, nivel_geral, NIVEL_CRITICO

load_dotenv()

# Identificação da trilha
TRILHA = "agrosat"  # "envirosat" | "connectsat" | "mobilitysat"

client = Client(
    host="https: /ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)

def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b", messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"

def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente de monitoramento de satélite agrícola."  # fallback genérico

class MissionEngine:
        """Motor de análise."""

        def __init__(self):
            self.trilha = TRILHA
            self.system_prompt = load_system_prompt()
            # Coleta a primeira leitura de telemetria ao inicializar
            self._telemetria = gerar_telemetria("aleatorio")
            self._alertas = avaliar_telemetria(self._telemetria)
            self._nivel = nivel_geral(self._alertas)

        def is_ready(self):
            return True

        def _respostas_automatizadas(self) -> str:
            """
            Respostas automáticas para situações críticas — lógica em Python puro.
            Requisito: pelo menos uma resposta automatizada para situação crítica.
            """
            t = self._telemetria
            acoes = []

            # Temperatura crítica → modo seguro térmico
            if t.payload_temp_c > 55:
                acoes.append(
                    "🔴 AÇÃO AUTOMÁTICA: Modo Seguro Térmico ativado — "
                    "payload óptico em standby para resfriamento."
                )

            # Storage crítico → compressão de emergência
            if t.storage_used_pct > 90:
                acoes.append(
                    "🔴 AÇÃO AUTOMÁTICA: Compressão de emergência ativada — "
                    "novas imagens em resolução reduzida até próximo downlink."
                )

            # Downlink crítico → priorização de transmissão
            if t.downlink_window_min < 3:
                acoes.append(
                    "🔴 AÇÃO AUTOMÁTICA: Modo prioridade de downlink — "
                    "apenas imagens críticas de áreas de alerta serão transmitidas."
                )

            # NDVI crítico → suspensão de capturas
            if t.ndvi_sensor_health < 60:
                acoes.append(
                    "🔴 AÇÃO AUTOMÁTICA: Capturas NDVI suspensas — "
                    "sensor em diagnóstico, aguardando recalibração."
                )

            # Atitude crítica → protocolo de estabilização
            if t.attitude_stability < 80:
                acoes.append(
                    "🔴 AÇÃO AUTOMÁTICA: Protocolo de estabilização iniciado — "
                    "rodas de reação ativadas, capturas pausadas."
                )

            return "\n".join(acoes)

        def status_snapshot(self) -> str:
            """Retorna texto resumindo o estado atual da telemetria."""
            from src.alertas import emoji_nivel
            # 1. Coleta dados de telemetria
            t = self._telemetria
            alertas = self._alertas
            nivel = self._nivel
            # 2. Formata o resumo
            linhas = [
                f"{emoji_nivel(nivel)} NÍVEL GERAL DA MISSÃO: {nivel}",
                "",
                formatar_telemetria(t),
                "",
            ]
            # 3. Lista alertas ativos
            if alertas:
                linhas.append("⚠️  ALERTAS ATIVOS:")
                for a in alertas:
                    linhas.append(f"  [{a.nivel}] {a.parametro}: {a.mensagem}")
            else:
                linhas.append("✅ Nenhum alerta ativo — todos os parâmetros normais.")
            # 4. Exibe ações automáticas se houver
            acoes = self._respostas_automatizadas()
            if acoes:
                linhas.append("")
                linhas.append(acoes)

            return "\n".join(linhas)

        def analyze(self, pergunta_usuario: str) -> str:
                """Analisa a pergunta com base na telemetria + alertas + IA."""

            # 1. Coletar dados via src.telemetria
            t = self._telemetria
                alertas = self._alertas

            # 2. Avaliar alertas e montar bloco de texto
            if alertas:
                    alertas_txt = ""
                    for a in alertas:
                        alertas_txt += (
                            f"\n  [{a.nivel}] {a.parametro}: {a.mensagem}"
                            f"\n  Impacto terrestre: {a.impacto_terrestre}\n"
                        )
                else:
                    alertas_txt = "\n  Todos os parâmetros dentro da faixa normal.\n"

                # Inclui ações automáticas já executadas no contexto
                acoes = self._respostas_automatizadas()
                bloco_acoes = f"\nAções automáticas já executadas:\n{acoes}\n" if acoes else ""

                # 3. Montar prompt com dados + alertas + pergunta do operador
                prompt = f"""
        === TELEMETRIA AGROSAT-1 ===
        Timestamp         : {t.timestamp}
        NDVI Sensor Health: {t.ndvi_sensor_health:.1f}%
        Payload Temp      : {t.payload_temp_c:.1f}°C
        Storage Usado     : {t.storage_used_pct:.1f}%
        Janela Downlink   : {t.downlink_window_min:.1f} min
        Estab. Atitude    : {t.attitude_stability:.1f}%

        === ALERTAS DETECTADOS ==={alertas_txt}{bloco_acoes}
        === PERGUNTA DO OPERADOR ===
        {pergunta_usuario}
        """

        # 4. Chamar llm com o system prompt customizado
        # 5. Retornar a resposta
    return llm(prompt, system=self.system_prompt)