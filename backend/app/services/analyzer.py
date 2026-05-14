HUB_ELITE_ALGORITHM = "HUB-ELITE"

import unicodedata

from services.card_tiers import get_card_tier
from services.hub_elite_population import get_elite_profiles_for_families, get_top25_shortlist_snapshot

BASE_CATEGORIES = [f"sub-{age}" for age in range(8, 21)]
COMPETITION_TRACK_ALIASES = {
    "masculino": "masculino",
    "male": "masculino",
    "masc": "masculino",
    "m": "masculino",
    "feminino": "feminino",
    "female": "feminino",
    "fem": "feminino",
    "f": "feminino",
}

POSITION_BENCHMARKS = {
    "goleiro": {"speed": 55, "technique": 70, "game_iq": 85, "physical": 78},
    "zagueiro": {"speed": 70, "technique": 72, "game_iq": 82, "physical": 85},
    "lateral": {"speed": 84, "technique": 75, "game_iq": 78, "physical": 80},
    "volante": {"speed": 74, "technique": 80, "game_iq": 86, "physical": 82},
    "meia": {"speed": 76, "technique": 88, "game_iq": 90, "physical": 72},
    "ponta": {"speed": 90, "technique": 84, "game_iq": 78, "physical": 72},
    "atacante": {"speed": 82, "technique": 84, "game_iq": 82, "physical": 80},
}

POSITION_COMPATIBILITY = {
    "goleiro": ["goleiro"],
    "zagueiro": ["zagueiro", "volante"],
    "lateral": ["lateral", "ponta", "volante"],
    "volante": ["volante", "zagueiro", "meia"],
    "meia": ["meia", "ponta", "volante", "atacante"],
    "ponta": ["ponta", "atacante", "meia"],
    "atacante": ["atacante", "ponta", "meia"],
}

CANONICAL_POSITION_CODE_ALIASES = {
    "goleiro": "goleiro",
    "lateral direito": "lateral_direito",
    "lateral esquerdo": "lateral_esquerdo",
    "zagueiro": "zagueiro",
    "zagueiro direito": "zagueiro",
    "zagueiro central": "zagueiro",
    "zagueiro esquerdo": "zagueiro",
    "volante": "volante",
    "primeiro volante": "volante",
    "segundo volante": "volante",
    "meia central": "meia_central",
    "meia ofensivo": "meia_ofensivo",
    "meia direita": "meia_central",
    "meia esquerda": "meia_central",
    "ponta direita": "ponta_direita",
    "ponta esquerda": "ponta_esquerda",
    "ala direita": "ponta_direita",
    "ala esquerda": "ponta_esquerda",
    "segundo atacante": "segundo_atacante",
    "centroavante": "centroavante",
}

ELITE_PROFILE_ARCHETYPES = [
    {
        "name": "Gilberto Silva",
        "position_family": "volante",
        "headline": "volante equilibrado, disciplinado e forte na leitura defensiva",
        "speed": 74,
        "technique": 78,
        "game_iq": 92,
        "physical": 84,
        "style_tags": ["protecao da defesa", "jogo simples", "lideranca silenciosa"],
        "development_note": "Seu perfil pede treino de leitura, cobertura e passe seguro para controlar o ritmo do jogo.",
    },
    {
        "name": "Casemiro",
        "position_family": "volante",
        "headline": "volante competitivo, intenso e dominante nos duelos",
        "speed": 73,
        "technique": 79,
        "game_iq": 88,
        "physical": 91,
        "style_tags": ["duelo fisico", "antecipacao", "mentalidade competitiva"],
        "development_note": "Seu perfil deve evoluir intensidade, timing de combate e tomada de decisao sob pressao.",
    },
    {
        "name": "Marta",
        "competition_track": "feminino",
        "position_family": "meia",
        "headline": "meia criativa, tecnica e decisiva no ultimo terco",
        "speed": 84,
        "technique": 94,
        "game_iq": 90,
        "physical": 75,
        "style_tags": ["criatividade", "drible", "decisao ofensiva"],
        "development_note": "Seu perfil pede liberdade criativa com treino de finalizacao, passe vertical e leitura de espacos.",
    },
    {
        "name": "Ronaldinho",
        "competition_track": "masculino",
        "position_family": "meia",
        "headline": "meia ofensivo criativo, leve e imprevisivel",
        "speed": 82,
        "technique": 96,
        "game_iq": 88,
        "physical": 72,
        "style_tags": ["improviso", "drible", "alegria com bola"],
        "development_note": "Seu perfil deve proteger a criatividade, mas transformar habilidade em jogadas objetivas.",
    },
    {
        "name": "Cafu",
        "competition_track": "masculino",
        "position_family": "lateral",
        "headline": "lateral de alta energia, constancia e apoio ofensivo",
        "speed": 90,
        "technique": 80,
        "game_iq": 84,
        "physical": 88,
        "style_tags": ["resistencia", "amplitude", "lideranca"],
        "development_note": "Seu perfil pede evolucao de cruzamento, recomposicao e repeticao de alta intensidade.",
    },
    {
        "name": "Vinicius Jr",
        "competition_track": "masculino",
        "position_family": "ponta",
        "headline": "ponta explosivo, agressivo no um contra um e vertical",
        "speed": 96,
        "technique": 88,
        "game_iq": 82,
        "physical": 78,
        "style_tags": ["arrancada", "drible em velocidade", "profundidade"],
        "development_note": "Seu perfil pede treino de aceleracao, escolha da jogada e finalizacao apos conducao.",
    },
    {
        "name": "Neymar",
        "competition_track": "masculino",
        "position_family": "atacante",
        "headline": "atacante tecnico, associativo e criador de desequilibrio",
        "speed": 88,
        "technique": 95,
        "game_iq": 88,
        "physical": 74,
        "style_tags": ["drible curto", "assistencia", "criatividade"],
        "development_note": "Seu perfil deve unir tecnica e decisao rapida, evitando excesso de toque quando houver vantagem.",
    },
    {
        "name": "Ronaldo",
        "competition_track": "masculino",
        "position_family": "atacante",
        "headline": "atacante potente, rapido e objetivo para finalizar",
        "speed": 94,
        "technique": 90,
        "game_iq": 86,
        "physical": 88,
        "style_tags": ["explosao", "finalizacao", "ataque ao espaco"],
        "development_note": "Seu perfil pede treino de ataque a profundidade, finalizacao curta e protecao de bola.",
    },
    {
        "name": "Thiago Silva",
        "competition_track": "masculino",
        "position_family": "zagueiro",
        "headline": "zagueiro cerebral, tecnico e seguro na organizacao defensiva",
        "speed": 78,
        "technique": 82,
        "game_iq": 94,
        "physical": 86,
        "style_tags": ["posicionamento", "saida limpa", "comando defensivo"],
        "development_note": "Seu perfil pede leitura de linha, antecipacao e comunicacao constante com a defesa.",
    },
    {
        "name": "Alisson",
        "competition_track": "masculino",
        "position_family": "goleiro",
        "headline": "goleiro seguro, frio e forte na decisao",
        "speed": 66,
        "technique": 82,
        "game_iq": 90,
        "physical": 86,
        "style_tags": ["seguranca", "reflexo", "jogo com os pes"],
        "development_note": "Seu perfil pede reflexo, posicionamento, reposicao e coragem para decidir no tempo certo.",
    },
    {
        "name": "Hope Solo",
        "competition_track": "feminino",
        "position_family": "goleiro",
        "headline": "goleira firme, explosiva e dominante nas decisoes de area",
        "speed": 64,
        "technique": 80,
        "game_iq": 89,
        "physical": 84,
        "style_tags": ["explosao", "seguranca", "comando de area"],
        "development_note": "Seu perfil pede treino de posicionamento, tempo de bola e comunicacao constante com a linha defensiva.",
    },
    {
        "name": "Lucy Bronze",
        "competition_track": "feminino",
        "position_family": "lateral",
        "headline": "lateral poderosa, intensa e muito forte no apoio ofensivo",
        "speed": 88,
        "technique": 83,
        "game_iq": 84,
        "physical": 86,
        "style_tags": ["forca", "profundidade", "duelo"],
        "development_note": "Seu perfil pede amplitude, repeticao em alta intensidade e qualidade no cruzamento.",
    },
    {
        "name": "Wendie Renard",
        "competition_track": "feminino",
        "position_family": "zagueiro",
        "headline": "zagueira dominante, forte no jogo aereo e muito segura na lideranca",
        "speed": 73,
        "technique": 79,
        "game_iq": 91,
        "physical": 92,
        "style_tags": ["jogo aereo", "lideranca", "comando defensivo"],
        "development_note": "Seu perfil pede leitura de linha, imposicao fisica e controle da area em bolas paradas.",
    },
    {
        "name": "Aitana Bonmati",
        "competition_track": "feminino",
        "position_family": "meia",
        "headline": "meia inteligente, associativa e muito refinada na tomada de decisao",
        "speed": 80,
        "technique": 93,
        "game_iq": 95,
        "physical": 72,
        "style_tags": ["associacao", "controle", "jogo entre linhas"],
        "development_note": "Seu perfil pede jogo de apoio, leitura fina do espaco e continuidade tecnica sob pressao.",
    },
    {
        "name": "Lauren James",
        "competition_track": "feminino",
        "position_family": "ponta",
        "headline": "ponta criativa, fisica e muito perigosa no um contra um",
        "speed": 86,
        "technique": 89,
        "game_iq": 84,
        "physical": 81,
        "style_tags": ["desequilibrio", "drible", "forca ofensiva"],
        "development_note": "Seu perfil pede agressividade com controle, escolha da jogada e consistencia no ultimo terco.",
    },
    {
        "name": "Sam Kerr",
        "competition_track": "feminino",
        "position_family": "atacante",
        "headline": "atacante agressiva, potente e muito forte no ataque ao espaco",
        "speed": 87,
        "technique": 86,
        "game_iq": 85,
        "physical": 84,
        "style_tags": ["profundidade", "finalizacao", "ataque ao espaco"],
        "development_note": "Seu perfil pede repeticao de movimentos de ruptura, finalizacao rapida e leitura de ultima linha.",
    },
]

