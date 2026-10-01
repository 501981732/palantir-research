import assert from "node:assert/strict";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

// Isolated helper probes of the downloaded 0.61.0 artifact. No network,
// production ontology, React rendering, action or mutation is involved.
const artifactRoot = resolve(process.argv[2] ?? resolve(import.meta.dirname, "react19/node_modules/@osdk/react-components"), "build/esm/object-table");
const { deriveSelectionObjectSet } = await import(pathToFileURL(`${artifactRoot}/utils/deriveSelectionObjectSet.js`));
const { buildSnapshotRow, DEFAULT_SNAPSHOT_ROW_LIMIT, fetchFunctionColumnValues } = await import(pathToFileURL(`${artifactRoot}/utils/objectTableSnapshot.js`));
const constants = await import(pathToFileURL(`${artifactRoot}/utils/constants.js`));
let whereCalls = [];
const filtered = { kind: "synthetic-filtered-set" };
const syntheticSet = { where: (clause) => { whereCalls.push(clause); return filtered; } };
const partial = { selectedRows: [{ $primaryKey: 1 }, { $primaryKey: 2 }], isSelectAll: false };
assert.equal(deriveSelectionObjectSet(syntheticSet, partial), filtered);
assert.deepEqual(whereCalls.at(-1), { $primaryKey: { $in: [1, 2] } });
assert.equal(deriveSelectionObjectSet(syntheticSet, { ...partial, isSelectAll: true }), syntheticSet);
assert.equal(whereCalls.length, 1);
deriveSelectionObjectSet(syntheticSet, { selectedRows: [], isSelectAll: false });
assert.deepEqual(whereCalls.at(-1), { $primaryKey: { $in: [] } });
assert.equal(deriveSelectionObjectSet(undefined, partial), undefined);
assert.equal(constants.DEFAULT_PAGE_SIZE, 50);
assert.equal(constants.DEFAULT_ROW_HEIGHT, 40);
assert.equal(constants.VIRTUALIZER_OVERSCAN, 5);
assert.equal(constants.SCROLL_FETCH_THRESHOLD, 100);
assert.equal(DEFAULT_SNAPSHOT_ROW_LIMIT, 10_000);

const raw = { $primaryKey: "a", name: "Raw property" };
const functionLocator = { id: "computed", getKey: object => object.$primaryKey };
const failure = new Error("synthetic function failure");
const snapshot = buildSnapshotRow(raw, ["name", "computed"], [functionLocator], new Map([["computed", new Map([["a", failure]])]]));
assert.equal(snapshot.getValue("name"), "Raw property");
assert.equal(snapshot.getValue("computed"), failure);

let inFlight = 0;
let peak = 0;
const pages = ["a", "b", "c"].map(key => ({ objectSet: { key }, objects: [{ $primaryKey: key }] }));
const locator = { id: "computed", queryDefinition: {}, getKey: object => object.$primaryKey, getFunctionParams: objectSet => objectSet };
const values = await fetchFunctionColumnValues([locator], pages, async (_definition, params) => {
  inFlight++;
  peak = Math.max(peak, inFlight);
  await new Promise(resolveProbe => setTimeout(resolveProbe, 5));
  inFlight--;
  if (params.key === "b") throw failure;
  return { [params.key]: `result-${params.key}` };
}, 1);
assert.equal(peak, 1);
assert.equal(values.get("computed").get("a"), "result-a");
assert.equal(values.get("computed").get("b"), failure);
assert.equal(values.get("computed").get("c"), "result-c");
process.stdout.write(JSON.stringify({ artifact: "@osdk/react-components@0.61.0", probes: "passed", network: false, scope: "isolated pure helper modules", selectionAllReturnsOriginalSet: true, snapshotDefaultRowLimit: DEFAULT_SNAPSHOT_ROW_LIMIT, functionQueryPeakConcurrency: peak }) + "\n");
