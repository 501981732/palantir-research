#!/usr/bin/env python3
"""Compare npm sourcemap embedded sources with pinned official GitHub sources."""
import concurrent.futures
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import tempfile
from urllib.request import Request, urlopen

OUT = Path(__file__).parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--artifacts-dir", type=Path, default=Path(tempfile.gettempdir()) / "palantir-custom-widgets-npm")
parser.add_argument("--sources-dir", type=Path, default=Path(tempfile.gettempdir()) / "palantir-custom-widgets-source")
args = parser.parse_args()
AUDIT = json.loads((OUT / "protocol-npm-audit.json").read_text())
NPM_VERSION = AUDIT["packages"][0]["selectedVersionMetadata"]["version"]
COMMITS = ["fb8ec172d540ef7819382ff036aa2a692614af75", "e53b94ecd5de7cdd7e864d0daa04363bdad4db4c", "37cfd38676bf04edaef5847e929d914ea214c149"]
scratch = args.sources_dir
scratch.mkdir(parents=True, exist_ok=True)
jobs = []
for package in AUDIT["packages"]:
    package_name = package["name"].split("/")[1]
    package_root = args.artifacts_dir / package["packageSubdirectory"] / "package"
    for source_map_path in sorted((package_root / "build/browser").rglob("*.js.map")):
        source_map = json.loads(source_map_path.read_text())
        for source, embedded in zip(source_map["sources"], source_map["sourcesContent"]):
            relative_path = source_map_path.relative_to(package_root / "build/browser").parent / source
            repo_path = "packages/" + package_name + "/src/" + relative_path.as_posix()
            for commit in COMMITS:
                jobs.append((package_name, commit, repo_path, str(source_map_path.relative_to(package_root)), embedded))
    for commit in COMMITS:
        jobs.append((package_name, commit, "packages/" + package_name + "/package.json", None, None))

def fetch_compare(job):
    package_name, commit, repo_path, source_map_file, embedded = job
    url = "https://raw.githubusercontent.com/palantir/osdk-ts/" + commit + "/" + repo_path
    with urlopen(Request(url, headers={"User-Agent": "source-led-research/1.0"}), timeout=40) as response:
        raw = response.read()
    text = raw.decode()
    target = scratch / commit / repo_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    row = {"package": package_name, "commit": commit, "repoPath": repo_path, "sourceUrl": url, "sourceSha256": hashlib.sha256(raw).hexdigest(), "sourceBytes": len(raw), "sourceMapPath": source_map_file}
    if embedded is not None:
        row.update({"sourceMapEmbeddedSha256": hashlib.sha256(embedded.encode()).hexdigest(), "sourceMapEmbeddedBytes": len(embedded.encode()), "exactlyEqual": text == embedded})
        if text != embedded:
            row["unifiedDiffSourceToNpmEmbedded"] = "\n".join(difflib.unified_diff(text.splitlines(), embedded.splitlines(), fromfile=commit + ":" + repo_path, tofile="npm-" + NPM_VERSION + ":" + repo_path, lineterm=""))
    else:
        meta = json.loads(text)
        row.update({"sourceManifestVersion": meta["version"], "sourceManifestDependencies": meta.get("dependencies"), "sourceManifestExports": meta.get("exports")})
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    rows = list(pool.map(fetch_compare, jobs))
result = {"retrievedAt": datetime.now(timezone.utc).isoformat(), "npmVersion": NPM_VERSION, "method": "Exact UTF-8 byte/text comparison of published browser JS sourcemap sourcesContent to pinned raw GitHub TypeScript files; does not establish provenance attestation or closed-source host behavior.", "commits": COMMITS, "files": rows}
(OUT / "protocol-npm-source-compare.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"evidence": "protocol-npm-source-compare.json", "summary": [{"commit": c, "package": p, "exactMatches": sum(r.get("exactlyEqual") is True for r in rows if r["commit"] == c and r["package"] == p), "sourceMapsCompared": sum(r["sourceMapPath"] is not None for r in rows if r["commit"] == c and r["package"] == p), "manifestVersion": next(r["sourceManifestVersion"] for r in rows if r["commit"] == c and r["package"] == p and r["sourceMapPath"] is None)} for c in COMMITS for p in ["widget.api", "widget.client"]]}, ensure_ascii=False, indent=2))
