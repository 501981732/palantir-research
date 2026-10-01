// Research harness: actual npm React/client packages, simulated host only.
import assert from "node:assert/strict";
import { JSDOM } from "jsdom";

const dom = new JSDOM("<!doctype html><body><div id='root'></div></body>", { url: "https://local.invalid" });
for (const name of ["window", "document", "HTMLElement", "Event", "EventTarget", "CustomEvent"]) globalThis[name] = dom.window[name];
globalThis.IS_REACT_ACT_ENVIRONMENT = true;
let resizeCallback;
let resizeDisconnected = 0;
globalThis.ResizeObserver = class {
  constructor(callback) { resizeCallback = callback; }
  observe() {}
  disconnect() { resizeDisconnected++; }
};
const React = await import("react");
const { createRoot } = await import("react-dom/client");
const { FoundryWidget, useFoundryWidgetContext } = await import("@osdk/widget.client-react");
const { createClient } = await import("@osdk/client");
const { act, createElement: h } = React;
const checks = [];
const record = (name, observed) => checks.push({ name, observed, result: "PASS" });
let context;
function Capture() { context = useFoundryWidgetContext(); return null; }
const config = {
  id: "reactProbe", name: "LOCAL MOCK React probe", type: "workshop",
  parameters: {
    title: { type: "string", displayName: "Title" },
    count: { type: "number", displayName: "Count" },
    scenario: { type: "scenario", displayName: "Scenario RID" },
    layer: { type: "mapTileLayer", displayName: "Map layer" },
    labels: { type: "array", subType: "string", displayName: "Labels" },
  },
  events: { countChanged: { displayName: "Count changed", parameterUpdateIds: ["count"] } },
};
const loaded = (type, value) => ({ type, value: { type: "loaded", value } });
const mount = async ({ strict = false, initialValues, config: cfg = config, client } = {}) => {
  const transport = new EventTarget();
  const sent = [];
  let adds = 0, removes = 0;
  window.__PALANTIR_WIDGET_API__ = {
    sendMessage(message) { sent.push(message); },
    addEventListener(type, callback, opts) { adds++; transport.addEventListener(type, callback, opts); },
    removeEventListener(type, callback, opts) { removes++; transport.removeEventListener(type, callback, opts); },
  };
  const root = createRoot(document.getElementById("root"));
  const tree = () => h(FoundryWidget, { config: cfg, initialValues, client }, h(Capture));
  await act(async () => root.render(strict ? h(React.StrictMode, null, tree()) : tree()));
  return {
    sent, root,
    subscriptions: () => ({ adds, removes }),
    async push(parameters) {
      let reads = 0;
      const payload = { get parameters() { reads++; return parameters; } };
      await act(async () => transport.dispatchEvent(new CustomEvent("message", { detail: { type: "host.update-parameters", payload } })));
      return reads;
    },
    async unmount() { await act(async () => root.unmount()); },
  };
};

// Context outside its provider silently exposes defaults, rather than throwing.
let root = createRoot(document.getElementById("root"));
await act(async () => root.render(h(Capture)));
assert.equal(context.parameters.state, "not-started");
assert.doesNotThrow(() => context.emitEvent("any", { parameterUpdates: {} }));
record("context_without_provider", { state: context.parameters.state, values: context.parameters.values, emit: "no-op" });
await act(async () => root.unmount());

