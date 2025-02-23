import { ITechnologyProps } from "./technology";

export type ILessonTechnologyProps = Pick<ITechnologyProps, "id" | "name">;

export type ILessonProps = {
  id: string;
  technologies: ILessonTechnologyProps[];
  title: string;
  description: string;
  duration: number;
  githubUrl: string;
  price: number;
  active: boolean;
};

export type ILessonPriceHistoryProps = {
  id: string;
  lesson: ILessonProps;
  price: number;
  createdAt: string;
};