CATEGORY_DEVELOPMENT_FACTORS = {
    "sub-8": 0.58,
    "sub-9": 0.61,
    "sub-10": 0.64,
    "sub-11": 0.67,
    "sub-12": 0.70,
    "sub-13": 0.74,
    "sub-14": 0.78,
    "sub-15": 0.82,
    "sub-16": 0.86,
    "sub-17": 0.90,
    "sub-18": 0.94,
    "sub-19": 0.97,
    "sub-20": 1.00,
}

METRIC_LABELS = {
    "speed": "velocidade",
    "technique": "tecnica",
    "game_iq": "inteligencia de jogo",
    "physical": "fisico",
}

POSITION_PRIORITY_WEIGHTS = {
    "goleiro": {"game_iq": 0.32, "technique": 0.26, "physical": 0.26, "speed": 0.16},
    "zagueiro": {"game_iq": 0.30, "physical": 0.30, "speed": 0.22, "technique": 0.18},
    "lateral": {"speed": 0.30, "physical": 0.24, "technique": 0.24, "game_iq": 0.22},
    "volante": {"game_iq": 0.34, "physical": 0.24, "technique": 0.24, "speed": 0.18},
    "meia": {"game_iq": 0.32, "technique": 0.30, "speed": 0.20, "physical": 0.18},
    "ponta": {"speed": 0.34, "technique": 0.28, "game_iq": 0.20, "physical": 0.18},
    "atacante": {"technique": 0.30, "speed": 0.28, "game_iq": 0.22, "physical": 0.20},
}

CATEGORY_WEIGHT_PROFILES = {
    "foundation": {"technique": 0.34, "game_iq": 0.30, "speed": 0.20, "physical": 0.16},
    "development": {"technique": 0.30, "game_iq": 0.30, "speed": 0.22, "physical": 0.18},
    "competitive": {"game_iq": 0.31, "technique": 0.27, "speed": 0.22, "physical": 0.20},
    "high_performance": {"game_iq": 0.30, "speed": 0.25, "technique": 0.24, "physical": 0.21},
}

METRIC_DEVELOPMENT_HINTS = {
    "speed": "repeticao de arranque, mudanca de direcao e potencia nas primeiras passadas",
    "technique": "fundamentos especificos, execucao sob pressao e refinamento de gesto tecnico",
    "game_iq": "leitura de jogo, decisao rapida e entendimento de contexto competitivo",
    "physical": "forca funcional, resistencia especifica e capacidade de duelo",
}

GOLDEN_BALL_STAGES = [
    {"code": "foundation", "label": "Fundacao competitiva", "minimum": 0},
    {"code": "emerging", "label": "Talento emergente", "minimum": 63},
    {"code": "competitive", "label": "Competitivo de alto nivel", "minimum": 72},
    {"code": "high_performance", "label": "Alta performance em construcao", "minimum": 81},
    {"code": "golden_ball_track", "label": "Trilha Golden Ball", "minimum": 90},
]

POSITION_STYLE_MAP = {
    "goleiro": ["seguranca", "reflexo", "comando de area", "jogo com os pes"],
    "zagueiro": ["posicionamento", "comando defensivo", "jogo aereo", "antecipacao"],
    "lateral": ["amplitude", "profundidade", "resistencia", "duelo"],
    "volante": ["protecao da defesa", "antecipacao", "jogo simples", "mentalidade competitiva"],
    "meia": ["criatividade", "associacao", "controle", "jogo entre linhas"],
    "ponta": ["arrancada", "drible", "profundidade", "desequilibrio"],
    "atacante": ["finalizacao", "ataque ao espaco", "profundidade", "explosao"],
}

