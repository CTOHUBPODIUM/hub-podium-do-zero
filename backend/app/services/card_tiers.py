CARD_TIERS = [
    {
        "code": "comum",
        "label": "COMUM",
        "overall_min": 0,
        "overall_max": 59,
        "headline": "Base em desenvolvimento",
        "message": "Card comum para atletas em fase inicial de organizacao tecnica e evolucao.",
        "accent_rgb": [178, 186, 196],
        "secondary_rgb": [96, 105, 116],
        "dark_rgb": [14, 17, 22],
        "panel_rgb": [33, 38, 45],
    },
    {
        "code": "promessa",
        "label": "PROMESSA",
        "overall_min": 60,
        "overall_max": 74,
        "headline": "Potencial em evolucao",
        "message": "Card promessa para atletas com sinais consistentes de desenvolvimento.",
        "accent_rgb": [85, 195, 142],
        "secondary_rgb": [35, 113, 95],
        "dark_rgb": [8, 24, 27],
        "panel_rgb": [22, 44, 48],
    },
    {
        "code": "destaque",
        "label": "DESTAQUE",
        "overall_min": 75,
        "overall_max": 84,
        "headline": "Performance acima da base",
        "message": "Card destaque para atletas com leitura competitiva superior na categoria.",
        "accent_rgb": [85, 170, 220],
        "secondary_rgb": [218, 190, 88],
        "dark_rgb": [9, 20, 34],
        "panel_rgb": [25, 39, 57],
    },
    {
        "code": "elite",
        "label": "ELITE",
        "overall_min": 85,
        "overall_max": 99,
        "headline": "Perfil HUB-ELITE",
        "message": "Card elite para atletas com indicadores fortes e comparativo de alto nivel.",
        "accent_rgb": [226, 190, 76],
        "secondary_rgb": [130, 96, 28],
        "dark_rgb": [10, 12, 16],
        "panel_rgb": [24, 27, 32],
    },
]


def normalize_overall(overall):
    try:
        return max(0, min(99, int(round(float(overall)))))
    except (TypeError, ValueError):
        return 0


def get_card_tier(overall):
    normalized = normalize_overall(overall)
    for tier in CARD_TIERS:
        if tier["overall_min"] <= normalized <= tier["overall_max"]:
            return {**tier, "overall": normalized}
    return {**CARD_TIERS[-1], "overall": normalized}
