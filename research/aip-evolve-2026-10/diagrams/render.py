#!/usr/bin/env python3
"""Render and inventory the source-led conceptual diagrams in this directory."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image


def main() -> None:
    directory = Path(__file__).resolve().parent
    renderer = subprocess.run(
        ["dot", "-V"], capture_output=True, text=True, check=True
    ).stderr.strip()
    entries = []
    for source in sorted(directory.glob("*.dot")):
        for file_format in ("svg", "png"):
            target = source.with_suffix(f".{file_format}")
            result = subprocess.run(
                ["dot", f"-T{file_format}", str(source), "-o", str(target)],
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stderr:
                raise RuntimeError(f"{source.name}: {result.stderr.strip()}")
        for target in (source, source.with_suffix(".svg"), source.with_suffix(".png")):
            data = target.read_bytes()
            entry = {
                "file": target.name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            if target.suffix == ".png":
                with Image.open(target) as picture:
                    picture.verify()
                with Image.open(target) as picture:
                    entry["dimensions"] = list(picture.size)
                    entry["mode"] = picture.mode
            entries.append(entry)
    manifest = {
        "created": "2026-10-01",
        "kind": "Original conceptual diagrams; not official internal architecture",
        "renderer": renderer,
        "font": "PingFang SC",
        "files": entries,
    }
    (directory / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
