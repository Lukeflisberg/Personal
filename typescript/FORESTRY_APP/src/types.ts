export type GroupId = string;
export type TaskId = string;

export type Task = {
  id: TaskId;
  name: string;
  start: Date;
  end: Date;
  groupId: GroupId;
  lat: number;
  lon: number;
};

export type Dependency = {
  id: string;
  from: TaskId;
  to: TaskId;
  type?: "FS" | "SS" | "FF" | "SF";
};

export type Group = { id: GroupId; name: string; color: string };
