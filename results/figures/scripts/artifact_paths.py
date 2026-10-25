"""Keep manuscript previews, publication exports and QA records separate."""
from pathlib import Path


def artifact_path(base, suffix):
    """Return the output path without changing the artifact's filename."""
    base = Path(base)
    if suffix == ".png":
        directory = base.parent
    elif suffix in {".pdf", ".svg", ".tiff"}:
        directory = base.parent / "exports"
    elif suffix in {".alignment.json", ".alignment.svg", ".pdf.collision-audit.json"}:
        directory = base.parent / "qa"
    else:
        raise ValueError(f"Unsupported artifact suffix: {suffix}")
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory / (base.name + suffix))
