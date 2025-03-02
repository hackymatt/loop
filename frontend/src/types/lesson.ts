import { IUserProps } from "./user";
import { ITechnologyProps } from "./technology";

export type ILessonTechnologyProps = Pick<ITechnologyProps, "id" | "name">;

export type ILessonLecturerProps = Pick<IUserProps, "id" | "gender" | "image"> & { name: string };

export type ILessonProps = {
  id: string;
  technologies: ILessonTechnologyProps[];
  title: string;
  description: string;
  duration: number;
  githubUrl: string;
  price: number;
  active: boolean;
  ratingNumber: number | null;
  totalReviews: number;
  totalStudents: number;
  teachers: ILessonLecturerProps[];
};

export type ILessonPriceHistoryProps = {
  id: string;
  lesson: ILessonProps;
  price: number;
  createdAt: string;
};
