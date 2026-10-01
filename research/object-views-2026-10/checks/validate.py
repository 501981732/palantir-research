#!/usr/bin/env python3
"""Validate the local Object Views research deliverable; no network requests.

Run from any directory. Exit 0 means all checks passed, 1 means a deliverable
check failed, and 2 means the validator could not finish. Results use repository
relative paths. Pillow is optional for full image decoding; PNG/GIF dimensions
can also be checked with the standard library.
"""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
from urllib.parse import unquote, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

try:
    from PIL import Image
except ImportError:
    Image = None


TOPIC = Path(__file__).resolve().parents[1]
REPO = TOPIC.parents[1]
BASELINE = "70feed00b61f7572190b94741bfba9958a573486"
DIAGRAMS = ("01-object-entry", "02-explore-detail-act", "03-save-publish")
SOURCE_COVERAGE_FILES = (
    "README.md", "notes/explorer-flow.md", "notes/views-governance.md",
    "notes/workshop-boundaries.md", "notes/secondary-reading.md",
    "notes/media-evidence.md",
)
IMAGE_SUFFIXES = {".png", ".gif", ".jpg", ".jpeg", ".webp"}
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
REF_DEF = re.compile(r"^ {0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)")
PERSONAL_PATHS = (
    re.compile(r"(?<![\w:/])/(?:Users|home)/[^\s<>\"'`]+"),
    re.compile(r"(?<![\w:/])/(?:private/)?var/folders/[^\s<>\"'`]+"),
    re.compile(r"(?<![\w:/])(?:[A-Za-z]:\\Users\\)[^\s<>\"'`]+"),
)
SECRET_PATTERNS = (
    re.compile(r"\b(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\b(?:sk-proj-|sk-ant-|sk-|hf_)[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{24,}=*", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"[?&](?:access_token|api_key|apikey|secret|token)=[A-Za-z0-9._~-]{20,}", re.I),
)


class Report:
    def __init__(self, baseline: str):
        self.data = {
            "schema_version": 1,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "topic": relative(TOPIC),
            "baseline_commit": baseline,
            "scope": "Local deliverable integrity only; no network, tenant, or product-runtime tests",
            "checks": [],
            "limitations": [
                "Public source access is documented by research evidence, not rechecked by this script.",
                "SVG/PNG existence and safety do not independently prove visual quality or product behavior.",
                "Pattern-based privacy checks cannot guarantee discovery of every possible secret.",
            ],
        }

    def add(self, group: str, name: str, passed: bool, **details):
        self.data["checks"].append({
            "group": group, "check": name,
            "status": "passed" if passed else "failed", **details,
        })

    def finish(self):
        counts = Counter(check["status"] for check in self.data["checks"])
        self.data["summary"] = {
            "status": "passed" if not counts["failed"] else "failed",
            "checks": len(self.data["checks"]),
            "passed": counts["passed"], "failed": counts["failed"],
            "exit_status": 0 if not counts["failed"] else 1,
        }
        return self.data["summary"]["exit_status"]


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO).as_posix()
    except ValueError:
        return "outside-repository"


def safe_topic_file(name: str) -> Path | None:
    candidate = (TOPIC / name).resolve()
    try:
        candidate.relative_to(TOPIC)
    except ValueError:
        return None
    return candidate


def read_json(report: Report, path: Path, group: str):
    if not path.is_file():
        report.add(group, "required JSON exists", False, file=relative(path), reason="missing")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError, UnicodeError) as error:
        report.add(group, "JSON parses", False, file=relative(path), reason=type(error).__name__)
        return None
    report.add(group, "JSON parses", True, file=relative(path))
    return data


def without_fences(text: str):
    """Retain line positions while removing fenced code from link parsing."""
    lines = text.splitlines()
    output, open_fence, unclosed = [], None, []
    for number, line in enumerate(lines, 1):
        match = FENCE.match(line)
        if open_fence is None:
            if match:
                open_fence = (match.group(1)[0], len(match.group(1)), number)
                output.append("")
            else:
                output.append(line)
        else:
            if match and match.group(1)[0] == open_fence[0] and len(match.group(1)) >= open_fence[1] and not match.group(2).strip():
                open_fence = None
            output.append("")
    if open_fence:
        unclosed.append(open_fence[2])
    return "\n".join(output), unclosed


