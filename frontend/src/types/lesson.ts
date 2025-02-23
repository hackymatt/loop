import { ITechnologyProps } from "./technology";

export type ILessonProps = {
  id: string;
  technologies: Pick<ITechnologyProps, "id" | "name">[];
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
