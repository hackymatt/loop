import { ILessonProps } from "./lesson";

export type IModuleProps = {
  id: string;
  title: string;
  price: number;
  duration: number;
  lessons: Pick<ILessonProps, "id" | "title">[];
};