GOLDEN_BALL_CYCLE_CHECKPOINTS = {
    "foundation": [
        {"label": "Base tecnica confiavel", "minimum": 58},
        {"label": "Leitura inicial da funcao", "minimum": 64},
        {"label": "Regularidade de treino", "minimum": 70},
    ],
    "development": [
        {"label": "Habito competitivo", "minimum": 68},
        {"label": "Execucao sob pressao", "minimum": 74},
        {"label": "Consistencia por funcao", "minimum": 80},
    ],
    "competitive": [
        {"label": "Impacto competitivo acima da media", "minimum": 76},
        {"label": "Decisao em ritmo alto", "minimum": 83},
        {"label": "Dominio funcional de elite", "minimum": 89},
    ],
    "high_performance": [
        {"label": "Detalhe fino de alto rendimento", "minimum": 84},
        {"label": "Repeticao em ambiente de elite", "minimum": 90},
        {"label": "Pressao Golden Ball", "minimum": 95},
    ],
}

TRAINING_BLOCKS = {
    "speed": ["arranque curto", "mudanca de direcao", "aceleracao repetida"],
    "technique": ["fundamento especifico", "execucao sob pressao", "repeticao orientada"],
    "game_iq": ["leitura de jogo", "tomada de decisao", "video orientado"],
    "physical": ["forca funcional", "resistencia especifica", "duelo corporal"],
}

EVOLUTION_MODULE_LIBRARY = {
    "goleiro": {
        "title": "Modulo Guardian",
        "core_focus": ["reflexo", "posicionamento", "reposicao"],
    },
    "zagueiro": {
        "title": "Modulo Fortress",
        "core_focus": ["linha defensiva", "jogo aereo", "antecipacao"],
    },
    "lateral": {
        "title": "Modulo Corridor",
        "core_focus": ["amplitude", "recomposicao", "cruzamento"],
    },
    "volante": {
        "title": "Modulo Balance",
        "core_focus": ["cobertura", "passe seguro", "duelo"],
    },
    "meia": {
        "title": "Modulo Vision",
        "core_focus": ["leitura", "passe vertical", "controle entre linhas"],
    },
    "ponta": {
        "title": "Modulo Breakline",
        "core_focus": ["um contra um", "profundidade", "decisao no ultimo terco"],
    },
    "atacante": {
        "title": "Modulo Finish",
        "core_focus": ["ataque ao espaco", "finalizacao", "timing de ruptura"],
    },
}


def normalize(value, minimum=0, maximum=100):
    return max(min(int(value), maximum), minimum)


def normalize_category(category):
    raw_category = (category or "sub-12").lower().replace(" ", "").replace("_", "-")
    if raw_category.startswith("sub") and not raw_category.startswith("sub-"):
        raw_category = raw_category.replace("sub", "sub-", 1)
    return raw_category if raw_category in BASE_CATEGORIES else "sub-12"


def normalize_competition_track(value):
    normalized_value = str(value or "masculino").strip().lower()
    return COMPETITION_TRACK_ALIASES.get(normalized_value, "masculino")


def get_category_profile(category):
    normalized_category = normalize_category(category)
    age = int(normalized_category.split("-")[1])

    if age <= 12:
        return {
            "category": normalized_category,
            "experience_profile": "emotional",
            "audience": "pais_responsaveis_e_criancas",
            "tone": "acolhedor, motivador e familiar",
            "message": "O foco e incentivar o sonho, fortalecer confianca e orientar os proximos passos sem pressao excessiva.",
            "recommendation_frame": "orientacao acolhedora para desenvolvimento inicial",
        }

    return {
        "category": normalized_category,
        "experience_profile": "evolutive",
        "audience": "atletas_responsaveis_e_treinadores",
        "tone": "tecnico, evolutivo e orientado a metas",
        "message": "O foco e medir evolucao, identificar gaps e orientar treino para performance competitiva.",
        "recommendation_frame": "orientacao evolutiva com foco em treino e consistencia competitiva",
    }


def get_category_stage(category):
    age = int(normalize_category(category).split("-")[1])
    if age <= 12:
        return "foundation"
    if age <= 15:
        return "development"
    if age <= 17:
        return "competitive"
    return "high_performance"


def get_hub_elite_reference(position, category):
    normalized_position = get_position_family(position)
    normalized_category = normalize_category(category)
    position_base = POSITION_BENCHMARKS.get(normalized_position, POSITION_BENCHMARKS["meia"])
    factor = CATEGORY_DEVELOPMENT_FACTORS[normalized_category]

    return {
        key: normalize(round(value * factor), 35, 99)
        for key, value in position_base.items()
    }


def get_canonical_position_code(position):
    normalized_position = str(position or "meia").strip().lower()
    normalized_position = unicodedata.normalize("NFKD", normalized_position).encode("ascii", "ignore").decode("ascii")
    normalized_position = normalized_position.replace("_", " ").replace("-", " ")
    return CANONICAL_POSITION_CODE_ALIASES.get(normalized_position, get_position_family(normalized_position))


def get_runtime_track_benchmark(position, category, competition_track):
    canonical_position_code = get_canonical_position_code(position)
    position_family = get_position_family(position)
    normalized_category = normalize_category(category)
    factor = CATEGORY_DEVELOPMENT_FACTORS[normalized_category]

    seed_candidates = get_elite_profiles_for_families([position_family], competition_track)
    exact_candidates = [
        candidate for candidate in seed_candidates
        if candidate.get("canonical_position_code") == canonical_position_code
    ]
    archetype_candidates = [
        item for item in ELITE_PROFILE_ARCHETYPES
        if item["position_family"] == position_family
        and item.get("competition_track", "masculino") == competition_track
    ]
    benchmark_pool = exact_candidates or seed_candidates or archetype_candidates
    static_reference = POSITION_BENCHMARKS.get(position_family, POSITION_BENCHMARKS["meia"])

    averaged = {}
    for metric in ("speed", "technique", "game_iq", "physical"):
        if benchmark_pool:
            runtime_average = sum(candidate.get(metric, static_reference[metric]) for candidate in benchmark_pool) / len(benchmark_pool)
        else:
            runtime_average = static_reference[metric]
        averaged[metric] = normalize(round(runtime_average * factor), 35, 99)

    blended = {}
    for metric in ("speed", "technique", "game_iq", "physical"):
        blended[metric] = normalize(round((static_reference[metric] * factor * 0.40) + (averaged[metric] * 0.60)), 35, 99)

    return {
        **blended,
        "canonical_position_code": canonical_position_code,
        "position_family": position_family,
        "competition_track": competition_track,
        "benchmark_pool_size": len(benchmark_pool),
        "benchmark_basis": "runtime_exact_candidates" if exact_candidates else "runtime_family_candidates" if seed_candidates else "fallback_archetypes",
    }


