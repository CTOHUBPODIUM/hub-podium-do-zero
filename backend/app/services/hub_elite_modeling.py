import csv
from collections import Counter
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[3]
POPULATION_QUEUE_PATH = ROOT_DIR / "database" / "hub_elite_population_queue.csv"
CANDIDATE_REGISTRY_PATH = ROOT_DIR / "database" / "hub_elite_candidate_registry.csv"
SOURCE_AUDIT_LOG_PATH = ROOT_DIR / "database" / "hub_elite_source_audit_log.csv"
TOP25_SHORTLIST_PATH = ROOT_DIR / "database" / "hub_elite_top25_shortlist.csv"
TOP25_EXPANSION_QUEUE_PATH = ROOT_DIR / "database" / "hub_elite_top25_expansion_queue.csv"
CANDIDATE_DISCOVERY_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_candidate_discovery_board.csv"
CANDIDATE_VALIDATION_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_candidate_validation_board.csv"
EXTERNAL_AUDIT_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_external_audit_board.csv"
TOP25_GROWTH_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_top25_growth_board.csv"
TOP25_GROWTH_VALIDATION_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_top25_growth_validation_board.csv"
TOP25_GROWTH_EXTERNAL_AUDIT_BOARD_PATH = ROOT_DIR / "database" / "hub_elite_top25_growth_external_audit_board.csv"


def load_population_queue():
    if not POPULATION_QUEUE_PATH.exists():
        return []

    with POPULATION_QUEUE_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_candidate_registry():
    if not CANDIDATE_REGISTRY_PATH.exists():
        return []

    with CANDIDATE_REGISTRY_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_source_audit_log():
    if not SOURCE_AUDIT_LOG_PATH.exists():
        return []

    with SOURCE_AUDIT_LOG_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_top25_shortlist():
    if not TOP25_SHORTLIST_PATH.exists():
        return []

    with TOP25_SHORTLIST_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_top25_expansion_queue():
    if not TOP25_EXPANSION_QUEUE_PATH.exists():
        return []

    with TOP25_EXPANSION_QUEUE_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_candidate_discovery_board():
    if not CANDIDATE_DISCOVERY_BOARD_PATH.exists():
        return []

    with CANDIDATE_DISCOVERY_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_candidate_validation_board():
    if not CANDIDATE_VALIDATION_BOARD_PATH.exists():
        return []

    with CANDIDATE_VALIDATION_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_external_audit_board():
    if not EXTERNAL_AUDIT_BOARD_PATH.exists():
        return []

    with EXTERNAL_AUDIT_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_top25_growth_board():
    if not TOP25_GROWTH_BOARD_PATH.exists():
        return []

    with TOP25_GROWTH_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_top25_growth_validation_board():
    if not TOP25_GROWTH_VALIDATION_BOARD_PATH.exists():
        return []

    with TOP25_GROWTH_VALIDATION_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def load_top25_growth_external_audit_board():
    if not TOP25_GROWTH_EXTERNAL_AUDIT_BOARD_PATH.exists():
        return []

    with TOP25_GROWTH_EXTERNAL_AUDIT_BOARD_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return list(csv.DictReader(dataset))


