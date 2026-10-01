#!/usr/bin/env bash
# Official published no-OSDK template; no tenant, token, mock SDK or deploy.
set -euo pipefail
probe_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
probe_work_dir="$(mktemp -d /tmp/widget-build-reproduce.XXXXXX)"
cd "$probe_work_dir"
npm exec --yes --registry=https://registry.npmjs.org --cache=/tmp/widget-research-npm-cache \
  --package=@osdk/create-widget@3.74.0 -- create-osdk-widget official-widget \
  --template=widget-react --sdkVersion=2.x --foundryUrl=https://example.palantirfoundry.com \
  --widgetSet=ri.widgetregistry..widget-set.public-research-probe --skipOsdk
cd official-widget
cp "$probe_script_dir/../evidence/build-template-package-lock.json" package-lock.json
npm ci --registry=https://registry.npmjs.org --cache=/tmp/widget-research-npm-cache --ignore-scripts --no-audit --no-fund
npm run lint
npm run build
node "$probe_script_dir/build-validation.mjs" "$probe_work_dir/official-widget"
printf 'Generated project: %s\n' "$probe_work_dir/official-widget"
