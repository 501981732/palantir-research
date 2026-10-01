#!/usr/bin/env python3
"""Save bounded, decoded official npm provenance. Signature validation is not claimed."""
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).parent
audit = json.loads((OUT / "protocol-npm-audit.json").read_text())
result = {"retrievedAt": datetime.now(timezone.utc).isoformat(), "verificationBoundary": "Registry URL retrieved over HTTPS; payload decoded and subject hash compared. Sigstore certificate, DSSE signature and Rekor inclusion proofs were not cryptographically validated by this script.", "packages": []}
for package in audit["packages"]:
    url = package["selectedVersionMetadata"]["dist"]["attestations"]["url"]
    with urlopen(Request(url, headers={"User-Agent": "source-led-research/1.0"}), timeout=40) as response:
        raw = response.read()
    attestation = json.loads(raw)
    decoded = []
    for item in attestation["attestations"]:
        bundle = item["bundle"]
        envelope = bundle["dsseEnvelope"]
        payload = base64.b64decode(envelope["payload"])
        predicate = json.loads(payload)
        decoded.append({"predicateType": item.get("predicateType"), "payloadType": envelope["payloadType"], "statement": predicate, "payloadSha256": hashlib.sha256(payload).hexdigest(), "sha512SubjectMatchesTarball": any(s.get("digest", {}).get("sha512") == base64.b64decode(package["tarballVerification"]["registryIntegrity"].split("-", 1)[1]).hex() for s in predicate.get("subject", []))})
    result["packages"].append({"name": package["name"], "version": package["selectedVersionMetadata"]["version"], "sourceUrl": url, "responseBytes": len(raw), "responseSha256": hashlib.sha256(raw).hexdigest(), "decodedAttestations": decoded})
(OUT / "protocol-npm-provenance.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
