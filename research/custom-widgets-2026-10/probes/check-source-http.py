#!/usr/bin/env python3
"""Harmless public source reachability checks. Does not download source bodies."""
import concurrent.futures
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urldefrag, urlsplit

TOPIC = Path(__file__).resolve().parents[1]
urls = json.loads((TOPIC / "evidence/external-url-inventory.json").read_text())
urls = sorted({urldefrag(u)[0] for u in urls if urlsplit(u).hostname in {
    "www.palantir.com", "palantir.com", "github.com", "raw.githubusercontent.com", "registry.npmjs.org", "community.palantir.com", "www.youtube.com"
}})

def check(url):
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "Research-source-link-check/1.0"})
        with urlopen(req, timeout=15) as response:
            return {"url": url, "status": response.status, "final_url": response.url, "method": "HEAD"}
    except HTTPError as e:
        return {"url": url, "status": e.code, "final_url": e.url, "method": "HEAD", "note": "An HTTP refusal is recorded, not bypassed."}
    except Exception as e:
        return {"url": url, "status": None, "method": "HEAD", "error": str(e)[:250]}

previous_path = TOPIC / "evidence/http-checks.json"
previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
previous_results = {row["url"]: row for row in previous.get("results", [])}
new_urls = [url for url in urls if url not in previous_results]
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    new_results = list(executor.map(check, new_urls))
new_results_map = {row["url"]: row for row in new_results}
results = [new_results_map[url] if url in new_results_map else previous_results[url] for url in urls]
output = {"checked_at": datetime.now(timezone.utc).isoformat(), "boundary": "Public HEAD reachability; status 200 does not prove content claims, anchors, playback or tenant capabilities.", "url_count": len(results), "results": results}
(TOPIC / "evidence/http-checks.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"total_checked": len(results), "new_checks": len(new_urls), "non_2xx": [r for r in results if not isinstance(r["status"], int) or not 200 <= r["status"] < 300]}, ensure_ascii=False, indent=2))
