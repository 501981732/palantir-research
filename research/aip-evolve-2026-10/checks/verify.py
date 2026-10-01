#!/usr/bin/env python3
"""Verify the research package locally; does not perform network requests."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    failures = []
    links = 0
    urls = set()
    for file in sorted(root.rglob("*.md")):
        text = file.read_text(encoding="utf-8")
        if re.search(r"/Users/|file://|source_thread_id|ghp_[A-Za-z0-9]+", text):
            failures.append(f"Forbidden local path or credential pattern: {file.relative_to(root)}")
        for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
            if target.startswith(("https://", "http://")):
                if file.name not in ("sources.md", "assets.md", "checks.md"):
                    urls.add(target)
                continue
            path = unquote(target.split("#", 1)[0])
            if path:
                links += 1
                if not (file.parent / path).exists():
                    failures.append(f"Missing relative target: {file.relative_to(root)} -> {target}")
    ledger = (root / "sources.md").read_text(encoding="utf-8")
    for url in sorted(urls):
        # A timestamp/anchor variant can share the canonical source entry.
        base = url.split("#", 1)[0]
        if "youtube.com/watch?" in base:
            base = base.split("&", 1)[0]
        if base not in ledger:
            failures.append(f"Citation missing from source ledger: {url}")
    images = []
    asset_ledger = (root / "assets.md").read_text(encoding="utf-8")
    for folder in (root / "assets", root / "diagrams"):
        for file in sorted(folder.iterdir()):
            if file.suffix not in (".png", ".jpg", ".svg", ".dot"):
                continue
            content = file.read_bytes()
            item = {"file": str(file.relative_to(root)), "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest()}
            if file.suffix in (".jpg", ".png"):
                with Image.open(file) as im:
                    im.verify()
                with Image.open(file) as im:
                    item["dimensions"] = list(im.size)
            if item["sha256"] not in asset_ledger:
                failures.append(f"Hash missing from asset ledger: {item['file']}")
            images.append(item)
    manifest = json.loads((root / "diagrams/manifest.json").read_text())
    for item in manifest["files"]:
        file = root / "diagrams" / item["file"]
        content = file.read_bytes()
        if len(content) != item["bytes"] or hashlib.sha256(content).hexdigest() != item["sha256"]:
            failures.append(f"Diagram manifest mismatch: {item['file']}")
    responses = json.loads((root / "checks/public-link-responses.json").read_text())
    checked = {item["url"]: item for item in responses}
    primary = {url.split("#", 1)[0] for url in urls
               if "palantir.com/docs/" in url or "community.palantir.com/" in url}
    for url in sorted(primary):
        if url not in checked or checked[url].get("status") != 200:
            failures.append(f"Primary document missing successful recorded fetch: {url}")
    result = {"check_date_utc": "2026-10-01", "relative_links_checked": links,
              "cited_url_variants": len(urls), "primary_urls_covered": len(primary),
              "stored_media_and_diagram_sources": images, "failures": failures}
    (root / "checks/package-validation.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items()
                      if key != "stored_media_and_diagram_sources"}, ensure_ascii=False))
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
