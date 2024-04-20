import { ICourseTeacherProp } from "./course";

export type IFinanceHistoryProp = {
  id: number;
  teacher: ICourseTeacherProp;
  account: string;
  rate: number;
  commission: number;
  createdAt: Date;
};

type ILecturer = {
  email: string;
  full_name: string;
  account: string;
  street_address: string;
  city: string;
  zip_code: string;
  country: string;
};

export type IEarningProp = {
  actual: boolean;
  year: number;
  month: number;
  lecturer?: ILecturer;
  earnings?: number;
  cost?: number;
  profit?: number;
};
