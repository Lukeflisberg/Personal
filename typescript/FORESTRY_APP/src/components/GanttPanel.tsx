import React, { useMemo, useState } from "react";
import { Timeline } from "@thetechcompany/react-gantt-timeline";
import type { TimelineProps } from "@thetechcompany/react-gantt-timeline";
import { useAppStore } from "../store";
import type { Task } from "../types";

export function GanttPanel() {
  const { groups, tasks, deps, moveTask } = useAppStore();
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const ganttGroups = groups.map(g => ({
    id: g.id,
    title: g.name,
    style: { "--group-color": g.color } as React.CSSProperties
  }));

  // Convert tasks object to array
  const ganttItems = Object.values(tasks).map(t => {
    const group = groups.find(g => g.id === t.groupId);
    return {
      id: t.id,
      group: t.groupId,
      title: t.name,
      start_time: t.start,
      end_time: t.end,
      style: {
        backgroundColor: group?.color ?? "#666", // main fill
        borderColor: group?.color ?? "#666",     // border match
        color: "#fff"                            // text color
      }
    };
  });

  const links = useMemo(() => deps.map(d => ({ id: d.id, start: d.from, end: d.to })), [deps]);

  const onUpdateTask: TimelineProps["onUpdateTask"] = (item, props: any) => {
    const patch: Partial<Task> = {
      start: props.start ?? item.start,
      end: props.end ?? item.end,
      groupId: (props.groupId ?? item.group) as string
    };
    const { ok, reason } = moveTask(item.id as string, patch);
    if (!ok) {
      setErrorMsg(reason ?? "Invalid move");
      return false;
    }
    setErrorMsg(null);
    return true;
  };

  return (
    <div className="gantt-container">
      {errorMsg && <div className="gantt-error">{errorMsg}</div>}
      <Timeline
        groups={ganttGroups}
        items={ganttItems}
        links={links}
        onUpdateTask={onUpdateTask}
        canMove
        canChangeGroup
        canResize="both"
        zoomLevels={["day", "week", "month"]}
        />
    </div>
    );
}
