import type { FoundryWidgetClientContext } from "@osdk/widget.client-react";
import { defineConfig } from "@osdk/widget.client";
import type { taskWidgetConfig } from "./adapter-example.js";

export function verifyEventConstraints(context: FoundryWidgetClientContext<typeof taskWidgetConfig>) {
  // @ts-expect-error Event IDs must exist in the widget configuration.
  context.emitEvent("unknownEvent", { parameterUpdates: {} });
  // @ts-expect-error All event parameterUpdateIds must be present in the payload.
  context.emitEvent("selectionChanged", { parameterUpdates: { isSelectAll: true } });
  // @ts-expect-error React augmentation accepts ObjectSet, rather than the wire RID object.
  context.emitEvent("selectionChanged", { parameterUpdates: { isSelectAll: true, selectedTasks: { objectSetRid: "ri.object-set.mock" } } });
}

defineConfig({
  id: "invalidLayerWriter", name: "Type-negative fixture", type: "workshop",
  parameters: { layer: { type: "mapTileLayer", displayName: "Layer" } },
  events: {
    changed: { displayName: "Changed", parameterUpdateIds: [
      // @ts-expect-error mapTileLayer is read-only in the current published contract.
      "layer",
    ] },
  },
});
