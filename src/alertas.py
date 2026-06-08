"""
alertas.py
Thresholds e regras de decisão para o AgroSat.
Toda a lógica condicional é feita em Python — a IA só interpreta.
"""

from dataclasses import dataclass
from typing import List
from src.telemetria import TelemetriaAgroSat


# ── Níveis de severidade ────────────────────────────────────────────────────

NIVEL_OK       = "OK"
NIVEL_ALERTA   = "ALERTA"
NIVEL_CRITICO  = "CRÍTICO"


# ── Thresholds ───────────────────────────────────────────────────────────────

THRESHOLDS = {
    "ndvi_sensor_health": {
        "alerta":  85.0,   # abaixo → ALERTA
        "critico": 60.0,   # abaixo → CRÍTICO
    },
    "payload_temp_c": {
        "alerta":  40.0,   # acima → ALERTA
        "critico": 55.0,   # acima → CRÍTICO
        "alerta_low":  -10.0,  # abaixo → ALERTA
        "critico_low": -20.0,  # abaixo → CRÍTICO
    },
    "storage_used_pct": {
        "alerta":  80.0,
        "critico": 90.0,
    },
    "downlink_window_min": {
        "alerta":  8.0,    # abaixo → ALERTA
        "critico": 3.0,    # abaixo → CRÍTICO
    },
    "attitude_stability": {
        "alerta":  92.0,   # abaixo → ALERTA
        "critico": 80.0,   # abaixo → CRÍTICO
    },
}


@dataclass
class Alerta:
    parametro: str
    nivel: str
    valor_atual: float
    mensagem: str
    impacto_terrestre: str


def _nivel_range(valor, th_alerta, th_critico, maior_e_pior=True) -> str:
    """
    maior_e_pior=True  → valores ALTOS são ruins (temp, storage)
    maior_e_pior=False → valores BAIXOS são ruins (ndvi, downlink, atitude)
    """
    if maior_e_pior:
        if valor >= th_critico:
            return NIVEL_CRITICO
        if valor >= th_alerta:
            return NIVEL_ALERTA
    else:
        if valor <= th_critico:
            return NIVEL_CRITICO
        if valor <= th_alerta:
            return NIVEL_ALERTA
    return NIVEL_OK


def avaliar_telemetria(t: TelemetriaAgroSat) -> List[Alerta]:
    """
    Aplica as regras de threshold e retorna lista de alertas.
    """
    alertas: List[Alerta] = []

    # ── NDVI Sensor Health ──
    th = THRESHOLDS["ndvi_sensor_health"]
    nivel = _nivel_range(t.ndvi_sensor_health, th["alerta"], th["critico"], maior_e_pior=False)
    if nivel != NIVEL_OK:
        alertas.append(Alerta(
            parametro="NDVI Sensor Health",
            nivel=nivel,
            valor_atual=t.ndvi_sensor_health,
            mensagem=f"Sensor multiespectral degradado: {t.ndvi_sensor_health:.1f}% (mín. recomendado: 85%)",
            impacto_terrestre=(
                "Imagens NDVI com qualidade insuficiente para análise de safras. "
                "Produtores rurais e analistas de seguro agrícola podem receber "
                "índices de vegetação imprecisos, comprometendo decisões de irrigação e cobertura."
            ),
        ))

    # ── Payload Temp ──
    th = THRESHOLDS["payload_temp_c"]
    if t.payload_temp_c >= th["critico"]:
        nivel = NIVEL_CRITICO
    elif t.payload_temp_c >= th["alerta"]:
        nivel = NIVEL_ALERTA
    elif t.payload_temp_c <= th["critico_low"]:
        nivel = NIVEL_CRITICO
    elif t.payload_temp_c <= th["alerta_low"]:
        nivel = NIVEL_ALERTA
    else:
        nivel = NIVEL_OK

    if nivel != NIVEL_OK:
        alertas.append(Alerta(
            parametro="Temperatura do Payload",
            nivel=nivel,
            valor_atual=t.payload_temp_c,
            mensagem=f"Temperatura fora da faixa operacional: {t.payload_temp_c:.1f}°C (faixa: -10°C a 40°C)",
            impacto_terrestre=(
                "Risco de dano permanente ao sensor óptico. Em caso de falha, "
                "a janela de revisita sobre áreas agrícolas monitoradas pode ser "
                "interrompida por dias, afetando plataformas como Climate FieldView e Embrapa Monitora."
            ),
        ))

    # ── Storage ──
    th = THRESHOLDS["storage_used_pct"]
    nivel = _nivel_range(t.storage_used_pct, th["alerta"], th["critico"], maior_e_pior=True)
    if nivel != NIVEL_OK:
        alertas.append(Alerta(
            parametro="Armazenamento a Bordo",
            nivel=nivel,
            valor_atual=t.storage_used_pct,
            mensagem=f"Uso de storage elevado: {t.storage_used_pct:.1f}% (limite: 80%)",
            impacto_terrestre=(
                "Se o buffer encher antes do downlink, imagens capturadas sobre "
                "áreas de plantio serão descartadas automaticamente, "
                "causando lacunas nos dados de safra e seguro rural baseado em índice."
            ),
        ))

    # ── Downlink Window ──
    th = THRESHOLDS["downlink_window_min"]
    nivel = _nivel_range(t.downlink_window_min, th["alerta"], th["critico"], maior_e_pior=False)
    if nivel != NIVEL_OK:
        alertas.append(Alerta(
            parametro="Janela de Downlink",
            nivel=nivel,
            valor_atual=t.downlink_window_min,
            mensagem=f"Janela de downlink reduzida: {t.downlink_window_min:.1f} min (mín. recomendado: 8 min)",
            impacto_terrestre=(
                "Tempo insuficiente para transmitir o volume de imagens acumulado. "
                "Dados de sensoriamento remoto podem não chegar às plataformas "
                "de análise agrícola no prazo necessário para decisões de plantio ou colheita."
            ),
        ))

    # ── Attitude Stability ──
    th = THRESHOLDS["attitude_stability"]
    nivel = _nivel_range(t.attitude_stability, th["alerta"], th["critico"], maior_e_pior=False)
    if nivel != NIVEL_OK:
        alertas.append(Alerta(
            parametro="Estabilidade de Atitude",
            nivel=nivel,
            valor_atual=t.attitude_stability,
            mensagem=f"Instabilidade de atitude detectada: {t.attitude_stability:.1f}% (mín.: 92%)",
            impacto_terrestre=(
                "Imagens geradas com rastro de movimento (motion blur) e "
                "georreferenciamento impreciso. Mapas de talhões e índices de "
                "vegetação ficam distorcidos, inviabilizando análise de precisão."
            ),
        ))

    return alertas


def nivel_geral(alertas: List[Alerta]) -> str:
    """Retorna o nível mais alto encontrado na lista de alertas."""
    if any(a.nivel == NIVEL_CRITICO for a in alertas):
        return NIVEL_CRITICO
    if any(a.nivel == NIVEL_ALERTA for a in alertas):
        return NIVEL_ALERTA
    return NIVEL_OK


def cor_nivel(nivel: str) -> str:
    return {
        NIVEL_OK:      "green",
        NIVEL_ALERTA:  "yellow",
        NIVEL_CRITICO: "red",
    }.get(nivel, "white")


def emoji_nivel(nivel: str) -> str:
    return {
        NIVEL_OK:      "✅",
        NIVEL_ALERTA:  "⚠️",
        NIVEL_CRITICO: "🚨",
    }.get(nivel, "❓")