def _normalize_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def get_hub_elite_modeling_plan():
    queue = load_population_queue()
    candidates = load_candidate_registry()
    audits = load_source_audit_log()
    shortlist = load_top25_shortlist()
    expansion_queue = load_top25_expansion_queue()
    discovery_board = load_candidate_discovery_board()
    validation_board = load_candidate_validation_board()
    external_audit_board = load_external_audit_board()
    growth_board = load_top25_growth_board()
    growth_validation_board = load_top25_growth_validation_board()
    growth_external_audit_board = load_top25_growth_external_audit_board()
    by_track = Counter(row.get("competition_track", "") for row in queue)
    by_stage = Counter(row.get("population_stage", "") for row in queue)

    return {
        "model_id": "HUB_ELITE_MODELING_PLAN_2026_05_07",
        "status": "modeling_and_population_started",
        "started_at": "2026-05-07",
        "executive_owner": "Rafael Duarte",
        "algorithm_architect": "Diego Torres",
        "objective": "Modelar o HUB-ELITE como sistema de inteligencia esportiva masculino e feminino e iniciar a populacao por posicao com pipeline operacional claro.",
        "model_layers": [
            {
                "layer": "identity",
                "goal": "Fixar trilha competitiva, posicao canonica, familia funcional e contexto do atleta.",
            },
            {
                "layer": "current_state",
                "goal": "Separar fundamentos tecnicos, taticos, fisicos e comportamentais do estado atual.",
            },
            {
                "layer": "similarity",
                "goal": "Comparar por familia posicional, estilo e referencia real coerente.",
            },
            {
                "layer": "evolution",
                "goal": "Medir potencial evolutivo, gaps prioritarios e estagio do mapa Golden Ball.",
            },
            {
                "layer": "decision",
                "goal": "Traduzir a inteligencia para relatorio, card, trilha de treino e decisao de produto.",
            },
        ],
        "population_pipeline": {
            "queue_document": str(POPULATION_QUEUE_PATH),
            "candidate_registry_document": str(CANDIDATE_REGISTRY_PATH),
            "source_audit_document": str(SOURCE_AUDIT_LOG_PATH),
            "top25_shortlist_document": str(TOP25_SHORTLIST_PATH),
            "top25_expansion_queue_document": str(TOP25_EXPANSION_QUEUE_PATH),
            "candidate_discovery_board_document": str(CANDIDATE_DISCOVERY_BOARD_PATH),
            "candidate_validation_board_document": str(CANDIDATE_VALIDATION_BOARD_PATH),
            "external_audit_board_document": str(EXTERNAL_AUDIT_BOARD_PATH),
            "top25_growth_board_document": str(TOP25_GROWTH_BOARD_PATH),
            "top25_growth_validation_board_document": str(TOP25_GROWTH_VALIDATION_BOARD_PATH),
            "top25_growth_external_audit_board_document": str(TOP25_GROWTH_EXTERNAL_AUDIT_BOARD_PATH),
            "queue_rows": len(queue),
            "candidate_registry_rows": len(candidates),
            "source_audit_rows": len(audits),
            "top25_shortlist_rows": len(shortlist),
            "top25_expansion_queue_rows": len(expansion_queue),
            "candidate_discovery_board_rows": len(discovery_board),
            "candidate_validation_board_rows": len(validation_board),
            "external_audit_board_rows": len(external_audit_board),
            "top25_growth_board_rows": len(growth_board),
            "top25_growth_validation_board_rows": len(growth_validation_board),
            "top25_growth_external_audit_board_rows": len(growth_external_audit_board),
            "by_track": dict(sorted(by_track.items())),
            "by_stage": dict(sorted(by_stage.items())),
            "stages": [
                "candidate_discovery",
                "source_audit",
                "feature_scoring",
                "runtime_seed",
                "top25_shortlist_started",
                "approved_production",
            ],
        },
        "execution_targets": {
            "target_per_position": 100,
            "positions": 11,
            "tracks": 2,
            "target_total_athletes": 2200,
            "next_milestone_per_position": 25,
        },
        "checkpoints": [
            {
                "window": "2026-05-07 a 2026-06-06",
                "focus": "Blueprint, taxonomia posicional, primeira versao do mapa Golden Ball e seed operacional.",
            },
            {
                "window": "2026-06-07 a 2026-07-06",
                "focus": "Ranking por estilo, crescimento de base masculina/feminina e sinais de video mais robustos.",
            },
            {
                "window": "2026-07-07 a 2026-08-05",
                "focus": "HUB-ELITE 2.0, rota Golden Ball operacional e dashboard tecnico executivo.",
            },
        ],
    }


def get_hub_elite_population_queue_summary():
    queue = load_population_queue()
    by_track = Counter(row.get("competition_track", "") for row in queue)
    by_stage = Counter(row.get("population_stage", "") for row in queue)

    queue_rows = []
    for row in queue:
        queue_rows.append({
            "competition_track": row.get("competition_track"),
            "canonical_position_code": row.get("canonical_position_code"),
            "position_family": row.get("position_family"),
            "target_total": _normalize_int(row.get("target_total")),
            "current_seed_count": _normalize_int(row.get("current_seed_count")),
            "current_candidate_count": _normalize_int(row.get("current_candidate_count")),
            "next_milestone_count": _normalize_int(row.get("next_milestone_count")),
            "population_stage": row.get("population_stage"),
            "owner": row.get("owner"),
            "priority": row.get("priority"),
            "next_action": row.get("next_action"),
            "source_audit_status": row.get("source_audit_status"),
        })

    return {
        "status": "population_queue_ready" if queue else "population_queue_missing",
        "queue_path": str(POPULATION_QUEUE_PATH),
        "rows": queue_rows,
        "by_track": dict(sorted(by_track.items())),
        "by_stage": dict(sorted(by_stage.items())),
    }


def get_hub_elite_candidate_registry_summary():
    candidates = load_candidate_registry()
    by_track = Counter(row.get("competition_track", "") for row in candidates)
    by_position = Counter(row.get("canonical_position_code", "") for row in candidates)
    by_audit_status = Counter(row.get("source_audit_status", "") for row in candidates)

    return {
        "status": "candidate_registry_ready" if candidates else "candidate_registry_missing",
        "registry_path": str(CANDIDATE_REGISTRY_PATH),
        "rows": len(candidates),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_audit_status": dict(sorted(by_audit_status.items())),
    }


