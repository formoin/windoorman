import { create } from "zustand";
import axiosApi from "../instance/axiosApi";

export interface Schedule {
  scheduleId: number;
  groupId: number;
  placeName: string;
  windowName: string;
  startTime: string;
  endTime: string;
  days: string[];
  activate: boolean;
}

interface ScheduleState {
  schedules: Schedule[];
  RegistSchedule: (
    windowsId: number,
    startTime: string,
    endTime: string,
    days: string[]
  ) => Promise<void>;
  fetchSchedules: () => Promise<void>;
  isActive: (groupId: number, activate: boolean) => Promise<void>;
}

const useScheduleStore = create<ScheduleState>((set) => ({
  schedules: [],
  RegistSchedule: async (windowsId, startTime, endTime, days) => {
    try {
      const response = await axiosApi.post("/schedules", {
        windowsId,
        startTime,
        endTime,
        days,
      });
      console.log("Registered schedule:", response);
    } catch (error) {
      console.error("Failed to register schedule:", error);
    }
  },
  fetchSchedules: async () => {
    try {
      const response = await axiosApi.get(`/schedules`);
      set({ schedules: response.data });
      console.log("Fetched schedules:", response);
    } catch (error) {
      console.error("Failed to fetch schedules:", error);
    }
  },
  isActive: async (groupId, activate) => {
    try {
      await axiosApi.patch(`/schedules/toggle`, { groupId, activate });
    } catch (error) {
      console.error("Failed to change schedule activation:", error);
    }
  },
}));

export default useScheduleStore;
