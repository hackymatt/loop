// ----------------------------------------------------------------------

import { ITeamMemberProps } from "./team";
import { IPaymentStatus } from "./payment";

export enum LessonStatus {
  NEW = "nowa",
  PLANNED = "zaplanowana",
  CONFIRMED = "potwierdzona",
  COMPLETED = "zakończona",
}

export enum ReviewStatus {
  COMPLETED = "ukończone",
  PENDING = "oczekujące",
  NONE = "brak",
}

export type ILessonStatus = `${LessonStatus}`;

export type IReviewStatus = `${ReviewStatus}`;

export type IRecordingProp = { name: string; url: string };

export type IPurchaseItemProp = {
  id: string;
  lessonId: string;
  lessonTitle: string;
  lessonResource: string;
  lessonDuration: number;
  lessonPrice: number;
  lessonStatus: ILessonStatus;
  lessonSlot: string[];
  reservationId: string;
  teacher: ITeamMemberProps;
  reviewStatus: IReviewStatus;
  reviewId: string;
  ratingNumber: number;
  review: string;
  meetingUrl: string;
  recordings: IRecordingProp[];
  paymentId: string;
  createdAt: Date;
};

export type IPurchaseError = { lessons: { lesson: string }[]; coupon: string };

export type IPaymentCurrencyProp = "PLN" | "USD" | "EUR";

export type IPaymentItemProp = {
  id: string;
  sessionId: string;
  amount: number;
  currency: IPaymentCurrencyProp;
  status: IPaymentStatus;
  createdAt: Date;
};
