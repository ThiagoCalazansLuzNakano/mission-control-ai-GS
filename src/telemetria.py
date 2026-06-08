



#Implementar
#src/telemetria.py com 3-4 parâmetros simulados
#código seginte errado


"""
telemetria.py
Geração de dados simulados de telemetria do AgroSat.

Parâmetros monitorados (Trilha 1 — AgroSat):
  - ndvi_sensor_health    : Saúde do sensor multiespectral (NDVI) — %
  - payload_temp_c        : Temperatura do payload óptico — °C
  - storage_used_pct      : Capacidade de armazenamento usada — %
  - downlink_window_min   : Janela de downlink disponível — minutos
  - attitude_stability    : Estabilidade de atitude — % (100 = perfeita)
"""

class TelemetriaAgroSat:
    timestamp: str
    ndvi_sensor_health: float      # %        | normal: 85-100
    payload_temp_c: float          # °C       | normal: -10 a 40
    storage_used_pct: float        # %        | normal: 0 a 80
    downlink_window_min: float     # minutos  | normal: 8 a 30
    attitude_stability: float      # %        | normal: 92 a 100

    def to_dict(self) -> dict:
        return asdict(self)

CENARIOS = {
    "normal": {
        "ndvi_sensor_health":   (88.0, 100.0),
        "payload_temp_c":       (-5.0,  35.0),
        "storage_used_pct":     (10.0,  75.0),
        "downlink_window_min":  ( 8.0,  28.0),
        "attitude_stability":   (93.0, 100.0),
    },
    "alerta": {
        "ndvi_sensor_health":   (60.0,  84.9),
        "payload_temp_c":       (40.1,  55.0),
        "storage_used_pct":     (80.1,  90.0),
        "downlink_window_min":  ( 3.0,   7.9),
        "attitude_stability":   (80.0,  91.9),
    },
    "critico": {
        "ndvi_sensor_health":   ( 0.0,  59.9),
        "payload_temp_c":       (55.1,  80.0),
        "storage_used_pct":     (90.1, 100.0),
        "downlink_window_min":  ( 0.0,   2.9),
        "attitude_stability":   ( 0.0,  79.9),
    },
}


def _rand(low: float, high: float, decimals: int = 1) -> float:
    return round(random.uniform(low, high), decimals)


def gerar_telemetria(cenario: str = "normal") -> TelemetriaAgroSat:
    """
    Gera um snapshot de telemetria para o cenário informado.
    cenario: 'normal' | 'alerta' | 'critico' | 'aleatorio'
    """
    if cenario == "aleatorio":
        cenario = random.choices(
            ["normal", "alerta", "critico"],
            weights=[60, 25, 15],
        )[0]

    faixas = CENARIOS.get(cenario, CENARIOS["normal"])

    return TelemetriaAgroSat(
        timestamp=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        ndvi_sensor_health=_rand(*faixas["ndvi_sensor_health"]),
        payload_temp_c=_rand(*faixas["payload_temp_c"]),
        storage_used_pct=_rand(*faixas["storage_used_pct"]),
        downlink_window_min=_rand(*faixas["downlink_window_min"]),
        attitude_stability=_rand(*faixas["attitude_stability"]),
    )


def formatar_telemetria(t: TelemetriaAgroSat) -> str:
    """Retorna string legível para exibir no CLI."""
    return (
        f"  🕐 Timestamp          : {t.timestamp}\n"
        f"  🌿 NDVI Sensor Health : {t.ndvi_sensor_health:.1f}%\n"
        f"  🌡️  Payload Temp       : {t.payload_temp_c:.1f}°C\n"
        f"  💾 Storage Usado      : {t.storage_used_pct:.1f}%\n"
        f"  📡 Janela Downlink    : {t.downlink_window_min:.1f} min\n"
        f"  🎯 Estab. de Atitude  : {t.attitude_stability:.1f}%"
    )
