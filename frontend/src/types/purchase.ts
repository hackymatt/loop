// ----------------------------------------------------------------------

import { ITeamMemberProps } from "./team";

export enum LessonStatus {
  nowa = "nowa",
  zaplanowana = "zaplanowana",
  zakończona = "zakończona",
}

export enum ReviewStatus {
  ukończone = "ukończone",
  oczekujące = "oczekujące",
  brak = "brak",
}

export type ILessonStatus = keyof typeof LessonStatus;

export type IReviewStatus = keyof typeof ReviewStatus;

export type IPurchaseItemProp = {
  id: string;
  lessonTitle: string;
  lessonDuration: number;
  lessonStatus: ILessonStatus;
  lessonSlot: string[];
  reservationId: string;
  teacher: ITeamMemberProps;
  reviewStatus: IReviewStatus;
  reviewId: string;
  ratingNumber: number;
  review: string;
  createdAt: Date;
};
