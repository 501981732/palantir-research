/** Compile against the actual 3.74.0 package declarations using TypeScript 5.5.4. */
import { defineConfig, type EventParameterValueMap, type ParameterValue } from '@osdk/widget.api';
import { createFoundryWidgetClient } from '@osdk/widget.client';

const config = defineConfig({
  id: 'protocolProbe', name: 'Protocol probe', type: 'workshop',
  parameters: {
    count: { type: 'number', displayName: 'Count' },
    day: { type: 'date', displayName: 'Date' },
    scenarios: { type: 'array', subType: 'scenario', displayName: 'Scenarios' },
    style: { type: 'mapTileLayer', displayName: 'Read only style' },
  },
  events: { changed: { displayName: 'Changed', parameterUpdateIds: ['count', 'day', 'scenarios'] } },
});
const client = createFoundryWidgetClient<typeof config>();
client.emitEvent('changed', {
  parameterUpdates: { count: 2, day: '2026-10-01', scenarios: ['ri.mock.scenario'] },
});
// @ts-expect-error - A declared number parameter cannot be emitted as a string.
const badNumber: EventParameterValueMap<typeof config, 'changed'> = { count: '2', day: '2026-10-01', scenarios: [] };
// @ts-expect-error - A declared event name is required.
client.emitEvent('missingEvent', { parameterUpdates: {} });
// @ts-expect-error - Date wire values are strings, not JavaScript Date instances.
const badDate: ParameterValue.Date = { type: 'date', value: { type: 'loaded', value: new Date() } };
const scenarioArray: ParameterValue.ScenarioArray = { type: 'array', subType: 'scenario', value: { type: 'loaded', value: ['ri.mock.scenario'] } };
const emptyNumber: ParameterValue.Number = { type: 'number', value: { type: 'loaded', value: undefined } };
// Type compatibility alone does not establish date format or finite numeric value.
const malformedDate: ParameterValue.Date = { type: 'date', value: { type: 'loaded', value: 'not-a-date' } };
const infiniteNumber: ParameterValue.Number = { type: 'number', value: { type: 'loaded', value: Infinity } };
defineConfig({
  id: 'readOnlyProbe', name: 'Read only probe', type: 'workshop',
  parameters: { style: { type: 'mapTileLayer', displayName: 'Style' } },
  events: {
    invalid: {
      displayName: 'Invalid',
      // @ts-expect-error - mapTileLayer parameter IDs are excluded from event updates.
      parameterUpdateIds: ['style'],
    },
  },
});
defineConfig({
  id: 'missingParameterProbe', name: 'Missing parameter probe', type: 'workshop',
  parameters: { count: { type: 'number', displayName: 'Count' } },
  events: {
    invalid: {
      displayName: 'Invalid',
      // @ts-expect-error - Event updates must name an existing parameter.
      parameterUpdateIds: ['missingParameter'],
    },
  },
});
void [badNumber, badDate, scenarioArray, emptyNumber, malformedDate, infiniteNumber];
