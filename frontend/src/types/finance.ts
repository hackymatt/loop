import { ICourseTeacherProp } from "./course";

export type IFinanceHistoryProp = {
  id: number;
  teacher: ICourseTeacherProp;
  account: string;
  rate: number;
  commission: number;
  createdAt: Date;
};

export type IEarningProp = {
  billing_date: string;
  year: number;
  month: number;
  earnings?: number;
  cost?: number;
  profit?: number;
};