def markdown_links(text: str):
    """Read inline destinations and explicit/collapsed/shortcut references."""
    clean, _ = without_fences(text)
    clean = re.sub(r"(`+)(.*?)\1", lambda m: " " * len(m.group(0)), clean)
    definitions = {}
    links = []
    for number, line in enumerate(clean.splitlines(), 1):
        match = REF_DEF.match(line)
        if match:
            definitions[match.group(1).strip().casefold()] = match.group(2).strip("<>")
            links.append((number, match.group(2).strip("<>")))
        for attribute in re.finditer(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", line, re.I):
            links.append((number, attribute.group(1)))
        for autolink in re.finditer(r"<(https?://[^<>\s]+)>", line, re.I):
            links.append((number, autolink.group(1)))
    i = 0
    while i < len(clean):
        if clean[i] != "[" or (i and clean[i - 1] == "\\"):
            i += 1
            continue
        start = i
        depth, j = 1, i + 1
        while j < len(clean) and depth:
            if clean[j] == "\\":
                j += 2
                continue
            if clean[j] == "[":
                depth += 1
            elif clean[j] == "]":
                depth -= 1
            j += 1
        if depth:
            i += 1
            continue
        label = clean[i + 1:j - 1]
        number = clean.count("\n", 0, start) + 1
        if j < len(clean) and clean[j] == "(":
            k = j + 1
            while k < len(clean) and clean[k].isspace():
                k += 1
            if k < len(clean) and clean[k] == "<":
                end = clean.find(">", k + 1)
                if end >= 0:
                    links.append((number, clean[k + 1:end]))
                    i = end + 1
                    continue
            dest, nesting = [], 0
            while k < len(clean):
                char = clean[k]
                if char == "\\" and k + 1 < len(clean):
                    dest.append(clean[k + 1])
                    k += 2
                    continue
                if char == "(":
                    nesting += 1
                elif char == ")":
                    if not nesting:
                        break
                    nesting -= 1
                elif char.isspace() and not nesting:
                    break
                dest.append(char)
                k += 1
            if dest:
                links.append((number, "".join(dest)))
            i = max(k + 1, j)
        elif j < len(clean) and clean[j] == "[":
            end = clean.find("]", j + 1)
            if end >= 0:
                reference = (clean[j + 1:end] or label).strip().casefold()
                if reference in definitions:
                    links.append((number, definitions[reference]))
                i = end + 1
            else:
                i = j
        else:
            if label.strip().casefold() in definitions and not (j < len(clean) and clean[j] == ":"):
                links.append((number, definitions[label.strip().casefold()]))
            i = j
    return links


def heading_anchors(text: str):
    clean, _ = without_fences(text)
    anchors, seen = set(), Counter()
    for line in clean.splitlines():
        match = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = html.unescape(match.group(1)).lower()
        heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
        heading = re.sub(r"<[^>]+>", "", heading)
        heading = re.sub(r"[^\w\- ]", "", heading)
        slug = heading.strip().replace(" ", "-")
        index = seen[slug]
        seen[slug] += 1
        anchors.add(slug if not index else f"{slug}-{index}")
    anchors.update(re.findall(r"\b(?:id|name)=[\"']([^\"']+)[\"']", clean))
    return anchors


def check_markdown(report: Report):
    files = sorted(TOPIC.rglob("*.md")) + [REPO / "README.md", REPO / "research/README.md"]
    failures, fence_failures, link_count = [], [], 0
    anchors_cache = {}
    for path in files:
        text = path.read_text(encoding="utf-8")
        _, unclosed = without_fences(text)
        fence_failures.extend({"file": relative(path), "line": line} for line in unclosed)
        for number, destination in markdown_links(text):
            parsed = urlsplit(html.unescape(destination))
            if parsed.scheme or parsed.netloc:
                continue
            link_count += 1
            display_destination = destination if not parsed.path.startswith("/") else "[absolute destination redacted]"
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if not target.exists():
                failures.append({"file": relative(path), "line": number, "target": display_destination, "reason": "missing target"})
                continue
            if relative(target) == "outside-repository":
                failures.append({"file": relative(path), "line": number, "reason": "target outside repository"})
                continue
            if parsed.fragment:
                anchor_file = target / "README.md" if target.is_dir() else target
                if anchor_file.suffix.lower() == ".md" and anchor_file.exists():
                    if anchor_file not in anchors_cache:
                        anchors_cache[anchor_file] = heading_anchors(anchor_file.read_text(encoding="utf-8"))
                    if unquote(parsed.fragment) not in anchors_cache[anchor_file]:
                        failures.append({"file": relative(path), "line": number, "target": display_destination, "reason": "missing Markdown heading or explicit anchor"})
    report.add("markdown", "fenced blocks close", not fence_failures, markdown_files=len(files), failures=fence_failures)
    report.add("markdown", "local links and Markdown fragments resolve", not failures, local_links=link_count, failures=failures)


def normalized_source_url(url: str) -> str | None:
    """Match the same public page despite fragments and terminal slashes."""
    parsed = urlsplit(html.unescape(url))
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        return None
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path.rstrip("/"), parsed.query, ""))