def build_functional_family_coherence(position, competition_track, benchmark_reference):
    canonical_position_code = benchmark_reference["canonical_position_code"]
    position_family = benchmark_reference["position_family"]
    shortlist_snapshot = get_top25_shortlist_snapshot(canonical_position_code, competition_track)
    coverage_score = normalize(round((shortlist_snapshot["row_count"] / 25) * 100 if shortlist_snapshot["row_count"] else 0))
    specificity_score = 100 if canonical_position_code != position_family else 82
    runtime_pool_score = normalize(round(min(benchmark_reference["benchmark_pool_size"], 10) * 10))
    overall_score = round((coverage_score * 0.45) + (specificity_score * 0.25) + (runtime_pool_score * 0.30))

    return {
        "position_family": position_family,
        "canonical_position_code": canonical_position_code,
        "competition_track": competition_track,
        "shortlist_row_count": shortlist_snapshot["row_count"],
        "coverage_score": coverage_score,
        "specificity_score": specificity_score,
        "runtime_pool_score": runtime_pool_score,
        "score": overall_score,
        "summary": (
            f"Coerencia funcional de {overall_score} para {canonical_position_code}, com cobertura top 25 de "
            f"{shortlist_snapshot['row_count']}/25 na trilha {competition_track}."
        ),
    }


def get_calibrated_position_weights(position_family, category):
    position_weights = POSITION_PRIORITY_WEIGHTS[position_family]
    category_weights = CATEGORY_WEIGHT_PROFILES[get_category_stage(category)]
    blended = {}

    for metric in ("speed", "technique", "game_iq", "physical"):
        blended[metric] = round((position_weights[metric] * 0.65) + (category_weights[metric] * 0.35), 4)

    total = sum(blended.values()) or 1
    normalized = {
        metric: value / total
        for metric, value in blended.items()
    }
    emphasis = [METRIC_LABELS[item[0]] for item in sorted(normalized.items(), key=lambda item: item[1], reverse=True)[:2]]

    return {
        "category_stage": get_category_stage(category),
        "weights": normalized,
        "emphasis": emphasis,
        "summary": f"Para esta fase competitiva, a calibracao prioriza {', '.join(emphasis)}.",
    }


def infer_athlete_style_tags(metrics, position_family):
    tags = []
    if metrics["speed"] >= 84:
        tags.append("arrancada")
    if metrics["technique"] >= 84:
        tags.append("criatividade" if position_family in {"meia", "ponta"} else "tecnica refinada")
    if metrics["game_iq"] >= 84:
        tags.append("leitura de jogo")
    if metrics["physical"] >= 82:
        tags.append("duelo")

    tags.extend(POSITION_STYLE_MAP.get(position_family, [])[:2])
    unique_tags = []
    for tag in tags:
        if tag not in unique_tags:
            unique_tags.append(tag)
    return unique_tags[:4]

def get_position_family(position):
    normalized_position = str(position or "meia").strip().lower()
    normalized_position = unicodedata.normalize("NFKD", normalized_position).encode("ascii", "ignore").decode("ascii")
    normalized_position = normalized_position.replace("_", " ").replace("-", " ")

    if normalized_position in POSITION_BENCHMARKS:
        return normalized_position
    if "goleiro" in normalized_position or normalized_position == "gol" or "keeper" in normalized_position:
        return "goleiro"
    if "zag" in normalized_position or "beque" in normalized_position or "libero" in normalized_position:
        return "zagueiro"
    if "lat" in normalized_position or "ala" in normalized_position or "wing back" in normalized_position:
        return "lateral"
    if "vol" in normalized_position or "holding" in normalized_position or "midfield defens" in normalized_position:
        return "volante"
    if "mei" in normalized_position or "armador" in normalized_position or "playmaker" in normalized_position:
        return "meia"
    if "pont" in normalized_position or "winger" in normalized_position or "wing" in normalized_position:
        return "ponta"
    if "ata" in normalized_position or "centro" in normalized_position or "avante" in normalized_position or "striker" in normalized_position or "forward" in normalized_position:
        return "atacante"
    return "meia"


def calculate_profile_similarity(metrics, archetype, position_family):
    return calculate_similarity_breakdown(metrics, archetype, position_family, "sub-12")["overall_score"]


def calculate_position_consistency(metrics, position_family, reference, category, functional_family_coherence=None):
    weight_profile = get_calibrated_position_weights(position_family, category)
    priority_weights = weight_profile["weights"]
    weighted_alignment = 0
    component_scores = {}

    for metric, weight in priority_weights.items():
        gap = abs(metrics[metric] - reference[metric])
        metric_score = normalize(round(100 - (gap * 1.55)))
        component_scores[metric] = {
            "score": metric_score,
            "gap_to_reference": metrics[metric] - reference[metric],
            "priority_weight": weight,
        }
        weighted_alignment += metric_score * weight

    weighted_alignment = round(weighted_alignment)
    if functional_family_coherence:
        weighted_alignment = round((weighted_alignment * 0.85) + (functional_family_coherence["score"] * 0.15))
    sorted_components = sorted(
        component_scores.items(),
        key=lambda item: item[1]["score"],
        reverse=True,
    )
    strongest = [METRIC_LABELS[item[0]] for item in sorted_components[:2]]
    tensions = [METRIC_LABELS[item[0]] for item in sorted_components[-2:]]

    if weighted_alignment >= 85:
        band = "alta"
    elif weighted_alignment >= 75:
        band = "boa"
    elif weighted_alignment >= 65:
        band = "moderada"
    else:
        band = "em_desenvolvimento"

    return {
        "position_family": position_family,
        "score": weighted_alignment,
        "band": band,
        "strongest_dimensions": strongest,
        "tension_dimensions": tensions,
        "component_scores": component_scores,
        "weight_profile": weight_profile,
        "functional_family_coherence": functional_family_coherence,
        "summary": (
            f"Consistencia {band.replace('_', ' ')} para a familia {position_family}, "
            f"com melhor aderencia em {', '.join(strongest)} e maior necessidade em {', '.join(tensions)}. "
            f"{weight_profile['summary']}"
        ),
    }


