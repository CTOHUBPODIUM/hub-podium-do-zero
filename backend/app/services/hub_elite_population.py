import csv
from collections import Counter
from functools import lru_cache
from pathlib import Path

from services.hub_elite_modeling import (
    get_hub_elite_candidate_discovery_board_summary,
    get_hub_elite_candidate_registry_summary,
    get_hub_elite_candidate_validation_board_summary,
    get_hub_elite_external_audit_board_summary,
    get_hub_elite_population_queue_summary,
    get_hub_elite_source_audit_summary,
    get_hub_elite_top25_growth_board_summary,
    get_hub_elite_top25_growth_external_audit_board_summary,
    get_hub_elite_top25_growth_validation_board_summary,
    get_hub_elite_top25_expansion_queue_summary,
    get_hub_elite_top25_shortlist_summary,
)


ROOT_DIR = Path(__file__).resolve().parents[3]
SEED_DATASET_PATH = ROOT_DIR / "database" / "hub_elite_real_athletes_seed.csv"
TOP25_SHORTLIST_PATH = ROOT_DIR / "database" / "hub_elite_top25_shortlist.csv"
TARGET_PER_POSITION = 100
TRACK_TARGET_TOTAL_ATHLETES = 1100
TARGET_TOTAL_ATHLETES = 2200
RUNTIME_ELIGIBLE_STATUSES = {"seed_beta", "approved_beta", "approved_production"}
COMPETITION_TRACKS = ["masculino", "feminino"]
CANONICAL_POSITION_CODES = [
    "goleiro",
    "lateral_direito",
    "lateral_esquerdo",
    "zagueiro",
    "volante",
    "meia_central",
    "meia_ofensivo",
    "ponta_direita",
    "ponta_esquerda",
    "segundo_atacante",
    "centroavante",
]


def normalize_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def normalize_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_style_tags(value):
    return [
        item.strip()
        for item in str(value or "").split("|")
        if item.strip()
    ]


def normalize_row(row):
    competition_track = (row.get("competition_track") or "masculino").strip().lower()
    if competition_track not in COMPETITION_TRACKS:
        competition_track = "masculino"

    return {
        "name": row.get("athlete_name", "").strip(),
        "competition_track": competition_track,
        "canonical_position_code": row.get("canonical_position_code", "").strip(),
        "position_family": row.get("position_family", "").strip(),
        "nationality": row.get("nationality", "").strip(),
        "active_from": normalize_int(row.get("active_from")),
        "active_to": normalize_int(row.get("active_to")),
        "primary_source_url": row.get("primary_source_url", "").strip(),
        "secondary_source_url": row.get("secondary_source_url", "").strip(),
        "source_confidence": normalize_float(row.get("source_confidence")),
        "performance_official": normalize_int(row.get("performance_official")),
        "position_excellence": normalize_int(row.get("position_excellence")),
        "competitive_peak": normalize_int(row.get("competitive_peak")),
        "longevity": normalize_int(row.get("longevity")),
        "international_continental_impact": normalize_int(row.get("international_continental_impact")),
        "scout_awards_consensus": normalize_int(row.get("scout_awards_consensus")),
        "hub_elite_score": normalize_int(row.get("hub_elite_score")),
        "speed": normalize_int(row.get("speed")),
        "technique": normalize_int(row.get("technique")),
        "game_iq": normalize_int(row.get("game_iq")),
        "physical": normalize_int(row.get("physical")),
        "style_tags": parse_style_tags(row.get("style_tags")),
        "headline": row.get("profile_headline", "").strip(),
        "development_note": row.get("development_note", "").strip(),
        "review_status": row.get("review_status", "").strip(),
        "notes": row.get("notes", "").strip(),
        "source_dataset": "hub_elite_real_athletes_seed",
    }


@lru_cache(maxsize=1)
def load_seed_athletes():
    if not SEED_DATASET_PATH.exists():
        return []

    with SEED_DATASET_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return [
            normalize_row(row)
            for row in csv.DictReader(dataset)
            if row.get("athlete_name")
        ]


@lru_cache(maxsize=1)
def load_top25_shortlist_rows():
    if not TOP25_SHORTLIST_PATH.exists():
        return []

    with TOP25_SHORTLIST_PATH.open("r", encoding="utf-8-sig", newline="") as dataset:
        return [row for row in csv.DictReader(dataset) if row.get("athlete_name")]


def as_profile_candidate(athlete):
    return {
        "name": athlete["name"],
        "competition_track": athlete["competition_track"],
        "position_family": athlete["position_family"],
        "canonical_position_code": athlete["canonical_position_code"],
        "headline": athlete["headline"],
        "speed": athlete["speed"],
        "technique": athlete["technique"],
        "game_iq": athlete["game_iq"],
        "physical": athlete["physical"],
        "style_tags": athlete["style_tags"],
        "development_note": athlete["development_note"],
        "hub_elite_score": athlete["hub_elite_score"],
        "source_confidence": athlete["source_confidence"],
        "review_status": athlete["review_status"],
        "source_dataset": athlete["source_dataset"],
        "primary_source_url": athlete["primary_source_url"],
        "secondary_source_url": athlete["secondary_source_url"],
    }


