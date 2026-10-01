#!/usr/bin/env python3
"""Check public links in this topic, without cookies, auth, or transport retries.

HEAD is requested first. GET is requested once per page only when HEAD succeeds
or the server explicitly disallows HEAD (405/501). HTML is sampled, not archived.
An HTTP 200 response is transport evidence, not proof of reading an entire page
or watching a video. Earlier source-registry access observations are kept apart.
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import html
import json
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urlsplit, urlunsplit
from urllib.request import Request, build_opener


INPUTS = (
    "README.md",
    "notes/explorer-flow.md",
    "notes/media-evidence.md",
    "notes/secondary-reading.md",
    "notes/views-governance.md",
    "notes/workshop-boundaries.md",
)
EXCLUDED_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif", ".ico",
    ".mp4", ".mov", ".webm", ".m4v", ".m3u8", ".mp3", ".wav",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".wasm", ".pdf",
}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(<?https?://[^\s)]+>?)\s*\)")
AUTOLINK_RE = re.compile(r"<(https?://[^<>\s]+)>")
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
HEADERS = {
    "User-Agent": "PalantirResearch-LinkCheck/1.0",
    "Accept": "text/html,application/xhtml+xml,text/plain;q=0.9,*/*;q=0.1",
    "Accept-Encoding": "identity",
}


def page_key(url: str) -> str:
    """Drop only fragment and equivalent trailing slash; preserve the query."""
    parts = urlsplit(urldefrag(url)[0])
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                      parts.path.rstrip("/") or "/", parts.query, ""))


def collect_inputs(root: Path) -> tuple[dict, list, list]:
    pages, exclusions, manifests = {}, [], []
    for relative in INPUTS:
        path = root / relative
        text = path.read_text(encoding="utf-8")
        manifests.append({"file": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        matches = [(m.start(), m.group(1).strip("<>")) for m in LINK_RE.finditer(text)]
        matches.extend((m.start(), m.group(1)) for m in AUTOLINK_RE.finditer(text))
        for offset, url in matches:
            reference = {"file": relative, "line": text.count("\n", 0, offset) + 1,
                         "url": url, "fragment": urlsplit(url).fragment or None}
            suffix = Path(urlsplit(url).path).suffix.lower()
            if suffix in EXCLUDED_SUFFIXES:
                exclusions.append({**reference, "reason": "binary-media-or-large-file"})
                continue
            key = page_key(url)
            page = pages.setdefault(key, {"page_key": key, "request_url": urldefrag(url)[0],
                                          "references": []})
            if reference not in page["references"]:
                page["references"].append(reference)
    return pages, exclusions, manifests


def read_prior_observations(root: Path) -> dict:
    observations = {}
    for path in sorted((root / "notes").glob("*sources.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        sources = data.get("sources", []) if isinstance(data, dict) else data
        if not isinstance(sources, list):
            continue
        for source in sources:
            if not isinstance(source, dict) or not source.get("url") or "access" not in source:
                continue
            observation = {"registry": path.relative_to(root).as_posix(),
                           "source_id": source.get("id"), "access_observation": source["access"],
                           "accessed_on": source.get("accessed_on") or
                           (data.get("retrieved_at") or data.get("retrieved_date") or
                            data.get("retrieval_date") if isinstance(data, dict) else None)}
            observations.setdefault(page_key(source["url"]), []).append(observation)
    return observations


def request_once(url: str, method: str, timeout: float, sample_limit: int) -> dict:
    start = time.monotonic()
    result = {"method": method, "requested_url": url}
    # No CookieProcessor or authentication handler is installed.
    opener = build_opener()
    try:
        response = opener.open(Request(url, headers=HEADERS, method=method), timeout=timeout)
    except HTTPError as error:
        response = error
    except (URLError, TimeoutError, OSError) as error:
        result.update({"status": None, "error_type": type(error).__name__,
                       "error": str(error), "elapsed_seconds": round(time.monotonic() - start, 3)})
        return result
    try:
        result.update({"status": response.code, "final_url": response.geturl(),
                       "content_type": response.headers.get("Content-Type"),
                       "content_length": response.headers.get("Content-Length")})
        if method == "GET":
            content_type = (result["content_type"] or "").lower()
            if content_type.startswith(("image/", "video/", "audio/")) or "application/pdf" in content_type:
                result["body_sample_skipped"] = "binary-content-type"
            else:
                body = response.read(sample_limit + 1)
                sample = body[:sample_limit]
                result.update({"bytes_sampled": len(sample), "sample_limit": sample_limit,
                               "body_complete": len(body) <= sample_limit,
                               "sample_sha256": hashlib.sha256(sample).hexdigest()})
                decoded = sample.decode("utf-8", errors="replace")
                title = TITLE_RE.search(decoded)
                result["page_title"] = html.unescape(re.sub(r"\s+", " ", title.group(1))).strip()[:300] if title else None
                result["html_sample_received"] = bool(title or re.search(r"<!doctype html|<html", decoded[:4096], re.I))
                result["content_observation"] = "bounded response sample; not a full-page review or video viewing"
    except (TimeoutError, OSError) as error:
        result.update({"body_error_type": type(error).__name__, "body_error": str(error)})
    finally:
        response.close()
    result["elapsed_seconds"] = round(time.monotonic() - start, 3)
    return result


def check_page(page: dict, timeout: float, sample_limit: int, observations: dict) -> dict:
    result = dict(page)
    result["prior_web_or_registry_evidence"] = observations.get(page["page_key"], [])
    head = request_once(page["request_url"], "HEAD", timeout, sample_limit)
    result["head"] = head
    status = head["status"]
    if status is not None and (200 <= status < 400 or status in {405, 501}):
        content_type = (head.get("content_type") or "").lower()
        if content_type.startswith(("image/", "video/", "audio/")) or "application/pdf" in content_type:
            result["get"] = None
            result["verdict"] = "head_only_binary_content"
            return result
        result["get"] = request_once(page["request_url"], "GET", timeout, sample_limit)
        status = result["get"]["status"]
    else:
        result["get"] = None
    if status is None:
        result["verdict"] = "transport_error"
    elif status in {401, 403, 429}:
        result["verdict"] = "http_access_limited"
    elif status in {404, 410}:
        result["verdict"] = "http_not_found"
    elif 200 <= status < 400:
        get = result["get"] or {}
        if get.get("body_error"):
            result["verdict"] = "http_success_body_read_incomplete"
        elif get.get("html_sample_received"):
            result["verdict"] = "http_success_html_sample"
        else:
            result["verdict"] = "http_success"
    else:
        result["verdict"] = "http_error"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--sample-limit", type=int, default=131072)
    args = parser.parse_args()
    if not 0 < args.timeout <= 15 or not 1 <= args.workers <= 4 or not 1 <= args.sample_limit <= 262144:
        parser.error("timeout must be <=15s, workers <=4, sample-limit <=262144 bytes")
    root = Path(__file__).resolve().parents[1]
    pages, exclusions, manifests = collect_inputs(root)
    observations = read_prior_observations(root)
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(check_page, p, args.timeout, args.sample_limit, observations): key
                   for key, p in pages.items()}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if len(results) % 10 == 0 or len(results) == len(pages) or not result['verdict'].startswith("http_success"):
                print(f"{len(results)}/{len(pages)} {result['verdict']} {result['request_url']}", flush=True)
    results.sort(key=lambda item: item["page_key"])
    verdicts = Counter(result["verdict"] for result in results)
    host_verdicts = {}
    for result in results:
        host = urlsplit(result["request_url"]).netloc
        host_verdicts.setdefault(host, Counter())[result["verdict"]] += 1
    output = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "Topic README and five research notes; direct Markdown URLs; queries preserved; fragments recorded, not requested",
        "policy": {"authentication": "none", "cookies": "none", "head_first": True,
                   "workers": args.workers, "per_request_timeout_seconds": args.timeout,
                   "get_sample_limit_bytes": args.sample_limit, "transport_retries": 0,
                   "get_policy": "one GET per page key after successful HEAD or HEAD 405/501; no GET after access denial or transport failure",
                   "interpretation": "HTTP success and a bounded HTML sample do not establish claim correctness, full-page reading, or video viewing; prior source observations are separate"},
        "input_snapshot": manifests,
        "summary": {"unique_pages": len(results), "references": sum(len(p["references"]) for p in results),
                    "fragment_references": sum(bool(r["fragment"]) for p in results for r in p["references"]),
                    "page_head_checks": len(results), "page_get_checks": sum(p["get"] is not None for p in results),
                    "excluded_media_references": len(exclusions), "verdict_counts": dict(sorted(verdicts.items())),
                    "host_verdict_counts": {host: dict(sorted(count.items())) for host, count in sorted(host_verdicts.items())}},
        "excluded_references": exclusions,
        "pages": results,
    }
    target = root / "checks" / "links.json"
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], ensure_ascii=False, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
