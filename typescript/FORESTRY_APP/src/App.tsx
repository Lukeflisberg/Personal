import React from "react";
import { GanttPanel } from "./components/GanttPanel";
import { WorldMap } from "./components/WorldMap";

export default function App() {
  return (
    <div style={{ padding: 16, display: "grid", gap: 16 }}>
      <h2>Forestry Ops Planner</h2>
      <GanttPanel />
      <WorldMap />
    </div>
  );
}
