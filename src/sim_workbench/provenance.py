from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .paths import ROOT


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, root: Path = ROOT) -> dict[str, Any]:
    path = path.resolve()
    try:
        rel = path.relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = str(path)
    return {
        "path": rel,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def snapshot(paths: Iterable[Path], root: Path = ROOT) -> list[dict[str, Any]]:
    return [file_record(path, root) for path in paths if path.is_file()]


def write_manifest(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "platform": platform.platform(),
        **payload,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest
