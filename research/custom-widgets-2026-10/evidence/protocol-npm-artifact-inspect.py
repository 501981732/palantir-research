#!/usr/bin/env python3
"""Inspect downloaded package artifacts without installation or code execution."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import re
import tempfile

OUT = Path(__file__).parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--artifacts-dir", type=Path, default=Path(tempfile.gettempdir()) / "palantir-custom-widgets-npm")
parser.add_argument("--sources-dir", type=Path, default=Path(tempfile.gettempdir()) / "palantir-custom-widgets-source")
args = parser.parse_args()
audit = json.loads((OUT / "protocol-npm-audit.json").read_text())
comparison = json.loads((OUT / "protocol-npm-source-compare.json").read_text())
source_scratch = args.sources_dir
result = {"inspectedAt": datetime.now(timezone.utc).isoformat(), "method": "Offline path, JSON, declaration text and content-hash inspection; no package code installed or executed.", "packages": []}

def flatten_targets(value, prefix=""):
    if isinstance(value, str):
        return [(prefix, value)]
    return [item for key, child in value.items() for item in flatten_targets(child, prefix + "/" + key)]

for package in audit["packages"]:
    name = package["name"].split("/")[1]
    root = args.artifacts_dir / package["packageSubdirectory"] / "package"
    manifest = json.loads((root / "package.json").read_text())
    root_targets = [{"condition": c, "path": p, "exists": (root / p).is_file()} for c, p in flatten_targets(manifest["exports"]["."])]
    wildcard_targets = [{"condition": c, "pattern": p, "matchingFileCount": sum(1 for f in root.glob(p.removeprefix("./")) if f.is_file())} for c, p in flatten_targets(manifest["exports"]["./*"])]
    browser_esm = []
    for browser_path in sorted((root / "build/browser").rglob("*.js")):
        rel = browser_path.relative_to(root / "build/browser")
        esm_path = root / "build/esm" / rel
        browser_esm.append({"relativePath": rel.as_posix(), "browserEqualsEsm": browser_path.read_bytes() == esm_path.read_bytes()})
    manifest_differences = []
    for commit in comparison["commits"]:
        source_manifest = json.loads((source_scratch / commit / "packages" / name / "package.json").read_text())
        changes = {key: {"source": source_manifest.get(key), "published": manifest.get(key)} for key in sorted(source_manifest.keys() | manifest.keys()) if source_manifest.get(key) != manifest.get(key)}
        manifest_differences.append({"commit": commit, "sourceVersion": source_manifest["version"], "sameExports": source_manifest["exports"] == manifest["exports"], "logicalJsonDifferences": changes})
    declarations = (root / "build/types/index.d.ts").read_text()
    stable_sections = [(version, text.strip()) for version, text in re.findall(r"^## (\d+\.\d+\.\d+)\n(.*?)(?=^## |\Z)", (root / "CHANGELOG.md").read_text(), re.M | re.S)]
    change_pattern = r"parameter type|object set parameters|reloading widget|browser permissions|widget set manifest authorizations|emitEvent types|parse out parameter config"
    functional_sections = [{"version": v, "selectedBullets": [line for line in t.splitlines() if line.startswith("- ") and (v == "3.74.0" or re.search(change_pattern, line, re.I))]} for v, t in stable_sections if v == "3.74.0" or re.search(change_pattern, t, re.I)][:14]
    result["packages"].append({"name": package["name"], "version": manifest["version"], "license": manifest["license"], "dependencies": manifest["dependencies"], "packagedManifestMatchesRegistryVersionAndDependencies": manifest["version"] == package["selectedVersionMetadata"]["version"] and manifest["dependencies"] == package["selectedVersionMetadata"]["dependencies"], "rootExportTargets": root_targets, "wildcardExportTargets": wildcard_targets, "browserEsmContentComparisons": browser_esm, "rootTypeDeclarationSha256": hashlib.sha256(declarations.encode()).hexdigest(), "rootTypeDeclarationSnapshot": declarations, "sourceManifestDifferences": manifest_differences, "selectedFunctionalChangelogSections": functional_sections})
(OUT / "protocol-npm-artifact-details.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"evidence": "protocol-npm-artifact-details.json", "packages": [{"name": p["name"], "rootExportsAllExist": all(t["exists"] for t in p["rootExportTargets"]), "wildcardTargetMatchingFileCounts": [t["matchingFileCount"] for t in p["wildcardExportTargets"]], "browserEsmFilesAllEqual": all(t["browserEqualsEsm"] for t in p["browserEsmContentComparisons"])} for p in result["packages"]]}, ensure_ascii=False, indent=2))