def source_record_urls(record: dict):
    values = [record.get(key) for key in ("url", "source_url", "canonical_url")]
    for key in ("aliases", "urls"):
        if isinstance(record.get(key), list):
            values.extend(record[key])
    return {normalized for value in values if isinstance(value, str)
            if (normalized := normalized_source_url(value))}


def media_manifest_path():
    candidates = [TOPIC / "media-manifest.json", TOPIC / "notes/media-manifest.json", TOPIC / "assets/media-manifest.json"]
    return next((path for path in candidates if path.is_file()), candidates[1])


def check_source_coverage(report: Report, registered: set[str]):
    """Citations use the page registry; original media URLs use their manifest."""
    media_urls, media_pages, media_errors = set(), set(), []
    manifest = media_manifest_path()
    try:
        media = json.loads(manifest.read_text(encoding="utf-8"))
        originals = media.get("assets", []) if isinstance(media, dict) else []
    except (OSError, ValueError, UnicodeError):
        originals = []
        media_errors.append({"file": relative(manifest), "reason": "media source coverage unavailable"})
    for index, record in enumerate(originals):
        if not isinstance(record, dict):
            media_errors.append({"record": index, "reason": "media source is not an object"})
            continue
        for key, target in (("original_url", media_urls), ("source_page", media_pages)):
            value = record.get(key)
            normalized = normalized_source_url(value) if isinstance(value, str) else None
            if normalized:
                target.add(normalized)
            else:
                media_errors.append({"record": index, "field": key, "reason": "missing or invalid public source URL"})
    unregistered_media_pages = sorted(media_pages - registered)
    report.add("sources", "original media URLs are manifest-listed and source pages registered", not media_errors and not unregistered_media_pages,
               manifest=relative(manifest), original_assets=len(originals), original_urls=len(media_urls),
               unregistered_source_pages=unregistered_media_pages, failures=media_errors)
    missing, external_pages, media_references, references = [], set(), set(), 0
    for name in SOURCE_COVERAGE_FILES:
        path = TOPIC / name
        if not path.is_file():
            missing.append({"file": relative(path), "reason": "missing research body or appendix"})
            continue
        for number, destination in markdown_links(path.read_text(encoding="utf-8")):
            normalized = normalized_source_url(destination)
            if normalized is None:
                continue
            references += 1
            if normalized in media_urls:
                media_references.add(normalized)
            else:
                external_pages.add(normalized)
                if normalized not in registered:
                    missing.append({"file": relative(path), "line": number, "url": normalized, "reason": "external page not in source registry"})
    report.add("sources", "body and appendix external links have source coverage", not missing,
               markdown_files=[relative(TOPIC / name) for name in SOURCE_COVERAGE_FILES],
               external_references=references, unique_external_pages=len(external_pages),
               original_media_urls_referenced=len(media_references), failures=missing)


def check_sources(report: Report):
    candidates = [TOPIC / "sources.json", TOPIC / "checks/sources.json"]
    registry = next((path for path in candidates if path.is_file()), candidates[1])
    data = read_json(report, registry, "sources")
    if data is None:
        return
    records = data.get("sources") if isinstance(data, dict) else data
    if not isinstance(records, list) or not records:
        report.add("sources", "source registry contains records", False, reason="expected nonempty sources array")
        return
    errors, ids, registered = [], [], set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append({"record": index, "reason": "record is not an object"})
            continue
        if record.get("id"):
            ids.append(record["id"])
        urls = source_record_urls(record)
        if not urls:
            errors.append({"record": index, "reason": "missing or invalid public URL"})
        registered.update(urls)
    duplicates = [key for key, count in Counter(ids).items() if count > 1]
    report.add("sources", "source records have public URLs and unique IDs", not errors and not duplicates, sources=len(records), duplicate_ids=duplicates, failures=errors)
    check_source_coverage(report, registered)


