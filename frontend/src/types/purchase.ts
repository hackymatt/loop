// ----------------------------------------------------------------------

import { ITeamMemberProps } from "./team";

export enum LessonStatus {
  Nowa = "Nowa",
  Zaplanowana = "Zaplanowana",
  Zakończona = "Zakończona",
}

export enum ReviewStatus {
  Ukończone = "Ukończone",
  Oczekujące = "Oczekujące",
}

export type ILessonStatus = keyof typeof LessonStatus;

export type IReviewStatus = keyof typeof ReviewStatus;

export type IPurchaseItemProp = {
  id: string;
  courseTitle: string;
  lessonTitle: string;
  lessonStatus: ILessonStatus;
  teacher: ITeamMemberProps;
  reviewStatus: IReviewStatus;
  ratingNumber: number;
  message: string;
  createdAt: Date;
};
