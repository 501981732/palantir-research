"""Audit public npm artifacts against release source; raw material stays in /tmp.

Run after npm pack/extraction as described in build-release.md. No tenant calls.
This compares digest/content; it does not cryptographically verify npm signatures.
"""
import base64
import argparse
import concurrent.futures
import hashlib
import json
import pathlib
import urllib.request

TMP = pathlib.Path('/tmp/widget-build-research')
OUT = pathlib.Path(__file__).resolve().parents[1] / 'evidence'
RELEASE = 'fb8ec172d540ef7819382ff036aa2a692614af75'
MAIN = 'e53b94ecd5de7cdd7e864d0daa04363bdad4db4c'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--main-tree', type=pathlib.Path, help='Optional osdk-ts checkout at the pinned main comparison commit.')
args = parser.parse_args()
MAIN_TREE = args.main_tree
PACKAGES = [('plugin', '@osdk/widget.vite-plugin', '3.74.0', 'widget.vite-plugin'),
            ('create', '@osdk/create-widget', '3.74.0', 'create-widget'),
            ('cli', '@osdk/cli', '0.101.0', 'cli'),
            ('config', '@osdk/foundry-config-json', '1.13.0', 'foundry-config-json')]

def sha(b):
    return hashlib.sha256(b).hexdigest()

def fetch(url):
    with urllib.request.urlopen(url, timeout=35) as r:
        return r.read()

metadata = []
for local, name, version, folder in PACKAGES:
    url = 'https://registry.npmjs.org/' + name.replace('/', '%2f')
    raw = fetch(url)
    data = json.loads(raw)
    ver = data['versions'][version]
    filename = 'osdk-' + folder + '-' + version + '.tgz'
    tarball = (TMP / filename).read_bytes()
    entry = {'name': name, 'version': version, 'retrievedDate': '2026-10-01',
             'publishedAt': data['time'][version], 'distTags': data['dist-tags'],
             'registryUrl': url, 'registryResponseSha256': sha(raw),
             'tarballUrl': ver['dist']['tarball'], 'tarballBytes': len(tarball),
             'tarballSha256': sha(tarball), 'distIntegrity': ver['dist']['integrity'],
             'integrityMatchesDownloadedTarball': ver['dist']['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(tarball).digest()).decode(),
             'peerDependencies': ver.get('peerDependencies', {}), 'dependencies': ver.get('dependencies', {})}
    provenance_path = TMP / (local + '-provenance.json')
    if provenance_path.exists():
        entry['provenanceResponseSha256'] = sha(provenance_path.read_bytes())
        for att in json.loads(provenance_path.read_bytes())['attestations']:
            payload = json.loads(base64.b64decode(att['bundle']['dsseEnvelope']['payload']))
            if payload['predicateType'] == 'https://slsa.dev/provenance/v1':
                entry['provenanceGitCommit'] = payload['predicate']['buildDefinition']['resolvedDependencies'][0]['digest']['gitCommit']
                entry['provenanceInvocation'] = payload['predicate']['runDetails']['metadata']['invocationId']
                entry['provenanceSubjectDigestMatchesTarball'] = payload['subject'][0]['digest']['sha512'] == hashlib.sha512(tarball).hexdigest()
    metadata.append(entry)
(OUT / 'build-package-versions.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n')

sources = {}
for local, name, version, folder in PACKAGES:
    root = TMP / local / 'package' / 'build' / 'esm'
    for mp in root.rglob('*.js.map'):
        m = json.loads(mp.read_bytes())
        for source, content in zip(m['sources'], m.get('sourcesContent', [])):
            if not content:
                continue
            if local in ['plugin', 'config']:
                src = 'packages/' + folder + '/src/' + str(mp.parent.relative_to(root) / source)
            elif '/src/' in source:
                src = 'packages/' + folder + '/src/' + source.split('/src/', 1)[1]
            else:
                continue
            if '/generatedNoCheck/' in src or src.endswith('/templates.ts'):
                continue
            if local == 'cli' and not ('widgetset/' in src or 'widget-registry/' in src):
                continue
            sources[src] = {'sourceMap': str(mp.relative_to(TMP)), 'content': content,
                            'comparisonMode': 'original-ts' if local in ['plugin', 'config'] else 'transpiled-intermediate-js'}

def audit(pair):
    src, v = pair
    url = 'https://raw.githubusercontent.com/palantir/osdk-ts/' + RELEASE + '/' + src
    result = {'path': src, 'url': 'https://github.com/palantir/osdk-ts/blob/' + RELEASE + '/' + src,
              'sourceMap': v['sourceMap'], 'sourceMapContentSha256': sha(v['content'].encode()),
              'comparisonMode': v['comparisonMode']}
    try:
        raw = fetch(url)
        result.update({'releaseSourceSha256': sha(raw), 'releaseMatchesSourceMap': raw.decode() == v['content']})
        if v['comparisonMode'] == 'transpiled-intermediate-js':
            result['interpretation'] = 'Bundled source map stores transpiled JS; byte comparison with original TS is not a behavioral compatibility verdict.'
        local = MAIN_TREE / src if MAIN_TREE is not None else None
        if local is not None and local.exists():
            result['currentMainSha'] = MAIN
            result['currentMainMatchesSourceMap'] = local.read_text() == v['content']
    except Exception as e:
        result['error'] = str(e)
    return result

with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    audits = sorted(pool.map(audit, sources.items()), key=lambda r: r['path'])
(OUT / 'build-source-map-audit.json').write_text(json.dumps(audits, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'packages': [(m['name'], m['version'], m['publishedAt'], m['integrityMatchesDownloadedTarball']) for m in metadata],
                  'sourceFiles': len(audits), 'releaseMatch': sum(a.get('releaseMatchesSourceMap') is True for a in audits),
                  'currentMainMatch': sum(a.get('currentMainMatchesSourceMap') is True for a in audits),
                  'errors': [a for a in audits if a.get('error')]}, ensure_ascii=False, indent=2))
