import { ICourseTeacherProp } from "./course";

export type IFinanceHistoryProp = {
  id: number;
  teacher: ICourseTeacherProp;
  account: string;
  rate: number;
  commission: number;
  createdAt: Date;
};
