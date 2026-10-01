"""Read public npm metadata/tarball in memory; retain only audit facts.

Usage: python3 lineage-inspect-npm.py --date 2026-10-01
No token, tenant, source redistribution or package execution is needed.
"""

import argparse
import base64
import hashlib
import io
import json
import tarfile
import urllib.request
from pathlib import Path


def read_json(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


parser = argparse.ArgumentParser()
parser.add_argument("--date", required=True, help="UTC retrieval date")
args = parser.parse_args()
url = "https://registry.npmjs.org/@osdk%2Fworkshop-iframe-custom-widget"
metadata = read_json(url)
version = metadata["dist-tags"]["latest"]
published = metadata["versions"][version]
with urllib.request.urlopen(published["dist"]["tarball"], timeout=30) as response:
    data = response.read()
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
    suffixes = (
        "internal/messages.d.ts", "internal/messages.js",
        "internal/variableTypeWithDefaultValue.d.ts",
        "useWorkshopContext.js", "utils.js",
    )
    names = [name for name in archive.getnames() if name.endswith(suffixes)]
    contents = [archive.extractfile(name).read().decode() for name in names]
symbols = (
    "temporaryObjectSetRid", "react-app-sending-config",
    "workshop-accepted-config", "workshop-rejected-config",
    "workshop-requesting-config", "workshop-value-change",
    "react-app-set-auto-max-height", "event.source !== window.parent",
    'window.parent.postMessage(message, "*")',
)
faux = read_json("https://registry.npmjs.org/@osdk%2Ffaux")
result = {
    "retrievedAt": args.date,
    "source": url,
    "version": version,
    "publishedAt": metadata["time"][version],
    "gitHead": published.get("gitHead"),
    "distTags": metadata["dist-tags"],
    "tarballUrl": published["dist"]["tarball"],
    "bytes": len(data),
    "sha256": hashlib.sha256(data).hexdigest(),
    "npmIntegrity": published["dist"]["integrity"],
    "integrityVerified": (
        "sha512-" + base64.b64encode(hashlib.sha512(data).digest()).decode()
        == published["dist"]["integrity"]
    ),
    "license": published.get("license"),
    "inspectedFiles": names,
    "observedSymbols": {
        symbol: any(symbol in content for content in contents)
        for symbol in symbols
    },
    "boundary": (
        "Published package inspection only. No authenticated Workshop host was run. "
        "Tarball read in memory; source files not redistributed."
    ),
    "fauxObjectSetRelease": {
        "source": "https://registry.npmjs.org/@osdk%2Ffaux",
        "version": "0.23.0",
        "publishedAt": faux["time"].get("0.23.0"),
        "gitHead": faux["versions"].get("0.23.0", {}).get("gitHead"),
        "changelogCommit": "58922c122b7c5c7624d30c74232826c1d534e52f",
    },
}
output = Path(__file__).with_name("lineage-npm-legacy.json")
output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({
    "output": str(output), "version": version,
    "integrityVerified": result["integrityVerified"],
    "allObservedSymbols": all(result["observedSymbols"].values()),
}, indent=2))