def calculate_similarity_breakdown(metrics, archetype, position_family, category, functional_family_coherence=None):
    metric_keys = ("speed", "technique", "game_iq", "physical")
    distance = sum(abs(metrics[key] - archetype[key]) for key in metric_keys) / len(metric_keys)
    metric_similarity = normalize(round(100 - (distance * 1.45)), 0, 99)
    family_fit = 100 if archetype["position_family"] == position_family else 84
    if functional_family_coherence:
        family_fit = round((family_fit * 0.70) + (functional_family_coherence["score"] * 0.30))

    weight_profile = get_calibrated_position_weights(position_family, category)
    priority_weights = weight_profile["weights"]
    benchmark_fit = 0
    per_metric = {}
    for metric in metric_keys:
        gap = abs(metrics[metric] - archetype[metric])
        closeness = normalize(round(100 - (gap * 1.65)), 0, 99)
        per_metric[metric] = closeness
        benchmark_fit += closeness * priority_weights[metric]

    benchmark_fit = round(benchmark_fit)
    athlete_style_tags = infer_athlete_style_tags(metrics, position_family)
    reference_tags = archetype.get("style_tags", [])
    shared_style_tags = [tag for tag in athlete_style_tags if tag in reference_tags]
    style_fit = normalize(round((len(shared_style_tags) / max(len(reference_tags), 1)) * 100))
    overall_score = round((metric_similarity * 0.44) + (family_fit * 0.16) + (benchmark_fit * 0.25) + (style_fit * 0.15))

    return {
        "overall_score": normalize(overall_score, 0, 99),
        "metric_similarity": metric_similarity,
        "family_fit": family_fit,
        "benchmark_fit": benchmark_fit,
        "style_fit": style_fit,
        "athlete_style_tags": athlete_style_tags,
        "reference_style_tags": reference_tags,
        "shared_style_tags": shared_style_tags,
        "weight_profile": weight_profile,
        "functional_family_coherence": functional_family_coherence,
        "per_metric": per_metric,
        "summary": (
            f"Similaridade refinada com base em distancia tecnica, encaixe de familia e aderencia ao perfil de jogo da posicao. "
            f"{weight_profile['summary']}"
        ),
    }


def build_development_gaps(metrics, reference, position_family, category):
    weight_profile = get_calibrated_position_weights(position_family, category)
    priority_weights = weight_profile["weights"]
    ranked_gaps = []

    for metric in ("speed", "technique", "game_iq", "physical"):
        target = reference[metric]
        gap = max(0, target - metrics[metric])
        urgency = round(gap * (1 + priority_weights[metric]), 1)
        ranked_gaps.append(
            {
                "metric": metric,
                "label": METRIC_LABELS[metric],
                "current": metrics[metric],
                "target": target,
                "gap": gap,
                "urgency": urgency,
                "focus": METRIC_DEVELOPMENT_HINTS[metric],
            }
        )

    ranked_gaps.sort(key=lambda item: (item["gap"], item["urgency"]), reverse=True)
    return {
        "priority_gaps": ranked_gaps,
        "top_priorities": ranked_gaps[:3],
        "weight_profile": weight_profile,
        "summary": "Gaps priorizados por importancia competitiva da posicao e distancia em relacao ao perfil HUB-ELITE de referencia.",
    }


def build_category_gap_matrix(development_gaps, category):
    category_stage = get_category_stage(category)
    top_priorities = development_gaps["top_priorities"]
    urgent = [item for item in top_priorities if item["gap"] >= 8]
    moderate = [item for item in top_priorities if 4 <= item["gap"] < 8]
    maintenance = [item for item in top_priorities if item["gap"] < 4]

    stage_frames = {
        "foundation": {
            "primary_goal": "construir base tecnica e confianca competitiva",
            "coach_frame": "menos pressao por resultado e mais repeticao orientada",
        },
        "development": {
            "primary_goal": "transformar talento em habito competitivo",
            "coach_frame": "equilibrar gesto tecnico, leitura e intensidade",
        },
        "competitive": {
            "primary_goal": "ganhar consistencia para competir acima da media",
            "coach_frame": "subir exigencia sem perder identidade funcional",
        },
        "high_performance": {
            "primary_goal": "aproximar o atleta do padrao elite por detalhe fino",
            "coach_frame": "ajustar decisao, execucao e repeticao em ritmo alto",
        },
    }
    stage_frame = stage_frames[category_stage]

    return {
        "category_stage": category_stage,
        "primary_goal": stage_frame["primary_goal"],
        "coach_frame": stage_frame["coach_frame"],
        "urgent_metrics": [item["label"] for item in urgent],
        "moderate_metrics": [item["label"] for item in moderate],
        "maintenance_metrics": [item["label"] for item in maintenance],
        "summary": (
            f"Na fase {category_stage}, o foco principal e {stage_frame['primary_goal']}. "
            f"Os gaps mais urgentes hoje estao em {', '.join([item['label'] for item in urgent]) or 'nenhuma frente critica imediata'}."
        ),
    }


def build_comparative_explainability(profile_match, calibration, category_profile):
    top_match = (profile_match.get("top_matches") or [{}])[0]
    style_tags = top_match.get("shared_style_tags", [])
    parent_summary = (
        f"O atleta mostra sinais de evolucao alinhados com {profile_match.get('reference_athlete', 'referencia HUB-ELITE')}, "
        f"principalmente em {', '.join(style_tags) or 'perfil competitivo geral'}. "
        f"O foco agora e desenvolver {', '.join(calibration.get('priority_focus', [])[:2]) or 'consistencia tecnica'} sem pressa excessiva."
    )
    club_summary = (
        f"Leitura HUB-ELITE indica aderencia funcional em {calibration.get('functional_family_coherence', {}).get('canonical_position_code', profile_match.get('position_family', 'slot'))}, "
        f"com consistencia {calibration.get('position_consistency', {}).get('band', 'moderada')} e prioridade em {', '.join(calibration.get('priority_focus', [])[:3]) or 'refino competitivo'}."
    )
    athlete_summary = (
        f"Seu jogo se aproxima de {profile_match.get('reference_athlete', 'uma referencia elite')} por {', '.join(style_tags) or 'caracteristicas do seu perfil'}. "
        f"Para subir de nivel, concentre energia em {', '.join(calibration.get('priority_focus', [])[:2]) or 'evolucao diaria'}."
    )

    return {
        "parent_summary": parent_summary,
        "club_summary": club_summary,
        "athlete_summary": athlete_summary,
        "tone": category_profile.get("tone"),
    }


def build_training_roadmap(development_gaps, golden_ball_map, category_gap_matrix, category):
    category_stage = get_category_stage(category)
    roadmap_blocks = []
    for week_index, priority in enumerate(development_gaps.get("top_priorities", [])[:3], start=1):
        roadmap_blocks.append(
            {
                "cycle": f"ciclo_{week_index}",
                "metric": priority["metric"],
                "label": priority["label"],
                "goal": f"Reduzir o gap de {priority['label']} com foco em {priority['focus']}.",
                "training_blocks": TRAINING_BLOCKS[priority["metric"]],
                "checkpoint": f"Revisar progresso do ciclo {week_index} com video curto e percepcao de consistencia.",
            }
        )

    return {
        "category_stage": category_stage,
        "primary_goal": category_gap_matrix.get("primary_goal"),
        "coach_frame": category_gap_matrix.get("coach_frame"),
        "cycles": roadmap_blocks,
        "next_golden_ball_checkpoint": golden_ball_map.get("next_cycle_checkpoint"),
        "summary": (
            f"Roadmap de treino organizado em {len(roadmap_blocks)} ciclos curtos para aproximar o atleta do proximo checkpoint Golden Ball."
        ),
    }


