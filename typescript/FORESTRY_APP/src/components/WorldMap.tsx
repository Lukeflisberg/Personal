import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { useAppStore } from "../store";
import { format } from "date-fns";

function circleIcon(color: string) {
  const svg = encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28">
      <circle cx="14" cy="14" r="10" stroke="black" stroke-width="1" fill="${color}"/>
    </svg>`
  );
  return L.icon({ iconUrl: `data:image/svg+xml,${svg}`, iconSize: [28, 28], iconAnchor: [14, 14] });
}

export function WorldMap() {
  const { groups, tasks, activeGroupFilter, setActiveGroupFilter } = useAppStore();
  const visibleTasks = Object.values(tasks).filter(t => !activeGroupFilter || t.groupId === activeGroupFilter);

  const Chips = () => (
    <div style={{ display: "flex", gap: 8, position: "absolute", zIndex: 1000, top: 10, left: 10 }}>
      {groups.map(g => {
        const active = activeGroupFilter === g.id;
        return (
          <button
            key={g.id}
            onClick={() => setActiveGroupFilter(active ? null : g.id)}
            className={`group-chip ${active ? "active" : "inactive"}`}
            style={{
              background: active ? g.color : undefined,
              borderColor: !active ? g.color : "transparent"
            }}
          >
            {g.name}
          </button>
        );
      })}
    </div>
  );

  return (
    <div className="map-container" style={{ position: "relative" }}>
      <Chips />
      <MapContainer center={[-33.9, 18.5]} zoom={7} style={{ height: 450, width: "100%" }}>
        <TileLayer
          attribution='&copy; OpenStreetMap'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {visibleTasks.map(t => {
          const color = groups.find(g => g.id === t.groupId)?.color ?? "#666";
          return (
            <Marker key={t.id} position={[t.lat, t.lon]} icon={circleIcon(color)}>
              <Popup>
                <b>{t.name}</b><br />
                {format(t.start, "MMM d")} → {format(t.end, "MMM d, yyyy")}
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
}
