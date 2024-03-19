import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { ILessonStatus, IReviewStatus, IPurchaseItemProp } from "src/types/purchase";

import { Api } from "../service";

const endpoint = "/purchase" as const;

type ILecturer = {
  uuid: string;
  full_name: string;
  email: string;
  gender: IGender | null;
  image: string | null;
};

type ILesson = {
  id: number;
  title: string;
};

type IReview = {
  id: number;
  rating: string;
  review: string;
};

type IPurchase = {
  id: number;
  lesson: ILesson;
  lesson_status: ILessonStatus;
  reservation_date: string | null;
  lecturer: ILecturer | null;
  review_status: IReviewStatus;
  review: IReview | null;
  created_at: string;
  price: number;
};

export const purchaseQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({
        id,
        lesson,
        lesson_status,
        reservation_date,
        lecturer,
        review_status,
        review,
        created_at,
      }: IPurchase) => {
        const { title: lessonTitle } = lesson;
        return {
          id,
          lessonTitle,
          lessonStatus: lesson_status,
          lessonSlot: reservation_date,
          teacher: lecturer
            ? {
                id: lecturer.uuid,
                name: lecturer.full_name,
                email: lecturer.email,
                avatarUrl: lecturer.image,
                gender: lecturer.gender,
              }
            : {},
          reviewStatus: review_status,
          ratingNumber: review?.rating,
          message: review?.review,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePurchase = (query?: IQueryParams) => {
  const { queryKey, queryFn } = purchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IPurchaseItemProp[], ...rest };
};

export const usePurchasePageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = purchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
