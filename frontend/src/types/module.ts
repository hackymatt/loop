import { ILessonProps } from "./lesson";

export type IModuleLessonProps = Pick<ILessonProps, "id" | "title">;

export type IModuleProps = {
  id: string;
  title: string;
  price: number;
  totalHours: number;
  lessons: IModuleLessonProps[];
};