def get_elite_profiles_for_families(position_families, competition_track=None):
    families = set(position_families or [])
    normalized_track = (competition_track or "masculino").strip().lower()
    if normalized_track not in COMPETITION_TRACKS:
        normalized_track = "masculino"

    return [
        as_profile_candidate(athlete)
        for athlete in load_seed_athletes()
        if athlete["position_family"] in families
        and athlete["competition_track"] == normalized_track
        and athlete["review_status"] in RUNTIME_ELIGIBLE_STATUSES
    ]


def get_top25_shortlist_snapshot(canonical_position_code=None, competition_track=None):
    normalized_track = (competition_track or "masculino").strip().lower()
    if normalized_track not in COMPETITION_TRACKS:
        normalized_track = "masculino"

    rows = [
        row for row in load_top25_shortlist_rows()
        if row.get("competition_track", "").strip().lower() == normalized_track
    ]

    if canonical_position_code:
        rows = [
            row for row in rows
            if row.get("canonical_position_code", "").strip() == canonical_position_code
        ]

    counts_by_position = Counter(row.get("canonical_position_code", "").strip() for row in rows)
    return {
        "competition_track": normalized_track,
        "canonical_position_code": canonical_position_code,
        "row_count": len(rows),
        "counts_by_position": dict(sorted(counts_by_position.items())),
        "status": "ready" if rows else "empty",
    }


def get_seed_population_summary():
    athletes = load_seed_athletes()
    by_position = Counter(athlete["canonical_position_code"] for athlete in athletes)
    by_family = Counter(athlete["position_family"] for athlete in athletes)
    by_track = Counter(athlete["competition_track"] for athlete in athletes)
    by_review_status = Counter(athlete["review_status"] for athlete in athletes)
    runtime_eligible_count = sum(
        1 for athlete in athletes
        if athlete["review_status"] in RUNTIME_ELIGIBLE_STATUSES
    )

    return {
        "status": "seed_population_started" if athletes else "seed_population_empty",
        "dataset_path": str(SEED_DATASET_PATH),
        "modeling_status": "started",
        "seed_count": len(athletes),
        "runtime_eligible_count": runtime_eligible_count,
        "target_total_athletes": TARGET_TOTAL_ATHLETES,
        "target_coverage_percent": round((len(athletes) / TARGET_TOTAL_ATHLETES) * 100, 2),
        "track_target_total_athletes": TRACK_TARGET_TOTAL_ATHLETES,
        "competition_tracks": [
            {
                "code": track,
                "seed_count": by_track.get(track, 0),
                "target_total_athletes": TRACK_TARGET_TOTAL_ATHLETES,
                "target_coverage_percent": round((by_track.get(track, 0) / TRACK_TARGET_TOTAL_ATHLETES) * 100, 2),
            }
            for track in COMPETITION_TRACKS
        ],
        "positions_started": sum(1 for code in CANONICAL_POSITION_CODES if by_position.get(code, 0) > 0),
        "positions_target": len(CANONICAL_POSITION_CODES),
        "target_per_position": TARGET_PER_POSITION,
        "position_progress": [
            {
                "canonical_position_code": code,
                "populated": by_position.get(code, 0),
                "target": TARGET_PER_POSITION,
                "progress_percent": round((by_position.get(code, 0) / TARGET_PER_POSITION) * 100, 2),
            }
            for code in CANONICAL_POSITION_CODES
        ],
        "family_counts": dict(sorted(by_family.items())),
        "review_status_counts": dict(sorted(by_review_status.items())),
        "runtime_policy": {
            "eligible_statuses": sorted(RUNTIME_ELIGIBLE_STATUSES),
            "stage": "seed_beta_refines_runtime_but_requires_source_audit_before_production",
        },
        "population_queue": get_hub_elite_population_queue_summary(),
        "candidate_registry": get_hub_elite_candidate_registry_summary(),
        "source_audit": get_hub_elite_source_audit_summary(),
        "top25_shortlist": get_hub_elite_top25_shortlist_summary(),
        "top25_expansion_queue": get_hub_elite_top25_expansion_queue_summary(),
        "candidate_discovery_board": get_hub_elite_candidate_discovery_board_summary(),
        "candidate_validation_board": get_hub_elite_candidate_validation_board_summary(),
        "external_audit_board": get_hub_elite_external_audit_board_summary(),
        "top25_growth_board": get_hub_elite_top25_growth_board_summary(),
        "top25_growth_validation_board": get_hub_elite_top25_growth_validation_board_summary(),
        "top25_growth_external_audit_board": get_hub_elite_top25_growth_external_audit_board_summary(),
    }