def build_evolution_subscription_offer(position_family, category, training_roadmap, category_gap_matrix, comparative_explainability):
    category_stage = get_category_stage(category)
    module = EVOLUTION_MODULE_LIBRARY[position_family]
    stage_labels = {
        "foundation": "Entrada guiada",
        "development": "Desenvolvimento competitivo",
        "competitive": "Aceleração de performance",
        "high_performance": "Refino elite",
    }

    weekly_modules = []
    for cycle in training_roadmap.get("cycles", []):
        weekly_modules.append(
            {
                "week": cycle["cycle"],
                "headline": cycle["label"],
                "focus_blocks": cycle["training_blocks"],
                "goal": cycle["goal"],
            }
        )

    return {
        "plan_name": "Acompanhamento em estudo",
        "module_name": module["title"],
        "position_family": position_family,
        "category_stage": category_stage,
        "program_tier": stage_labels[category_stage],
        "delivery_model": "frente em estudo para acompanhamento assistido, sem comercialização ativa",
        "core_focus": module["core_focus"],
        "weekly_modules": weekly_modules,
        "sales_summary": (
            f"{module['title']} segue como frente em estudo para acompanhamento assistido em {position_family}, "
            f"na etapa {stage_labels[category_stage].lower()}, com foco em {', '.join(module['core_focus'])}. "
            f"Nesta etapa, usamos esse bloco apenas como apoio ao piloto, sem oferta comercial ativa."
        ),
        "guardian_pitch": comparative_explainability.get("parent_summary"),
        "club_pitch": comparative_explainability.get("club_summary"),
        "coach_frame": category_gap_matrix.get("coach_frame"),
    }


def build_customer_offers(evolution_subscription, comparative_explainability, training_roadmap, category_gap_matrix):
    parent_offer = {
        "segment": "pais_responsaveis",
        "headline": "Leitura assistida para familias durante a fase beta",
        "primary_value": "clareza sobre evolução, rotina de treino e próximos passos, sem abertura comercial neste momento",
        "offer_summary": comparative_explainability.get("parent_summary"),
        "cta": "Registrar observacoes do piloto e consolidar aprendizados antes de qualquer oferta.",
    }
    club_offer = {
        "segment": "clubes",
        "headline": "Leitura assistida para equipes tecnicas na fase beta",
        "primary_value": "padronizar devolutiva, acompanhamento de gaps e checkpoints competitivos em ambiente de teste",
        "offer_summary": comparative_explainability.get("club_summary"),
        "cta": "Consolidar feedback técnico e maturidade operacional antes de qualquer abertura comercial.",
    }
    school_offer = {
        "segment": "escolas",
        "headline": "Uso pedagogico em observacao para escolas e projetos",
        "primary_value": "organizar trilhas de treino, devolutiva para familias e progressao por categoria em ambiente assistido",
        "offer_summary": (
            f"A escola pode usar o {evolution_subscription.get('module_name')} para estruturar ciclos curtos, "
            f"com foco em {', '.join(evolution_subscription.get('core_focus', []))} e checkpoints de evolucao."
        ),
        "cta": "Usar o piloto para entender aderência pedagógica antes de qualquer modelagem comercial.",
    }

    return {
        "parent_offer": parent_offer,
        "club_offer": club_offer,
        "school_offer": school_offer,
        "summary": (
            f"Frentes de acompanhamento em estudo para famílias, clubes e escolas, usando a mesma trilha evolutiva com foco em {category_gap_matrix.get('primary_goal')}, sem comercialização ativa nesta fase."
        ),
    }


def build_onboarding_journey(evolution_subscription, customer_offers, training_roadmap):
    steps = [
        {
            "step": 1,
            "title": "Diagnostico inicial",
            "description": "Atleta envia video e recebe leitura HUB-ELITE com foco em consistencia, gaps e proximo checkpoint.",
        },
        {
            "step": 2,
            "title": "Definicao de foco",
            "description": f"Equipe organiza o {evolution_subscription.get('module_name', 'modulo evolutivo')} como referencia de acompanhamento beta.",
        },
        {
            "step": 3,
            "title": "Ciclos de treino",
            "description": f"Roadmap aplicado em {len(training_roadmap.get('cycles', []))} ciclos curtos com checkpoints de video.",
        },
        {
            "step": 4,
            "title": "Reavaliacao",
            "description": "Novo envio de video, atualizacao de gaps e leitura do proximo checkpoint Golden Ball.",
        },
    ]

    return {
        "steps": steps,
        "summary": (
            f"Roteiro beta em {len(steps)} etapas para levar o caso do diagnostico inicial ate a devolutiva assistida."
        ),
        "segment_ctas": {
            "pais_responsaveis": customer_offers["parent_offer"]["cta"],
            "clubes": customer_offers["club_offer"]["cta"],
            "escolas": customer_offers["school_offer"]["cta"],
        },
    }


def build_commercial_plans(evolution_subscription, customer_offers, onboarding_journey):
    plans = {
        "pais_responsaveis": {
            "plan_name": "Familias em estudo",
            "price_brl_month": 0,
            "billing_cycle": "sem comercialização ativa",
            "primary_channel": "devolutiva assistida",
            "headline": customer_offers["parent_offer"]["headline"],
            "short_site_copy": "Frente em estudo para acompanhar a evolucao do atleta com mais clareza durante o piloto.",
            "short_linkedin_copy": "Frente em estudo, ainda sem oferta comercial ativa.",
            "short_whatsapp_copy": "Uso beta assistido, sem venda aberta nesta fase.",
        },
        "clubes": {
            "plan_name": "Clubes em estudo",
            "price_brl_month": 0,
            "billing_cycle": "sem comercialização ativa",
            "primary_channel": "devolutiva assistida",
            "headline": customer_offers["club_offer"]["headline"],
            "short_site_copy": "Frente em estudo para leitura de gaps e checkpoints em ambiente assistido.",
            "short_linkedin_copy": "Estrutura em estudo para uso técnico futuro, ainda sem comercialização ativa.",
            "short_whatsapp_copy": "Leitura beta assistida, sem abertura comercial neste momento.",
        },
        "escolas": {
            "plan_name": "Escolas em estudo",
            "price_brl_month": 0,
            "billing_cycle": "sem comercialização ativa",
            "primary_channel": "devolutiva assistida",
            "headline": customer_offers["school_offer"]["headline"],
            "short_site_copy": "Frente em estudo para apoiar leitura pedagogica e evolutiva em ambiente de piloto.",
            "short_linkedin_copy": "Estrutura em observação para uso futuro, sem definição comercial.",
            "short_whatsapp_copy": "Material de referencia interna, sem venda aberta nesta fase.",
        },
    }

    return {
        "plans": plans,
        "summary": (
            "Estrutura interna de frentes em estudo, sem precificação pública ou comercialização ativa nesta fase."
        ),
        "launch_order": ["pais_responsaveis", "escolas", "clubes"],
        "onboarding_summary": onboarding_journey.get("summary"),
    }


