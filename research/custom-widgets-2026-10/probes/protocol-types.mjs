/**
 * Reproducer for 3.74.0 TypeScript contract probes, including negative controls.
 * Install @osdk/widget.api@3.74.0, @osdk/widget.client@3.74.0 and typescript@5.5.4
 * with --ignore-scripts into /tmp/custom-widgets-protocol-runtime first.
 */
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
const runtime = process.env.PROTOCOL_RUNTIME ?? '/tmp/custom-widgets-protocol-runtime';
const original = readFileSync(new URL('./protocol-types.ts', import.meta.url), 'utf8');
const args = ['--noEmit', '--strict', '--skipLibCheck', '--module', 'nodenext', '--moduleResolution', 'nodenext', '--target', 'es2022'];
writeFileSync(resolve(runtime, 'protocol-types.ts'), original);
const compile = (file) => spawnSync(resolve(runtime, 'node_modules/.bin/tsc'), [file, ...args], { cwd: runtime, encoding: 'utf8', timeout: 30000 });
const expected = compile('protocol-types.ts');
assert.equal(expected.status, 0, expected.stdout + expected.stderr);
writeFileSync(resolve(runtime, 'protocol-types-negative-control.ts'), original.replace(/^.*@ts-expect-error.*\n/gm, ''));
const negative = compile('protocol-types-negative-control.ts');
assert.equal(negative.status, 2, negative.stdout + negative.stderr);
const errors = negative.stdout.split('\n').filter(line => /error TS\d+/.test(line));
assert.equal(errors.length, 5, negative.stdout);
const packageVersion = (name) => JSON.parse(readFileSync(resolve(runtime, 'node_modules', name, 'package.json'), 'utf8')).version;
const evidence = {
  title: 'Actual npm 3.74.0 declaration contract and negative controls',
  retrievedAt: new Date().toISOString(), nodeVersion: process.version,
  packageVersions: { widgetApi: packageVersion('@osdk/widget.api'), widgetClient: packageVersion('@osdk/widget.client'), typescript: packageVersion('typescript') },
  sourceSha256: createHash('sha256').update(original).digest('hex'),
  scope: 'TypeScript declaration behavior only; no runtime schema or real Workshop validation.',
  positiveCompilation: { exitCode: expected.status, diagnostics: expected.stdout + expected.stderr },
  negativeControlCompilation: { exitCode: negative.status, errorCount: errors.length, diagnostics: negative.stdout + negative.stderr },
  positiveCases: ['valid raw event updates', 'scenario arrays', 'loaded undefined', 'malformed date string is still assignable as string', 'Infinity is still assignable as number'],
  rejectedCases: ['number as string', 'unknown event ID', 'JavaScript Date instance as date wire value', 'read-only mapTileLayer event update', 'unknown parameter ID in event'],
};
const outputPath = fileURLToPath(new URL('../evidence/protocol-types-probe.json', import.meta.url));
writeFileSync(outputPath, `${JSON.stringify(evidence, null, 2)}\n`);
process.stdout.write(`PASS type probe and ${errors.length} negative controls; ${outputPath}\n`);
