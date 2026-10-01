#!/usr/bin/env python3
"""Check local review-pack links, JSON, media hashes, and existing-topic preservation."""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOPIC = Path(__file__).resolve().parents[1]
ROOT = TOPIC.parents[1]

def slug(text):
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")

def anchors(path):
    text = path.read_text()
    found = set(re.findall(r'<a\s+id=[\"\']([^\"\']+)', text))
    counts = {}
    for title in re.findall(r"^#{1,6}\s+(.+)$", text, re.M):
        s = slug(title)
        n = counts.get(s, 0)
        counts[s] = n + 1
        found.add(s if n == 0 else f"{s}-{n}")
    return found

def main():
    failures = []
    local_links = 0
    checked_anchors = 0
    external = set()
    markdown = sorted(p for p in TOPIC.rglob("*.md") if not any(part in {"node_modules", "dist", ".vite"} for part in p.parts))
    for path in markdown:
        text = path.read_text()
        targets = re.findall(r"\]\(([^\n]+?)\)", text)
        targets += re.findall(r"^\[[^\]]+\]:\s*(\S+)", text, re.M)
        for target in targets:
            target = target.strip().split(' "')[0].strip("<>")
            if target.startswith(("http://", "https://")):
                external.add(target)
                continue
            if target.startswith(("mailto:", "data:")):
                continue
            parts = urlsplit(target)
            resolved = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            if resolved.is_dir():
                resolved /= "README.md"
            local_links += 1
            if not resolved.exists():
                failures.append({"file": str(path.relative_to(ROOT)), "target": target, "error": "missing local target"})
            elif parts.fragment and resolved.suffix == ".md":
                checked_anchors += 1
                if unquote(parts.fragment) not in anchors(resolved):
                    failures.append({"file": str(path.relative_to(ROOT)), "target": target, "error": "missing heading/anchor"})
    json_count = 0
    for p in TOPIC.rglob("*.json"):
        if "node_modules" in p.parts:
            continue
        try:
            json.loads(p.read_text())
            json_count += 1
        except Exception as e:
            failures.append({"file": str(p.relative_to(ROOT)), "error": str(e)})
    manifest = TOPIC / "evidence/media-assets-manifest.json"
    media_checks = []
    if manifest.exists():
        for asset in json.loads(manifest.read_text()):
            path = TOPIC / "assets" / asset["file"]
            ok = path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == asset["sha256"] and path.stat().st_size == asset["byte_size"]
            media_checks.append({"file": asset["file"], "hash_and_bytes_match": ok, "visual_review": asset.get("visual_review")})
            if not ok:
                failures.append({"file": asset["file"], "error": "asset hash/bytes mismatch"})
    existing = ["research/superrepo-2026-08", "research/pilot-2026-09", "research/osdk-react-components-2026-09", "research/osdk-typescript-2026-09", "research/ai-fde-2026-10"]
    changes = subprocess.check_output(["git", "diff", "--name-only", "origin/main", "--", *existing], cwd=ROOT, text=True).splitlines()
    if changes:
        failures.append({"error": "existing topics changed", "files": changes})
    result = {"checked_at": datetime.now(timezone.utc).isoformat(), "base_commit": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=ROOT, text=True).strip(), "scope": "Local assembly only; external URL reachability and real host behavior are separate evidence.", "markdown_files": len(markdown), "local_links_checked": local_links, "local_anchors_checked": checked_anchors, "json_files_parsed": json_count, "external_urls_discovered": len(external), "media_checks": media_checks, "existing_topics_unchanged": not changes, "failures": failures, "all_pass": not failures}
    (TOPIC / "evidence/assembly-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (TOPIC / "evidence/external-url-inventory.json").write_text(json.dumps(sorted(external), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "media_checks"}, ensure_ascii=False, indent=2))
    return bool(failures)

if __name__ == "__main__":
    sys.exit(main())
