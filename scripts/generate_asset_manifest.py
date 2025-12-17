#!/usr/bin/env python3
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Folders we want to include in the manifest if they exist
CANDIDATE_DIRS = ["logo", "guides", "fonts"]

# File extensions we consider "assets/docs"
ALLOWED_EXTS = {
    ".svg", ".png", ".jpg", ".jpeg", ".webp", ".pdf",
    ".ttf", ".otf", ".woff", ".woff2",
    ".md"
}

def is_allowed(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ALLOWED_EXTS

def collect_files(base_dir: Path) -> list[dict]:
    items = []
    if not base_dir.exists():
        return items

    for p in sorted(base_dir.rglob("*")):
        if is_allowed(p):
            rel = p.relative_to(ROOT).as_posix()
            items.append({
                "path": rel,
                "ext": p.suffix.lower(),
                "bytes": p.stat().st_size,
            })
    return items

def main():
    data = {
        "schemaVersion": 1,
        "repo": "classes-crispy/brand-kit",
        "generatedFrom": str(ROOT.name),
        "items": [],
    }

    for d in CANDIDATE_DIRS:
        data["items"].extend(collect_files(ROOT / d))

    out_path = ROOT / "asset-manifest.json"
    out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"✅ Wrote {out_path}")

if __name__ == "__main__":
    main()
