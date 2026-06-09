from dataclasses import dataclass
from typing import List
from src.telemetria import TelemetriaAgroSat

# Níveis de Alerta
NIVEL_OK = "OK"
NIVEL_ALERTA = "ALERTA"
NIVEL_CRITICO = "CRÍTICO"

@dataclass
class Alerta:
    parametro: str
    nivel: str
    valor_atual: float
    mensagem: str
    impacto_terrestre: str

def avaliar_telemetria(t: TelemetriaAgroSat) -> List[Alerta]:

    alertas = []

     # NDVI Sensor Health
    if t.ndvi_sensor_health <= 60:
            nivel = NIVEL_CRITICO
    elif t.ndvi_sensor_health <= 85:
            nivel = NIVEL_ALERTA
    else:
            nivel = NIVEL_OK
    if nivel != NIVEL_OK:
            alertas.append(
                Alerta(
                    parametro="NDVI Sensor Health",
                    nivel=nivel,
                    valor_atual=t.ndvi_sensor_health,
                    mensagem=f"Saúde do sensor NDVI baixa: {t.ndvi_sensor_health:.1f}%",
                    impacto_terrestre=(
                        "Imagens agrícolas podem apresentar baixa qualidade, "
                        "prejudicando a análise das plantações."
                    )
                )
            )

    # Temperatura do Payload
    if t.payload_temp_c >= 55 or t.payload_temp_c <= -20:
            nivel = NIVEL_CRITICO
    elif t.payload_temp_c >= 40 or t.payload_temp_c <= -10:
            nivel = NIVEL_ALERTA
    else:
            nivel = NIVEL_OK
    if nivel != NIVEL_OK:
            alertas.append(
                Alerta(
                    parametro="Temperatura do Payload",
                    nivel=nivel,
                    valor_atual=t.payload_temp_c,
                    mensagem=f"Temperatura fora da faixa: {t.payload_temp_c:.1f}°C",
                    impacto_terrestre=(
                        "O sensor pode sofrer danos e comprometer a captura "
                        "de imagens das áreas agrícolas."
                    )
                )
            )

    # Armazenamento
    if t.storage_used_pct >= 90:
            nivel = NIVEL_CRITICO
    elif t.storage_used_pct >= 80:
            nivel = NIVEL_ALERTA
    else:
            nivel = NIVEL_OK
    if nivel != NIVEL_OK:
            alertas.append(
                Alerta(
                    parametro="Armazenamento",
                    nivel=nivel,
                    valor_atual=t.storage_used_pct,
                    mensagem=f"Uso de armazenamento em {t.storage_used_pct:.1f}%",
                    impacto_terrestre=(
                        "Imagens importantes podem ser perdidas por falta de espaço."
                    )
                )
            )

# Janela de Downlink
    if t.downlink_window_min <= 3:
            nivel = NIVEL_CRITICO
    elif t.downlink_window_min <= 8:
            nivel = NIVEL_ALERTA
    else:
            nivel = NIVEL_OK
    if nivel != NIVEL_OK:
            alertas.append(
                Alerta(
                    parametro="Janela de Downlink",
                    nivel=nivel,
                    valor_atual=t.downlink_window_min,
                    mensagem=f"Janela de comunicação reduzida: {t.downlink_window_min:.1f} min",
                    impacto_terrestre=(
                        "Os dados podem demorar para chegar aos usuários na Terra."
                    )
                )
            )

# Estabilidade de Atitude
    if t.attitude_stability <= 80:
         nivel = NIVEL_CRITICO
    elif t.attitude_stability <= 92:
        nivel = NIVEL_ALERTA
    else:
        nivel = NIVEL_OK
        if nivel != NIVEL_OK:
            alertas.append(
                Alerta(
                    parametro="Estabilidade de Atitude",
                    nivel=nivel,
                    valor_atual=t.attitude_stability,
                    mensagem=f"Estabilidade reduzida: {t.attitude_stability:.1f}%",
                    impacto_terrestre=(
                        "As imagens podem sair borradas ou imprecisas."
                    )
                )
            )
    return alertas


def nivel_geral(alertas: List[Alerta]) -> str:

    for alerta in alertas:
        if alerta.nivel == NIVEL_CRITICO:
            return NIVEL_CRITICO

    for alerta in alertas:
        if alerta.nivel == NIVEL_ALERTA:
            return NIVEL_ALERTA

    return NIVEL_OK

def acao_automatica(alertas: List[Alerta]) -> str:

    for alerta in alertas:

        if alerta.parametro == "Temperatura do Payload":
            return (
                "Ação automática: sensor colocado em modo de economia "
                "para evitar superaquecimento."
            )

        if alerta.parametro == "Armazenamento":
            return (
                "Ação automática: iniciando transmissão de imagens "
                "para liberar espaço."
            )

        if alerta.parametro == "Janela de Downlink":
            return (
                "Ação automática: priorizando envio dos dados mais importantes."
            )

    return "Nenhuma ação automática necessária."

def cor_nivel(nivel: str) -> str:
    if nivel == NIVEL_OK:
        return "green"
    if nivel == NIVEL_ALERTA:
        return "yellow"
    if nivel == NIVEL_CRITICO:
        return "red"
    return "white"

def emoji_nivel(nivel: str) -> str:
    if nivel == NIVEL_OK:
        return "✅"
    if nivel == NIVEL_ALERTA:
        return "⚠️"
    if nivel == NIVEL_CRITICO:
        return "🚨"
    return "❓"
