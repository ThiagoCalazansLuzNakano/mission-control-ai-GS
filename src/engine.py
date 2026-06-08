"""
engine.py
Motor de análise: monta o contexto e chama a Ollama Cloud API.
"""

import os
import json
from pathlib import Path
from openai import OpenAI
from src.telemetria import TelemetriaAgroSat
from src.alertas import Alerta
from typing import List

# ── Carrega system prompt ────────────────────────────────────────────────────

_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "system_prompt.md"
SYSTEM_PROMPT = _PROMPT_PATH.read_text(encoding="utf-8")

# ── Cliente Ollama Cloud (compatível com OpenAI SDK) ─────────────────────────

def _get_client() -> OpenAI:
    api_key = os.getenv("OLLAMA_API_KEY", "")
    return OpenAI(
        base_url="https://api.ollama.ai/v1",
        api_key=api_key,
    )


MODEL = "gpt-oss:120b"


# ── Funções principais ────────────────────────────────────────────────────────

def _montar_contexto_telemetria(t: TelemetriaAgroSat, alertas: List[Alerta]) -> str:
    """Monta o bloco de contexto que será enviado à IA."""
    alertas_txt = ""
    if alertas:
        for a in alertas:
            alertas_txt += (
                f"\n  [{a.nivel}] {a.parametro}: {a.mensagem}"
                f"\n  → Impacto terrestre: {a.impacto_terrestre}\n"
            )
    else:
        alertas_txt = "\n  Todos os parâmetros dentro da faixa normal.\n"

    return f"""
=== TELEMETRIA AGROSAT-1 ===
Timestamp         : {t.timestamp}
NDVI Sensor Health: {t.ndvi_sensor_health:.1f}%
Payload Temp      : {t.payload_temp_c:.1f}°C
Storage Usado     : {t.storage_used_pct:.1f}%
Janela Downlink   : {t.downlink_window_min:.1f} min
Estab. Atitude    : {t.attitude_stability:.1f}%

=== ALERTAS DETECTADOS ===
{alertas_txt}
"""


def analisar_telemetria(t: TelemetriaAgroSat, alertas: List[Alerta]) -> str:
    """
    Envia os dados de telemetria + alertas para a IA e retorna a análise.
    """
    contexto = _montar_contexto_telemetria(t, alertas)

    user_message = (
        f"{contexto}\n"
        "Analise o estado atual da missão AgroSat-1. "
        "Explique o que está acontecendo, o nível de risco, "
        "o impacto para os usuários terrestres e recomende ações imediatas."
    )

    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.4,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()


def responder_pergunta(
    pergunta: str,
    t: TelemetriaAgroSat,
    alertas: List[Alerta],
    historico: list,
) -> str:
    """
    Modo chat: responde uma pergunta livre do operador, com contexto de telemetria.
    historico: lista de dicts {"role": ..., "content": ...}
    """
    contexto = _montar_contexto_telemetria(t, alertas)

    # Injeta contexto como primeira mensagem do usuário se histórico estiver vazio
    mensagens = [{"role": "system", "content": SYSTEM_PROMPT}]

    if not historico:
        mensagens.append({
            "role": "user",
            "content": f"Contexto atual da missão:\n{contexto}",
        })
        mensagens.append({
            "role": "assistant",
            "content": "Contexto recebido. Pode fazer suas perguntas sobre a missão.",
        })

    mensagens.extend(historico)
    mensagens.append({"role": "user", "content": pergunta})

    client = _get_client()
    response = client.chat.completions.create(
        model=MODEL,
        messages=mensagens,
        temperature=0.5,
        max_tokens=600,
    )
    return response.choices[0].message.content.strip()
