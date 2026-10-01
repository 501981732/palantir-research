// Research-owned example, typechecked only. Replace MockTask with a generated SDK export.
import type { ObjectTypeDefinition } from "@osdk/api";
import type { Client } from "@osdk/client";
import { OsdkProvider } from "@osdk/react";
import { ObjectTable } from "@osdk/react-components/object-table";
import { defineConfig } from "@osdk/widget.client";
import { FoundryWidget, useFoundryWidgetContext } from "@osdk/widget.client-react";

export const MockTask = { type: "object", apiName: "MockTask", primaryKeyType: "string" } as const satisfies ObjectTypeDefinition;
export const taskWidgetConfig = defineConfig({
  id: "taskTable", name: "Task Table", type: "workshop",
  parameters: {
    tasks: { type: "objectSet", allowedType: MockTask, displayName: "Tasks" },
    selectedTasks: { type: "objectSet", allowedType: MockTask, displayName: "Selected tasks" },
    isSelectAll: { type: "boolean", displayName: "Select all intent" },
  },
  events: {
    selectionChanged: { displayName: "Selection changed", parameterUpdateIds: ["selectedTasks", "isSelectAll"] },
  },
});

export const useTaskWidget = useFoundryWidgetContext.withTypes<typeof taskWidgetConfig>();

function TaskTableAdapter() {
  const { asyncParameterValues, emitEvent } = useTaskWidget();
  const tasks = asyncParameterValues.tasks?.value;
  if (!tasks || tasks.type === "not-started" || tasks.type === "loading") return <p>等待宿主任务集…</p>;
  if (tasks.type === "failed") return <p role="alert">任务参数加载失败：{String(tasks.error)}</p>;
  if (!tasks.value) return <p>没有绑定任务集。</p>;
  return <ObjectTable
    objectType={MockTask}
    objectSet={tasks.value.objectSet}
    selectionMode="multiple"
    streamUpdates={false}
    onRowSelectionChanged={({ objectSet, isSelectAll }) => {
      if (objectSet) emitEvent("selectionChanged", { parameterUpdates: { selectedTasks: objectSet, isSelectAll } });
    }}
  />;
}

// Widget config/client are a mount boundary. If either contract changes, remount this entry.
export function TaskWidgetEntry({ client, contractVersion }: { client: Client; contractVersion: string }) {
  return <OsdkProvider client={client}>
    <FoundryWidget key={contractVersion} config={taskWidgetConfig} client={client}>
      <TaskTableAdapter />
    </FoundryWidget>
  </OsdkProvider>;
}

// This is an output adapter. It does not restore ObjectTable row selection from a host selection set.
// That requires a separate primary-key/Select-All contract and echo policy, rather than assuming
// an ObjectSet RID is a serializable array of all selected records.
