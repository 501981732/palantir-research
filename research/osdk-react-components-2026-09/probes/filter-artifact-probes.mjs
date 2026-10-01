// Read-only, no-network probes of the extracted @osdk/react-components tarball.
// Run: node filter-artifact-probes.mjs [absolute npm package directory]
import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const packageRoot = pathToFileURL(resolve(process.argv[2] ?? fileURLToPath(new URL('react19/node_modules/@osdk/react-components/', import.meta.url))) + '/');
const moduleUrls = {
  serialization: new URL('build/esm/filter-list/utils/filterStateSerialization.js', packageRoot),
  scopes: new URL('build/esm/filter-list/utils/narrowObjectSet.js', packageRoot),
  values: new URL('build/esm/filter-list/utils/filterValues.js', packageRoot),
};
const metadata = JSON.parse(await readFile(new URL('package.json', packageRoot), 'utf8'));
const { serializeFilterStates, deserializeFilterStates } = await import(moduleUrls.serialization.href);
const { computeDualScopes } = await import(moduleUrls.scopes.href);
const { NO_VALUE, dedupeEmptyAggregationRows } = await import(moduleUrls.values.href);

const original = new Map([['startDate', {
  type: 'DATE_RANGE',
  minValue: new Date('2026-09-01T00:00:00.000Z'),
}]]);
const serialized = serializeFilterStates(original);
const restoredValue = deserializeFilterStates(serialized).get('startDate').minValue;
const whereClause = { name: 'Alice' };
const whereCalls = [];
const narrowedSet = { kind: 'narrowed' };
const baseSet = { where: (where) => { whereCalls.push(where); return narrowedSet; } };
const withoutBase = computeDualScopes(undefined, whereClause, [], true);
const directOnly = computeDualScopes(baseSet, whereClause, [], true);
const nullInput = [{ value: NO_VALUE, count: 0 }];
const sourceHashes = {};
for (const [name, url] of Object.entries(moduleUrls)) {
  sourceHashes[name] = {
    relativePath: url.href.slice(packageRoot.href.length),
    sha256: createHash('sha256').update(await readFile(url)).digest('hex'),
  };
}
const result = {
  package: metadata.name,
  version: metadata.version,
  sourceCommit: '37cfd38676bf04edaef5847e929d914ea214c149',
  node: process.version,
  generatedAt: new Date().toISOString(),
  scope: 'Isolated utility modules; no React render, network, Ontology, or Actions.',
  sourceHashes,
  dateRoundTrip: {
    inputDate: original.get('startDate').minValue.toISOString(),
    serialized,
    restoredType: typeof restoredValue,
    restoredIsDate: restoredValue instanceof Date,
    restoredValue,
  },
  dualScopes: {
    withoutObjectSet: {
      scopedIsUndefined: withoutBase.scoped === undefined,
      emptySourceIsUndefined: withoutBase.emptySource === undefined,
    },
    directOnlyWithShowFilteredOutValues: {
      whereCalls,
      scoped: directOnly.scoped,
      emptySourceIsUndefined: directOnly.emptySource === undefined,
    },
  },
  zeroCountNoValue: {
    input: nullInput,
    output: dedupeEmptyAggregationRows(nullInput),
  },
};
const outputUrl = new URL('./filter-artifact-probes.json', import.meta.url);
await writeFile(outputUrl, JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ output: fileURLToPath(outputUrl), observations: {
  restoredIsDate: result.dateRoundTrip.restoredIsDate,
  withoutBaseDropsBothScopes: result.dualScopes.withoutObjectSet,
  directOnlyHasNoEmptySource: directOnly.emptySource === undefined,
  zeroCountNoValueOutput: result.zeroCountNoValue.output,
} }, null, 2));
