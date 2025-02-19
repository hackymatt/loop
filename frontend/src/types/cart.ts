import { ITeacherProp } from "./teacher";
import { ITechnologyProps } from "./technology";

type ILessonProp = {
  id: string;
  title: string;
  duration: number;
  price: number;
  teachers: Pick<ITeacherProp, "name">[];
  technologies: Pick<ITechnologyProps, "name">[];
};

export type ICartProp = {
  id: string;
  lesson: ILessonProp;
};