def image_metadata(path: Path):
    if Image is not None:
        with Image.open(path) as image:
            meta = {"width": image.width, "height": image.height, "format": image.format, "frames": getattr(image, "n_frames", 1)}
            duration = 0
            for frame in range(meta["frames"]):
                image.seek(frame)
                image.load()
                duration += image.info.get("duration", 0)
            if meta["frames"] > 1:
                meta["animation_duration_ms"] = duration
            return meta
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", data[16:24])
        return {"width": width, "height": height, "format": "PNG"}
    if data[:6] in {b"GIF87a", b"GIF89a"}:
        width, height = struct.unpack("<HH", data[6:10])
        return {"width": width, "height": height, "format": "GIF"}
    raise ValueError("image format needs Pillow")


def artifact_metadata(path: Path):
    blob = path.read_bytes()
    meta = {"bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()}
    if path.suffix.lower() in IMAGE_SUFFIXES:
        meta.update(image_metadata(path))
    return meta


def check_manifest_records(report: Report, records: list, group: str):
    files, errors = set(), []
    for record in records:
        name = record.get("file") or record.get("path")
        if not isinstance(name, str):
            errors.append({"reason": "asset record has no relative file"})
            continue
        path = safe_topic_file(name)
        if path is None:
            errors.append({"reason": "asset path outside topic"})
            continue
        files.add(path)
        if not path.is_file():
            errors.append({"file": relative(path), "reason": "missing asset"})
            continue
        try:
            actual = artifact_metadata(path)
        except (OSError, ValueError, EOFError) as error:
            errors.append({"file": relative(path), "reason": type(error).__name__})
            continue
        required = ["bytes", "sha256"] + (["width", "height"] if path.suffix.lower() in IMAGE_SUFFIXES else [])
        missing_fields = []
        for key in required:
            if key not in record:
                missing_fields.append(key)
                errors.append({"file": relative(path), "field": key, "reason": "missing manifest metadata"})
        differences = {}
        for key in ("bytes", "sha256", "width", "height", "frames", "animation_duration_ms"):
            if key in record and key in actual and record[key] != actual[key]:
                differences[key] = {"expected": record[key], "actual": actual[key]}
        if differences:
            errors.append({"file": relative(path), "reason": "manifest mismatch", "differences": differences})
        elif not missing_fields:
            report.add(group, "asset matches bytes/hash/dimensions", True, file=relative(path), actual=actual)
        if record.get("source_asset"):
            source = safe_topic_file(record["source_asset"])
            if source is None or not source.is_file():
                errors.append({"file": relative(path), "reason": "derived source asset missing"})
    report.add(group, "manifest records validate", not errors, records=len(records), failures=errors)
    return files


def check_media(report: Report):
    manifest = media_manifest_path()
    data = read_json(report, manifest, "media")
    if data is None:
        return
    records = []
    if isinstance(data, dict):
        for key in ("assets", "derived_assets"):
            if isinstance(data.get(key), list):
                records.extend(data[key])
    if not records or not all(isinstance(record, dict) for record in records):
        report.add("media", "media manifest contains asset records", False)
        return
    declared = check_manifest_records(report, records, "media")
    actual = {path.resolve() for path in (TOPIC / "assets").glob("*") if path.suffix.lower() in IMAGE_SUFFIXES}
    undeclared = sorted(relative(path) for path in actual - declared)
    report.add("media", "all stored media images are declared", not undeclared, undeclared=undeclared)
    if Image is None:
        report.data["limitations"].append("Pillow unavailable: image header dimensions checked; full decoding/frame-count checks not performed.")


def svg_safety(path: Path):
    content = path.read_text(encoding="utf-8")
    errors = []
    if re.search(r"<!DOCTYPE|<!ENTITY", content, re.I):
        errors.append("DTD or entity declaration")
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return ["invalid XML"]
    if root.tag.rsplit("}", 1)[-1].lower() != "svg":
        errors.append("root is not SVG")
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1].lower()
        if tag in {"script", "foreignobject"}:
            errors.append(f"forbidden element: {tag}")
        for key, value in element.attrib.items():
            attribute = key.rsplit("}", 1)[-1].lower()
            if attribute.startswith("on"):
                errors.append("event handler attribute")
            if attribute in {"href", "src"} and value.strip() and not value.strip().startswith("#"):
                errors.append("nonlocal resource reference")
    for resource in re.findall(r"url\(\s*([^)]+)\)", content, re.I):
        if not resource.strip().strip("\"'").startswith("#"):
            errors.append("nonlocal CSS resource")
    if re.search(r"@import\b", content, re.I):
        errors.append("CSS import")
    return sorted(set(errors))


def nested_file_records(value):
    records = []
    if isinstance(value, list):
        for item in value:
            records.extend(nested_file_records(item))
    elif isinstance(value, dict):
        if isinstance(value.get("file") or value.get("path"), str):
            records.append(value)
        else:
            for item in value.values():
                records.extend(nested_file_records(item))
    return records


