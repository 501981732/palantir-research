import assert from 'node:assert/strict';

// Resolve an allowed public entry, then inspect two pure implementation files
// in the installed npm artifact. These are not public consumer import paths.
const entry = import.meta.resolve('@osdk/react-components/action-form');
const { coerceFieldValue } = await import(new URL('../action-form/utils/coerceFieldValue.js', entry));
const { getDefaultFieldDefinitions } = await import(new URL('../action-form/utils/getDefaultFieldDefinitions.js', entry));

assert.equal(coerceFieldValue('integer', '12.9'), 12);
assert.equal(coerceFieldValue('string', null), undefined);
assert.equal(coerceFieldValue('timestamp', new Date('2026-09-01T00:00:00Z')), '2026-09-01T00:00:00.000Z');
assert.equal(coerceFieldValue('boolean', 'True'), undefined);
const definitions = getDefaultFieldDefinitions({ parameters: {
  name: { type: 'string', nullable: false },
  enabled: { type: 'boolean', nullable: true },
  objectSet: { type: { type: 'objectSet' }, nullable: true },
}});
assert.deepEqual(definitions.map(({ fieldComponent, isRequired }) => ({ fieldComponent, isRequired })), [
  { fieldComponent: 'TEXT_INPUT', isRequired: true },
  { fieldComponent: 'RADIO_BUTTONS', isRequired: false },
  { fieldComponent: 'OBJECT_SET', isRequired: false },
]);
assert.equal(definitions[2].fieldComponentProps.value, null);
console.log(JSON.stringify({ package: '@osdk/react-components', version: '0.61.0', assertions: 6, passed: 6, failed: 0, network: false, actions: false }));
