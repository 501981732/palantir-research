#!/usr/bin/env python3
"""Read-only assembly checks; no tenant, transport or product behavior validation.

Run from any directory. Optional first argument is a fixed Git base; default
origin/main. Prints JSON, writes nothing. Local heading anchors use GitHub's
common slug rules plus explicit HTML anchors; this is not a Markdown renderer.
"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit

TOPIC = Path(__file__).resolve().parents[1]
REPO = TOPIC.parents[1]
BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=REPO, text=True).strip()


def anchors(path):
    body = path.read_text(encoding="utf-8")
    found = set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', body))
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", body, re.M):
        heading = re.sub(r"<[^>]+>", "", heading).lower().strip()
        slug = "".join(c for c in heading if c in " _-" or unicodedata.category(c)[0] in "LN")
        slug = slug.replace(" ", "-")
        n = counts.get(slug, 0)
        counts[slug] = n + 1
        found.add(slug if not n else f"{slug}-{n}")
    return found


link_errors = []
local_links = 0
markdown = [*sorted(TOPIC.glob("*.md")), REPO / "README.md", REPO / "research/README.md"]
for path in markdown:
    body = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", body))
    matches += list(re.finditer(r"^\[[^\]]+\]:\s*(\S+)", body, re.M))
    for match in matches:
        target = match.group(1).strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("//"):
            continue
        local_links += 1
        dest = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
        reason = None
        if not dest.exists():
            reason = "missing local target"
        elif parsed.fragment and dest.is_file() and dest.suffix == ".md" and unquote(parsed.fragment) not in anchors(dest):
            reason = "missing Markdown/HTML anchor"
        if reason:
            link_errors.append({"file": str(path.relative_to(REPO)), "line": body.count("\n", 0, match.start()) + 1, "target": target, "reason": reason})

json_errors = []
json_count = 0
for path in sorted((TOPIC / "evidence").glob("*.json")):
    json_count += 1
    try:
        json.loads(path.read_text())
    except (ValueError, OSError) as error:
        json_errors.append({"file": str(path.relative_to(REPO)), "error": str(error)})

media_errors = []
manifest = TOPIC / "evidence/media-assets-manifest.json"
assets = json.loads(manifest.read_text()) if manifest.exists() else []
for asset in assets:
    path = TOPIC / "assets" / asset["file"]
    if not path.is_file():
        media_errors.append({"file": asset["file"], "reason": "missing"})
        continue
    data = path.read_bytes()
    if len(data) != asset["byte_size"] or hashlib.sha256(data).hexdigest() != asset["sha256"]:
        media_errors.append({"file": asset["file"], "reason": "bytes/hash mismatch"})
    if asset.get("visual_review") != "passed":
        media_errors.append({"file": asset["file"], "reason": "no recorded visual review"})

base_sha = git("rev-parse", BASE)
tracked_changes = git("diff", "--name-only", base_sha, "--").splitlines()
untracked = git("ls-files", "--others", "--exclude-standard").splitlines()
allowed = lambda p: p in ("README.md", "research/README.md") or p.startswith("research/custom-widgets-2026-10/")
unexpected = [p for p in [*tracked_changes, *untracked] if not allowed(p)]
old_topics = ["superrepo-2026-08", "pilot-2026-09", "osdk-react-components-2026-09", "osdk-typescript-2026-09", "ai-fde-2026-10"]
old_changes = git("diff", "--name-only", base_sha, "--", *(f"research/{p}" for p in old_topics)).splitlines()
tracked_old_files = git("ls-tree", "-r", "--name-only", base_sha, "--", *(f"research/{p}" for p in old_topics)).splitlines()

summary = {
    "scope": "Read-only document assembly, evidence integrity and Git preservation; not Workshop acceptance.",
    "base": base_sha,
    "markdown_files_checked": len(markdown),
    "local_links_checked": local_links,
    "link_errors": link_errors,
    "evidence_json_checked": json_count,
    "json_errors": json_errors,
    "media_assets_checked": len(assets),
    "media_errors": media_errors,
    "existing_topic_files_at_base": len(tracked_old_files),
    "existing_topics_changed": old_changes,
    "tracked_changes": tracked_changes,
    "unexpected_changes": unexpected,
    "dependency_directory_candidates": [p for p in untracked if "/node_modules/" in p],
}
summary["pass"] = not any([link_errors, json_errors, media_errors, old_changes, unexpected, summary["dependency_directory_candidates"]])
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(0 if summary["pass"] else 1)