const harness = await mount({ initialValues: { title: loaded("string", "fixture") } });
assert.equal(context.asyncParameterValues.title.value.value, "fixture");
assert.deepEqual(context.parameters, { values: {}, state: "not-started" });
record("initialValues_do_not_initialize_aggregate", context.parameters);
assert.equal(harness.sent[0].type, "widget.ready");
assert.equal(harness.sent[0].payload.apiVersion, "1.0.0");
const values = {
  title: loaded("string", "Host title"), count: loaded("number", 4),
  scenario: loaded("scenario", "ri.ontology.main.scenario.mock"),
  layer: loaded("mapTileLayer", { styleJsonUrl: "https://local.invalid/mock-style.json" }),
};
assert.equal(await harness.push(values), 1);
assert.equal(context.parameters.state, "loaded");
assert.equal(context.parameters.values.scenario, values.scenario.value.value);
assert.deepEqual(context.parameters.values.layer, values.layer.value.value);
record("scenario_and_mapTileLayer_are_pass_through", { scenario: context.parameters.values.scenario, layer: context.parameters.values.layer });
context.emitEvent("countChanged", { parameterUpdates: { count: 9 } });
assert.equal(context.parameters.values.count, 4);
assert.deepEqual(harness.sent.at(-1), { type: "widget.emit-event", payload: { eventId: "countChanged", parameterUpdates: { count: 9 } } });
record("emitEvent_requires_host_echo_to_update_context", { contextCount: context.parameters.values.count, outboundCount: 9 });
await harness.push({ count: loaded("number", 9) });
assert.equal(context.parameters.values.count, 9);
record("host_echo_updates_context", context.parameters);
await harness.push({ title: { type: "string", value: { type: "failed", error: new Error("mock failure"), value: "previous" } } });
assert.equal(context.parameters.state, "failed");
await harness.push({ count: loaded("number", 10) });
assert.equal(context.parameters.state, "loaded");
assert.equal(context.asyncParameterValues.title.value.type, "failed");
record("partial_update_aggregate_only_checks_current_message", { aggregate: context.parameters.state, retainedTitle: context.asyncParameterValues.title.value.type });
await act(async () => resizeCallback([{ borderBoxSize: [{ inlineSize: 640, blockSize: 360 }] }]));
assert.deepEqual(harness.sent.at(-1), { type: "widget.resize", payload: { width: 640, height: 360 } });
record("ResizeObserver_notifies_host", harness.sent.at(-1));
await harness.unmount();
assert.equal(harness.subscriptions().removes, 1);
assert.equal(resizeDisconnected, 1);
record("unmount_cleans_transport_and_observer", { ...harness.subscriptions(), resizeDisconnected });

const strict = await mount({ strict: true });
const strictReads = await strict.push(values);
assert.equal(strictReads, 2);
assert.deepEqual(strict.subscriptions(), { adds: 2, removes: 1 });
record("StrictMode_effect_replay_retains_two_hostEventTarget_handlers", { parameterGetterReads: strictReads, ...strict.subscriptions() });
await strict.unmount();

const defaults = await mount();
assert.equal(context.asyncParameterValues.labels.type, "array");
assert.equal(context.asyncParameterValues.labels.subType, undefined);
record("initial_array_not_started_omits_subType", context.asyncParameterValues.labels);
await defaults.unmount();

// Hydration uses the real client, but no backend request is made until fetching.
let networkCalls = 0;
const osdk = createClient("https://local.invalid", "ri.ontology.main.ontology.mock", async () => "mock-token", async () => { networkCalls++; throw new Error("unexpected mock network call"); });
const ObjectType = { type: "object", apiName: "MockTask" };
const objectConfig = { id: "objectProbe", name: "Object hydration mock", type: "workshop", parameters: { objects: { type: "objectSet", displayName: "Tasks", allowedType: ObjectType } }, events: {} };
const objectHarness = await mount({ config: objectConfig, client: osdk });
await objectHarness.push({ objects: loaded("objectSet", { objectSetRid: "ri.object-set.mock.one" }) });
const firstSet = context.parameters.values.objects.objectSet;
await objectHarness.push({ objects: loaded("objectSet", { objectSetRid: "ri.object-set.mock.one" }) });
assert.equal(context.parameters.values.objects.objectSet, firstSet);
await objectHarness.push({ objects: loaded("objectSet", { objectSetRid: "ri.object-set.mock.two" }) });
assert.notEqual(context.parameters.values.objects.objectSet, firstSet);
assert.equal(networkCalls, 0);
record("ObjectSet_lazy_hydration_and_same_RID_identity_cache", { sameRidPreservesIdentity: true, newRidChangesIdentity: true, networkCalls });
await objectHarness.unmount();

console.log(JSON.stringify({ boundary: "ACTUAL NPM CLIENT/REACT, JSDOM + SIMULATED HOST; NO FOUNDRY TENANT", checkedAt: new Date().toISOString(), node: process.version, react: React.version, versions: { widgetClientReact: "3.74.0", widgetClient: "3.74.0", osdkClient: "2.75.0" }, checks }, null, 2));