def check_diagrams(report: Report):
    expected = {TOPIC / "diagrams" / f"{stem}.{suffix}" for stem in DIAGRAMS for suffix in ("mmd", "svg", "png")}
    for path in sorted(expected):
        report.add("diagrams", "diagram source/render exists", path.is_file() and path.stat().st_size > 0, file=relative(path))
        if path.is_file() and path.suffix == ".svg":
            errors = svg_safety(path)
            report.add("diagrams", "SVG has no script/foreignObject/external resource", not errors, file=relative(path), failures=errors)
        if path.is_file() and path.suffix == ".png":
            try:
                meta = image_metadata(path)
                report.add("diagrams", "PNG decodes with positive dimensions", meta["width"] > 0 and meta["height"] > 0, file=relative(path), actual=meta)
            except (OSError, ValueError, EOFError) as error:
                report.add("diagrams", "PNG decodes with positive dimensions", False, file=relative(path), reason=type(error).__name__)
    data = read_json(report, TOPIC / "diagrams/manifest.json", "diagrams")
    if data is None:
        return
    records = nested_file_records(data)
    if not records:
        report.add("diagrams", "diagram manifest contains file records", False)
        return
    declared = check_manifest_records(report, records, "diagrams")
    actual = {path.resolve() for path in (TOPIC / "diagrams").glob("*") if path.suffix in {".mmd", ".svg", ".png"}}
    undeclared = sorted(relative(path) for path in actual - declared)
    report.add("diagrams", "all diagram sources/renders are declared", not undeclared, undeclared=undeclared)


def check_privacy(report: Report):
    paths = [path for path in TOPIC.rglob("*") if path.is_file() and path.suffix in {".md", ".json", ".mmd", ".svg"} and path != TOPIC / "checks/results.json"]
    paths.extend([REPO / "README.md", REPO / "research/README.md"])
    private, secrets = [], []
    for path in sorted(paths):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(pattern.search(line) for pattern in PERSONAL_PATHS):
                private.append({"file": relative(path), "line": number})
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                secrets.append({"file": relative(path), "line": number})
    report.add("privacy", "no personal absolute paths in text deliverables", not private, text_files=len(paths), failures=private)
    report.add("privacy", "no sensitive credential patterns in text deliverables", not secrets, failures=secrets)


def indexed_topics(text: str):
    topics = set()
    for _, destination in markdown_links(text):
        path = urlsplit(destination).path.strip("/")
        match = re.fullmatch(r"(?:research/)?([a-z0-9-]+-\d{4}-\d{2})(?:/README\.md)?", path)
        if match:
            topics.add(match.group(1))
    return topics


def check_indexes(report: Report, baseline: str):
    originals, error = {}, None
    for name in ("README.md", "research/README.md"):
        result = subprocess.run(["git", "show", f"{baseline}:{name}"], cwd=REPO, text=True, capture_output=True)
        if result.returncode:
            error = "baseline index unavailable"
        else:
            originals[name] = indexed_topics(result.stdout)
    report.add("indexes", "main-baseline indexes available", error is None, reason=error)
    required = {"workshop-runtime-2026-10", "object-views-2026-10"}
    for topics in originals.values():
        required.update(topics)
    for name in ("README.md", "research/README.md"):
        current = indexed_topics((REPO / name).read_text(encoding="utf-8"))
        missing = sorted(required - current)
        report.add("indexes", "preserves all baseline topics plus Workshop Runtime/Object Views", not missing, file=name, required_topics=sorted(required), current_topics=sorted(current), missing_topics=missing)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-ref", default=BASELINE, help="Reviewed main baseline used to preserve topic indexes")
    args = parser.parse_args()
    report = Report(args.baseline_ref)
    output = TOPIC / "checks/results.json"
    try:
        check_markdown(report)
        check_sources(report)
        check_media(report)
        check_diagrams(report)
        check_privacy(report)
        check_indexes(report, args.baseline_ref)
        status = report.finish()
    except Exception as error:
        report.data["summary"] = {"status": "validator_error", "exit_status": 2, "error_type": type(error).__name__}
        status = 2
    output.write_text(json.dumps(report.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = report.data["summary"]
    print(json.dumps({"results": relative(output), **summary}, ensure_ascii=False))
    for check in report.data["checks"]:
        if check["status"] == "failed":
            print(json.dumps(check, ensure_ascii=False))
    return status


if __name__ == "__main__":
    sys.exit(main())
