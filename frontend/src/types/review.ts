// ----------------------------------------------------------------------

import { IGender } from "./testimonial";

type IReviewUsers = {
  id: string;
  name: string;
  avatarUrl: string;
};

type IReviewReplyComment = {
  id: string;
  userId: string;
  message: string;
  createdAt: Date;
  tagUser?: string;
};

export type IReviewItemProp = {
  id: string;
  name: string;
  gender?: IGender;
  rating: number;
  createdAt: Date;
  message: string;
  helpful?: number;
  avatarUrl: string;
  users?: IReviewUsers[];
  replyComment?: IReviewReplyComment[];
  lessonTitle?: string;
  teacherName?: string;
  teacherGender?: string;
  teacherAvatarUrl?: string;
};

export type IReviewStatistic = {
  rating: string;
  count: number;
};

export type IReview = {
  lesson: number;
  lecturer: number;
  rating: number;
  review: string;
};
