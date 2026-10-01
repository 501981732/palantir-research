/**
 * Runs the actual @osdk/widget.api / widget.client 3.74.0 npm artifacts against
 * a deliberately small injected-bridge mock. This is NOT a Workshop test,
 * browser postMessage/origin test, tenant permission test, or server test.
 *
 * Provision without package lifecycle scripts:
 * npm install --ignore-scripts --prefix /tmp/custom-widgets-protocol-runtime \
 *   @osdk/widget.client@3.74.0 @osdk/widget.api@3.74.0 --no-audit --no-fund
 * node research/custom-widgets-2026-10/probes/protocol-client.mjs
 * Optional: PROTOCOL_RUNTIME=/path/to/runtime-directory
 */
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const runtime = process.env.PROTOCOL_RUNTIME ?? '/tmp/custom-widgets-protocol-runtime';
const require = createRequire(resolve(runtime, 'package.json'));
const api = require('@osdk/widget.api');
const { createFoundryWidgetClient, createFoundryWidgetTokenProvider } = require('@osdk/widget.client');
const results = [];
const test = (name, run) => {
  run();
  results.push({ name, result: 'PASS' });
};

globalThis.window = {};
test('missing injected bridge throws immediately', () => {
  assert.throws(() => createFoundryWidgetClient(), /Missing __PALANTIR_WIDGET_API__/);
});
const sent = [];
const listeners = new Set();
const bridge = {
  sendMessage(message) { sent.push(structuredClone(message)); },
  addEventListener(type, listener) {
    assert.equal(type, 'message');
    listeners.add(listener);
  },
  removeEventListener(type, listener) {
    assert.equal(type, 'message');
    listeners.delete(listener);
  },
  // The mock intentionally exposes transport delivery; no browser is involved.
  deliver(detail) {
    for (const listener of listeners) listener(new CustomEvent('message', { detail }));
  },
};
globalThis.window.__PALANTIR_WIDGET_API__ = bridge;
const client = createFoundryWidgetClient();
test('construction neither subscribes nor sends ready automatically', () => {
  assert.equal(listeners.size, 0);
  assert.equal(sent.length, 0);
});
test('ready announces the wire API version 1.0.0', () => {
  client.ready();
  assert.deepEqual(sent.at(-1), { type: 'widget.ready', payload: { apiVersion: '1.0.0' } });
});
let received = [];
client.hostEventTarget.addEventListener('host.update-parameters', event => received.push(event.detail));
const initial = {
  count: { type: 'number', value: { type: 'loaded', value: 7 } },
  selected: { type: 'objectSet', value: { type: 'loaded', value: { objectSetRid: 'ri.mock.object-set' } } },
};
test('subscribed host payload is dispatched without value conversion', () => {
  client.subscribe();
  bridge.deliver({ type: 'host.update-parameters', payload: { parameters: initial } });
  assert.equal(received.length, 1);
  assert.equal(received[0].parameters, initial);
});
test('unknown host message is silently ignored by the client visitor', () => {
  bridge.deliver({ type: 'host.future-message', payload: {} });
  assert.equal(received.length, 1);
});
test('emitEvent forwards updates but does not synthesize a host acknowledgement', () => {
  client.emitEvent('updateCount', { parameterUpdates: { count: 8 } });
  assert.deepEqual(sent.at(-1), {
    type: 'widget.emit-event',
    payload: { eventId: 'updateCount', parameterUpdates: { count: 8 } },
  });
  assert.equal(received.length, 1);
  assert.equal(received[0].parameters.count.value.value, 7);
});
test('reload and resize are one-way bridge messages', () => {
  client.reload();
  assert.deepEqual(sent.at(-1), { type: 'widget.reload', payload: {} });
  client.resize({ width: 640, height: 360 });
  assert.deepEqual(sent.at(-1), { type: 'widget.resize', payload: { width: 640, height: 360 } });
});
test('unsubscribe stops delivery and subscribe can restore it', () => {
  client.unsubscribe();
  bridge.deliver({ type: 'host.update-parameters', payload: { parameters: initial } });
  assert.equal(received.length, 1);
  client.subscribe();
  bridge.deliver({ type: 'host.update-parameters', payload: { parameters: initial } });
  assert.equal(received.length, 2);
});
test('message guards only discriminate type and do not validate payload', () => {
  assert.equal(api.isHostParametersUpdatedMessage({ type: 'host.update-parameters' }), true);
  assert.equal(api.isWidgetEmitEventMessage({ type: 'widget.emit-event', payload: null }), true);
});
test('defineConfig is an identity function, not a runtime schema validator', () => {
  const invalid = { id: 'Invalid ID!', parameters: { bad: { type: 'unsupported' } } };
  assert.equal(api.defineConfig(invalid), invalid);
});
test('untyped callers can forward undeclared event/parameter IDs', () => {
  client.emitEvent('notInAnyConfig', { parameterUpdates: { undeclaredParameter: 'x' } });
  assert.equal(sent.at(-1).payload.eventId, 'notInAnyConfig');
  assert.deepEqual(sent.at(-1).payload.parameterUpdates, { undeclaredParameter: 'x' });
});
test('generic sendMessage is a pass-through at this public client layer', () => {
  client.sendMessage({ type: 'widget.not-a-supported-message', payload: { arbitrary: true } });
  assert.equal(sent.at(-1).type, 'widget.not-a-supported-message');
});
const placeholder = await createFoundryWidgetTokenProvider()();
assert.equal(placeholder, 'widgets-auth');
results.push({ name: 'token provider callback resolves placeholder widgets-auth', result: 'PASS' });
client.unsubscribe();

const output = {
  title: 'Actual npm widget API/client with a local injected-bridge mock',
  retrievedAt: new Date().toISOString(),
  nodeVersion: process.version,
  packageVersions: {
    widgetApi: JSON.parse(require('node:fs').readFileSync(resolve(runtime, 'node_modules/@osdk/widget.api/package.json'), 'utf8')).version,
    widgetClient: JSON.parse(require('node:fs').readFileSync(resolve(runtime, 'node_modules/@osdk/widget.client/package.json'), 'utf8')).version,
  },
  scope: 'Client behavior only. No real Workshop, Foundry authentication, browser iframe/postMessage/origin enforcement, or permission checks.',
  mockPolicy: 'Only window.__PALANTIR_WIDGET_API__ is replaced; package implementation and its dependency are the published npm artifacts.',
  assertionCount: results.length,
  results,
  messagesSent: sent,
};
const evidencePath = fileURLToPath(new URL('../evidence/protocol-client-probe.json', import.meta.url));
writeFileSync(evidencePath, `${JSON.stringify(output, null, 2)}\n`);
process.stdout.write(`PASS ${results.length} assertions; ${evidencePath}\n`);
