def normalize(value, minimum=0, maximum=100):
    return max(min(int(value), maximum), minimum)

ELITE_BASE = {
    "goleiro": {"speed": 55, "technique": 70, "game_iq": 85, "physical": 78},
    "zagueiro": {"speed": 70, "technique": 72, "game_iq": 82, "physical": 85},
    "lateral": {"speed": 84, "technique": 75, "game_iq": 78, "physical": 80},
    "volante": {"speed": 74, "technique": 80, "game_iq": 86, "physical": 82},
    "meia": {"speed": 76, "technique": 88, "game_iq": 90, "physical": 72},
    "ponta": {"speed": 90, "technique": 84, "game_iq": 78, "physical": 72},
    "atacante": {"speed": 82, "technique": 84, "game_iq": 82, "physical": 80}
}


def analyze_athlete(data):
    position = (data.get("position") or "meia").lower()
    base = ELITE_BASE.get(position, ELITE_BASE["meia"])

    # MVP: scores simulados/ajustáveis. Depois entra visão computacional.
    speed = normalize(data.get("speed", base["speed"] - 8))
    technique = normalize(data.get("technique", base["technique"] - 10))
    game_iq = normalize(data.get("game_iq", base["game_iq"] - 12))
    physical = normalize(data.get("physical", base["physical"] - 7))

    overall = round((speed * 0.25) + (technique * 0.30) + (game_iq * 0.30) + (physical * 0.15))
    potential = min(99, overall + 8)

    return {
        "athlete_name": data.get("athlete_name", "Atleta HUB-PODIUM"),
        "position": position,
        "overall": overall,
        "speed": speed,
        "technique": technique,
        "game_iq": game_iq,
        "physical": physical,
        "potential": potential,
        "strengths": ["Boa leitura de jogo", "Potencial de evolução", "Base técnica promissora"],
        "improvements": ["Aprimorar tomada de decisão", "Melhorar intensidade sem bola", "Treinar fundamentos específicos da posição"],
        "elite_gap": {
            "speed": base["speed"] - speed,
            "technique": base["technique"] - technique,
            "game_iq": base["game_iq"] - game_iq,
            "physical": base["physical"] - physical
        }
    }
