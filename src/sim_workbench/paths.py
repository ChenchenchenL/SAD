from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("SIM_ROOT", Path(__file__).resolve().parents[2])).resolve()

DATA = ROOT / "data"
EXTERNAL = DATA / "external"
LIBRARY = DATA / "library"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
EXPERIMENTS = ROOT / "experiments"
RESULTS = ROOT / "results"
MANUSCRIPT = ROOT / "manuscript"
DOCS = ROOT / "docs"
ARCHIVE = ROOT / "archive"
PROVENANCE = ROOT / "provenance"
TMP = ROOT / "tmp"

FROZEN_V5 = EXPERIMENTS / "2026-10-20_llm_v4_v5" / "v5"
MALRULELIB_REPO = EXTERNAL / "malrulelib_repo"
MALRULE_DESCRIPTIONS = LIBRARY / "malrule_descriptions.json"
ENV_PATH = ROOT / ".env"


def require(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(path)
    return path