def build_sales_activation_flow(commercial_plans, onboarding_journey):
    plan_order = commercial_plans.get("launch_order", [])
    plans = commercial_plans.get("plans", {})
    activation_steps = []

    for index, segment in enumerate(plan_order, start=1):
        plan = plans.get(segment, {})
        activation_steps.append(
            {
                "step": index,
                "segment": segment,
                "plan_name": plan.get("plan_name"),
                "entry_channel": plan.get("primary_channel"),
                "conversion_goal": f"Levar {segment.replace('_', ' ')} da observacao inicial para devolutiva assistida e coleta de feedback.",
                "message_asset": {
                    "site": plan.get("short_site_copy"),
                    "linkedin": plan.get("short_linkedin_copy"),
                    "whatsapp": plan.get("short_whatsapp_copy"),
                },
            }
        )

    return {
        "activation_steps": activation_steps,
        "summary": (
            f"Fluxo beta estruturado em {len(activation_steps)} frentes de acompanhamento, sem checkout ou oferta comercial ativa."
        ),
        "checkout_readiness": "beta_assistida_sem_checkout",
        "next_stack_recommendation": "validar teste de campo, linguagem e segurança antes de qualquer abertura comercial",
        "onboarding_dependency": onboarding_journey.get("summary"),
    }


def build_golden_ball_map(overall, potential, consistency, similarity, development_gaps, category):
    category_stage = get_category_stage(category)
    stage_score = round(
        (overall * 0.35)
        + (potential * 0.20)
        + (consistency["score"] * 0.25)
        + (similarity["overall_score"] * 0.20)
    )
    current_stage = GOLDEN_BALL_STAGES[0]
    next_stage = None

    for index, stage in enumerate(GOLDEN_BALL_STAGES):
        if stage_score >= stage["minimum"]:
            current_stage = stage
            next_stage = GOLDEN_BALL_STAGES[index + 1] if index + 1 < len(GOLDEN_BALL_STAGES) else None

    focus_metrics = [item["label"] for item in development_gaps["top_priorities"] if item["gap"] > 0]
    readiness_gap = 0 if next_stage is None else max(0, next_stage["minimum"] - stage_score)
    category_age = int(category.split("-")[1])
    cycle_checkpoints = GOLDEN_BALL_CYCLE_CHECKPOINTS[category_stage]
    checkpoint_progress = []
    for checkpoint in cycle_checkpoints:
        checkpoint_progress.append(
            {
                "label": checkpoint["label"],
                "minimum": checkpoint["minimum"],
                "achieved": stage_score >= checkpoint["minimum"],
                "distance": max(0, checkpoint["minimum"] - stage_score),
            }
        )
    next_cycle_checkpoint = next((item for item in checkpoint_progress if not item["achieved"]), None)

    return {
        "stage_score": stage_score,
        "category_stage": category_stage,
        "current_stage": current_stage["label"],
        "current_stage_code": current_stage["code"],
        "next_stage": next_stage["label"] if next_stage else "Elite consolidado",
        "next_stage_code": next_stage["code"] if next_stage else "elite_consolidated",
        "readiness_gap": readiness_gap,
        "time_horizon": "medio_prazo" if category_age <= 14 else "curto_medio_prazo",
        "focus_metrics": focus_metrics,
        "cycle_checkpoints": checkpoint_progress,
        "next_cycle_checkpoint": next_cycle_checkpoint,
        "summary": (
            f"O atleta esta hoje em '{current_stage['label']}' e precisa reduzir {readiness_gap} pontos para o proximo estagio."
            if next_stage
            else "O atleta ja opera na faixa mais alta do mapa Golden Ball atual do HUB-ELITE."
        ),
    }


def get_elite_profile_match(metrics, position, category_profile, competition_track, category, functional_family_coherence=None):
    position_family = get_position_family(position)
    compatible_families = POSITION_COMPATIBILITY.get(position_family, [position_family])
    seed_candidate_pool = get_elite_profiles_for_families(compatible_families, competition_track)
    archetype_candidate_pool = [
        item for item in ELITE_PROFILE_ARCHETYPES
        if item["position_family"] in compatible_families
        and item.get("competition_track", "masculino") == competition_track
    ]
    candidate_pool = seed_candidate_pool or archetype_candidate_pool
    if not candidate_pool:
        candidate_pool = [
            item for item in ELITE_PROFILE_ARCHETYPES
            if item["position_family"] == position_family
        ] or ELITE_PROFILE_ARCHETYPES

    ranked_pairs = [
        (
            item,
            calculate_similarity_breakdown(metrics, item, position_family, category, functional_family_coherence),
        )
        for item in candidate_pool
    ]
    ranked_pairs.sort(key=lambda pair: pair[1]["overall_score"], reverse=True)
    best, similarity = ranked_pairs[0]
    tone = "emocional" if category_profile["experience_profile"] == "emotional" else "evolutivo"

    return {
        "reference_athlete": best["name"],
        "position_family": position_family,
        "candidate_families": compatible_families,
        "candidate_pool_size": len(candidate_pool),
        "competition_track": competition_track,
        "source_dataset": best.get("source_dataset", "beta_archetypes"),
        "canonical_position_code": best.get("canonical_position_code"),
        "review_status": best.get("review_status", "beta_archetype"),
        "source_confidence": best.get("source_confidence"),
        "hub_elite_score": best.get("hub_elite_score"),
        "primary_source_url": best.get("primary_source_url"),
        "secondary_source_url": best.get("secondary_source_url"),
        "similarity_score": similarity["overall_score"],
        "similarity_breakdown": similarity,
        "profile_headline": best["headline"],
        "style_tags": best["style_tags"],
        "development_note": best["development_note"],
        "comparison_text": (
            f"Seu perfil se parece com o do {best['name']} em uma leitura {tone}: "
            f"{best['headline']}."
        ),
        "development_summary": (
            f"A referencia de perfil sugere foco de desenvolvimento em {best['development_note'].lower()}"
        ),
        "top_matches": [
            {
                "reference_athlete": candidate["name"],
                "position_family": candidate["position_family"],
                "similarity_score": candidate_similarity["overall_score"],
                "style_fit": candidate_similarity["style_fit"],
                "shared_style_tags": candidate_similarity["shared_style_tags"],
            }
            for candidate, candidate_similarity in ranked_pairs[:3]
        ],
        "method": "comparacao ponderada por posicao compativel, base HUB-ELITE seed, velocidade, tecnica, inteligencia de jogo e fisico",
        "disclaimer": "Comparacao de perfil esportivo, nao uma previsao de carreira ou equivalencia direta com atleta profissional.",
    }


