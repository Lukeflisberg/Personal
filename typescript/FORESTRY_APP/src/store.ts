import { create } from "zustand";
import { addMilliseconds, isBefore } from "date-fns";
import type { Task, Group, Dependency, TaskId, GroupId } from "./types";

type State = {
  groups: Group[];
  tasks: Record<TaskId, Task>;
  deps: Dependency[];
  activeGroupFilter: GroupId | null;
  setActiveGroupFilter: (g: GroupId | null) => void;
  moveTask: (id: TaskId, patch: Partial<Pick<Task, "start" | "end" | "groupId">>) => { ok: boolean; reason?: string };
};

function violatesDeps(tasks: Record<TaskId, Task>, deps: Dependency[], changedTaskId: TaskId): string | null {
  const t = tasks[changedTaskId];
  if (!t) return null;

  for (const d of deps) {
    const pred = tasks[d.from];
    const succ = tasks[d.to];
    const kind = d.type ?? "FS";

    if (!pred || !succ || (d.from !== t.id && d.to !== t.id)) continue;

    switch (kind) {
      case "FS":
        if (isBefore(succ.start, pred.end)) return `Invalid: "${pred.name}" must finish before "${succ.name}" starts`;
        break;
      case "SS":
        if (isBefore(succ.start, pred.start)) return `Invalid: "${pred.name}" must start before "${succ.name}" starts`;
        break;
      case "FF":
        if (isBefore(succ.end, pred.end)) return `Invalid: "${pred.name}" must finish before "${succ.name}" finishes`;
        break;
      case "SF":
        if (isBefore(succ.end, pred.start)) return `Invalid: "${pred.name}" must start before "${succ.name}" finishes`;
        break;
    }
  }
  return null;
}

export const useAppStore = create<State>((set, get) => ({
  groups: [
    { id: "group1", name: "Group 1", color: "#1f77b4" },
    { id: "group2", name: "Group 2", color: "#2ca02c" },
    { id: "group3", name: "Group 3", color: "#d62728" }
  ],
  tasks: {
    task1: { id: "task1", name: "Soil Survey", start: new Date("2025-08-18"), end: new Date("2025-08-20"), groupId: "group1", lat: -33.9249, lon: 18.4241 },
    task2: { id: "task2", name: "Road Prep",   start: new Date("2025-08-21"), end: new Date("2025-08-23"), groupId: "group1", lat: -34.0, lon: 18.5 },
    task4: { id: "task4", name: "Harvest A",   start: new Date("2025-08-24"), end: new Date("2025-08-27"), groupId: "group2", lat: -33.2, lon: 19.0 },
    task5: { id: "task5", name: "Machine Serv.",start:new Date("2025-08-19"), end: new Date("2025-08-20"), groupId: "group2", lat: -33.8, lon: 19.1 }
  },
  deps: [
    { id: "dep1", from: "task1", to: "task2", type: "FS" },
    { id: "dep2", from: "task5", to: "task4", type: "FS" }
  ],
  activeGroupFilter: null,

  setActiveGroupFilter: (g) => set({ activeGroupFilter: g }),

  moveTask: (id, patch) => {
    const { tasks, deps } = get();
    const current = tasks[id];
    if (!current) return { ok: false, reason: "Task not found" };

    const candidate: Task = { ...current, ...patch };
    if (candidate.end < candidate.start) {
      candidate.end = addMilliseconds(candidate.start, 60 * 60 * 1000);
    }

    const nextTasks = { ...tasks, [id]: candidate };
    const err = violatesDeps(nextTasks, deps, id);
    if (err) return { ok: false, reason: err };

    set({ tasks: nextTasks });
    return { ok: true };
  }
}));