def get_hub_elite_source_audit_summary():
    audits = load_source_audit_log()
    by_status = Counter(row.get("audit_status", "") for row in audits)
    by_auditor = Counter(row.get("auditor", "") for row in audits)

    return {
        "status": "source_audit_log_ready" if SOURCE_AUDIT_LOG_PATH.exists() else "source_audit_log_missing",
        "log_path": str(SOURCE_AUDIT_LOG_PATH),
        "rows": len(audits),
        "by_status": dict(sorted(by_status.items())),
        "by_auditor": dict(sorted(by_auditor.items())),
    }


def get_hub_elite_top25_shortlist_summary():
    shortlist = load_top25_shortlist()
    by_track = Counter(row.get("competition_track", "") for row in shortlist)
    by_position = Counter(row.get("canonical_position_code", "") for row in shortlist)
    by_stage = Counter(row.get("shortlist_stage", "") for row in shortlist)
    by_owner = Counter(row.get("owner", "") for row in shortlist)

    return {
        "status": "top25_shortlist_ready" if shortlist else "top25_shortlist_missing",
        "shortlist_path": str(TOP25_SHORTLIST_PATH),
        "rows": len(shortlist),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_stage": dict(sorted(by_stage.items())),
        "by_owner": dict(sorted(by_owner.items())),
    }


def get_hub_elite_top25_expansion_queue_summary():
    expansion_queue = load_top25_expansion_queue()
    by_track = Counter(row.get("competition_track", "") for row in expansion_queue)
    by_position = Counter(row.get("canonical_position_code", "") for row in expansion_queue)
    by_stage = Counter(row.get("expansion_stage", "") for row in expansion_queue)
    by_owner = Counter(row.get("owner", "") for row in expansion_queue)

    return {
        "status": "top25_expansion_queue_ready" if expansion_queue else "top25_expansion_queue_missing",
        "expansion_queue_path": str(TOP25_EXPANSION_QUEUE_PATH),
        "rows": len(expansion_queue),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_stage": dict(sorted(by_stage.items())),
        "by_owner": dict(sorted(by_owner.items())),
    }


def get_hub_elite_candidate_discovery_board_summary():
    board = load_candidate_discovery_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("discovery_status", "") for row in board)

    return {
        "status": "candidate_discovery_board_ready" if board else "candidate_discovery_board_missing",
        "discovery_board_path": str(CANDIDATE_DISCOVERY_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
    }


def get_hub_elite_candidate_validation_board_summary():
    board = load_candidate_validation_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("validation_status", "") for row in board)
    by_recommendation = Counter(row.get("approval_recommendation", "") for row in board)

    return {
        "status": "candidate_validation_board_ready" if board else "candidate_validation_board_missing",
        "validation_board_path": str(CANDIDATE_VALIDATION_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_recommendation": dict(sorted(by_recommendation.items())),
    }


def get_hub_elite_external_audit_board_summary():
    board = load_external_audit_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("external_audit_status", "") for row in board)
    by_recommendation = Counter(row.get("approval_recommendation", "") for row in board)

    return {
        "status": "external_audit_board_ready" if board else "external_audit_board_missing",
        "external_audit_board_path": str(EXTERNAL_AUDIT_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_recommendation": dict(sorted(by_recommendation.items())),
    }


def get_hub_elite_top25_growth_board_summary():
    board = load_top25_growth_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("growth_status", "") for row in board)

    return {
        "status": "top25_growth_board_ready" if board else "top25_growth_board_missing",
        "growth_board_path": str(TOP25_GROWTH_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
    }


def get_hub_elite_top25_growth_validation_board_summary():
    board = load_top25_growth_validation_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("validation_status", "") for row in board)
    by_recommendation = Counter(row.get("approval_recommendation", "") for row in board)

    return {
        "status": "top25_growth_validation_board_ready" if board else "top25_growth_validation_board_missing",
        "growth_validation_board_path": str(TOP25_GROWTH_VALIDATION_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_recommendation": dict(sorted(by_recommendation.items())),
    }


def get_hub_elite_top25_growth_external_audit_board_summary():
    board = load_top25_growth_external_audit_board()
    by_track = Counter(row.get("competition_track", "") for row in board)
    by_position = Counter(row.get("canonical_position_code", "") for row in board)
    by_owner = Counter(row.get("owner", "") for row in board)
    by_status = Counter(row.get("external_audit_status", "") for row in board)
    by_recommendation = Counter(row.get("approval_recommendation", "") for row in board)

    return {
        "status": "top25_growth_external_audit_board_ready" if board else "top25_growth_external_audit_board_missing",
        "growth_external_audit_board_path": str(TOP25_GROWTH_EXTERNAL_AUDIT_BOARD_PATH),
        "rows": len(board),
        "by_track": dict(sorted(by_track.items())),
        "by_position": dict(sorted(by_position.items())),
        "by_owner": dict(sorted(by_owner.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_recommendation": dict(sorted(by_recommendation.items())),
    }
