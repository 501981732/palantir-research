#!/usr/bin/env python3
"""Retrieve bounded official npm evidence; do not install or execute package code."""
import base64
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
import tempfile
from datetime import datetime, timezone
from urllib.request import urlopen, Request

OUT = Path(__file__).parent
PACKAGES = ["@osdk/widget.api", "@osdk/widget.client"]
parser = argparse.ArgumentParser()
parser.add_argument("--version", help="Download this exact stable version; omit to audit latest stable.")
parser.add_argument("--artifacts-dir", type=Path, default=Path(tempfile.gettempdir()) / "palantir-custom-widgets-npm", help="Directory for downloaded and extracted artifacts; not persisted in public evidence.")
args = parser.parse_args()
record = {"retrievedAt": datetime.now(timezone.utc).isoformat(), "registry": "https://registry.npmjs.org", "packages": []}
scratch = args.artifacts_dir
scratch.mkdir(parents=True, exist_ok=True)
for name in PACKAGES:
    url = "https://registry.npmjs.org/" + name.replace("/", "%2f")
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "source-led-research/1.0"})
    with urlopen(req, timeout=40) as response:
        raw = response.read()
        headers = dict(response.headers.items())
    metadata = json.loads(raw)
    stable = [v for v in metadata["versions"] if re.fullmatch(r"\d+\.\d+\.\d+", v)]
    latest_stable = max(stable, key=lambda v: tuple(map(int, v.split("."))))
    latest_published = max(stable, key=lambda v: metadata["time"].get(v, ""))
    selected_version_number = args.version or latest_stable
    if selected_version_number not in stable:
        raise ValueError("Requested version is not present as a stable version: " + selected_version_number)
    version = metadata["versions"][selected_version_number]
    dist = version["dist"]
    with urlopen(Request(dist["tarball"], headers={"User-Agent": "source-led-research/1.0"}), timeout=40) as response:
        tarball = response.read()
    integrity_algorithm, integrity_value = dist["integrity"].split("-", 1)
    calculated_integrity = base64.b64encode(hashlib.new(integrity_algorithm, tarball).digest()).decode()
    extraction_dir = scratch / name.split("/")[1]
    extraction_dir.mkdir(parents=True, exist_ok=True)
    inventory = []
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            p = Path(member.name)
            if p.is_absolute() or ".." in p.parts:
                raise ValueError("Unsafe package path: " + member.name)
            body = archive.extractfile(member).read()
            target = extraction_dir / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            inventory.append({"path": member.name, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()})
    selected_version = {k: version[k] for k in ["name", "version", "description", "license", "repository", "homepage", "bugs", "main", "module", "types", "exports", "files", "sideEffects", "engines", "dependencies", "peerDependencies", "peerDependenciesMeta", "gitHead", "_npmVersion", "_nodeVersion", "dist"] if k in version}
    entry = {
        "name": name,
        "metadataUrl": url,
        "metadataSha256": hashlib.sha256(raw).hexdigest(),
        "responseHeaders": {k: v for k, v in headers.items() if k.lower() in {"date", "etag", "last-modified", "content-type"}},
        "distTags": metadata.get("dist-tags"),
        "latestStableBySemver": latest_stable,
        "latestStableByPublishTime": latest_published,
        "selectedVersionPublishedAt": metadata["time"][selected_version_number],
        "recentStableVersions": [{"version": v, "publishedAt": metadata["time"].get(v)} for v in sorted(stable, key=lambda v: metadata["time"].get(v, ""), reverse=True)[:20]],
        "selectedVersionMetadata": selected_version,
        "tarballVerification": {"bytes": len(tarball), "sha256": hashlib.sha256(tarball).hexdigest(), "computedSha1": hashlib.sha1(tarball).hexdigest(), "registrySha1": dist["shasum"], "sha1Matches": hashlib.sha1(tarball).hexdigest() == dist["shasum"], "computedIntegrity": integrity_algorithm + "-" + calculated_integrity, "registryIntegrity": dist["integrity"], "integrityMatches": calculated_integrity == integrity_value},
        "fileCount": len(inventory),
        "packageSubdirectory": name.split("/")[1],
        "files": inventory,
    }
    record["packages"].append(entry)
record["completedAt"] = datetime.now(timezone.utc).isoformat()
(OUT / "protocol-npm-audit.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"evidence": "protocol-npm-audit.json", "packages": [{"name": p["name"], "version": p["selectedVersionMetadata"]["version"], "publishedAt": p["selectedVersionPublishedAt"], "files": p["fileCount"], "sha1Matches": p["tarballVerification"]["sha1Matches"], "integrityMatches": p["tarballVerification"]["integrityMatches"], "gitHead": p["selectedVersionMetadata"].get("gitHead")} for p in record["packages"]]}, ensure_ascii=False, indent=2))