def analyze_athlete(data):
    position = (data.get("position") or "meia").lower()
    position_family = get_position_family(position)
    category = normalize_category(data.get("category"))
    competition_track = normalize_competition_track(
        data.get("competition_track") or data.get("gender")
    )
    reference = get_runtime_track_benchmark(position, category, competition_track)
    category_profile = get_category_profile(category)

    # MVP: entrada simulada/ajustavel. Na fase de visao computacional,
    # estes atributos virao da leitura automatica do video.
    speed = normalize(data.get("speed", reference["speed"] - 5))
    technique = normalize(data.get("technique", reference["technique"] - 6))
    game_iq = normalize(data.get("game_iq", reference["game_iq"] - 7))
    physical = normalize(data.get("physical", reference["physical"] - 4))

    overall = round((speed * 0.25) + (technique * 0.30) + (game_iq * 0.30) + (physical * 0.15))
    card_tier = get_card_tier(overall)
    potential_bonus = 10 if category_profile["experience_profile"] == "emotional" else 7
    potential = min(99, overall + potential_bonus)
    metrics = {
        "speed": speed,
        "technique": technique,
        "game_iq": game_iq,
        "physical": physical,
    }
    functional_family_coherence = build_functional_family_coherence(position, competition_track, reference)
    profile_match = get_elite_profile_match(metrics, position_family, category_profile, competition_track, category, functional_family_coherence)
    position_consistency = calculate_position_consistency(metrics, position_family, reference, category, functional_family_coherence)
    development_gaps = build_development_gaps(metrics, reference, position_family, category)
    category_gap_matrix = build_category_gap_matrix(development_gaps, category)
    golden_ball_map = build_golden_ball_map(
        overall,
        potential,
        position_consistency,
        profile_match["similarity_breakdown"],
        development_gaps,
        category,
    )
    comparative_explainability = build_comparative_explainability(
        profile_match,
        {
            "functional_family_coherence": functional_family_coherence,
            "position_consistency": position_consistency,
            "priority_focus": [
                item["label"] for item in development_gaps["top_priorities"] if item["gap"] > 0
            ],
        },
        category_profile,
    )
    training_roadmap = build_training_roadmap(
        development_gaps,
        golden_ball_map,
        category_gap_matrix,
        category,
    )
    evolution_subscription = build_evolution_subscription_offer(
        position_family,
        category,
        training_roadmap,
        category_gap_matrix,
        comparative_explainability,
    )
    customer_offers = build_customer_offers(
        evolution_subscription,
        comparative_explainability,
        training_roadmap,
        category_gap_matrix,
    )
    onboarding_journey = build_onboarding_journey(
        evolution_subscription,
        customer_offers,
        training_roadmap,
    )
    commercial_plans = build_commercial_plans(
        evolution_subscription,
        customer_offers,
        onboarding_journey,
    )
    sales_activation_flow = build_sales_activation_flow(
        commercial_plans,
        onboarding_journey,
    )
    calibration = {
        "position_consistency": position_consistency,
        "functional_family_coherence": functional_family_coherence,
        "similarity_refinement": profile_match["similarity_breakdown"],
        "development_gaps": development_gaps,
        "category_gap_matrix": category_gap_matrix,
        "golden_ball_map": golden_ball_map,
        "comparative_explainability": comparative_explainability,
        "training_roadmap": training_roadmap,
        "evolution_subscription": evolution_subscription,
        "customer_offers": customer_offers,
        "onboarding_journey": onboarding_journey,
        "commercial_plans": commercial_plans,
        "sales_activation_flow": sales_activation_flow,
        "priority_focus": [
            item["label"] for item in development_gaps["top_priorities"] if item["gap"] > 0
        ],
    }
    facial_verification = data.get("facial_verification") or {}
    executive_summary = {
        "profile_reading": profile_match["comparison_text"],
        "development_recommendation": profile_match["development_note"],
        "category_guidance": category_profile["message"],
        "calibration_summary": position_consistency["summary"],
        "category_gap_summary": category_gap_matrix["summary"],
        "golden_ball_summary": golden_ball_map["summary"],
        "parent_explanation": comparative_explainability["parent_summary"],
        "club_explanation": comparative_explainability["club_summary"],
        "athlete_explanation": comparative_explainability["athlete_summary"],
        "training_roadmap_summary": training_roadmap["summary"],
        "subscription_summary": evolution_subscription["sales_summary"],
        "customer_offer_summary": customer_offers["summary"],
        "onboarding_summary": onboarding_journey["summary"],
        "commercial_plan_summary": commercial_plans["summary"],
        "sales_activation_summary": sales_activation_flow["summary"],
        "institutional_note": (
            "Esta analise apoia o desenvolvimento do atleta e nao representa previsao de carreira, promessa esportiva ou equivalencia direta com atleta profissional."
        ),
    }

    return {
        "algorithm": HUB_ELITE_ALGORITHM,
        "analysis_mode": "automatic_video_analysis",
        "athlete_name": data.get("athlete_name", "Atleta HUB-PODIUM"),
        "category": category,
        "category_profile": category_profile,
        "position": position,
        "position_family": position_family,
        "competition_track": competition_track,
        "responsible_whatsapp": data.get("responsible_whatsapp"),
        "supporter_club": data.get("supporter_club"),
        "overall": overall,
        "card_tier": card_tier,
        "speed": speed,
        "technique": technique,
        "game_iq": game_iq,
        "physical": physical,
        "potential": potential,
        "hub_elite_reference": reference,
        "elite_profile_match": profile_match,
        "calibration": calibration,
        "executive_summary": executive_summary,
        "recognition": {
            "athlete_photo_required": True,
            "athlete_photo_received": bool(data.get("athlete_photo_path")),
            "facial_recognition_required": True,
            "video_identity_check": facial_verification.get("status", "photo_video_reference_ready" if data.get("athlete_photo_path") else "photo_missing"),
            "match_confidence": facial_verification.get("match_confidence"),
            "faces_detected_in_video": facial_verification.get("faces_detected_in_video"),
            "message": facial_verification.get("message", "A foto do atleta e usada como referencia inicial para reconhecimento no fluxo de video."),
        },
        "strengths": ["Boa base de evolucao", "Potencial de desenvolvimento", "Resposta positiva ao treinamento"],
        "improvements": [
            "Aprimorar tomada de decisao",
            "Melhorar intensidade sem bola",
            "Treinar fundamentos especificos da posicao",
        ],
        "elite_gap": {
            "speed": reference["speed"] - speed,
            "technique": reference["technique"] - technique,
            "game_iq": reference["game_iq"] - game_iq,
            "physical": reference["physical"] - physical,
        },
        "deliverables": {
            "pdf_report": True,
            "fifa_style_card": True,
            "guardian_share": True,
        },
    }
