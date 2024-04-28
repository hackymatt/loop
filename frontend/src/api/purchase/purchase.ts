import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { ILessonStatus, IReviewStatus, IPurchaseItemProp } from "src/types/purchase";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

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
  duration: number;
};

type IReview = {
  id: number;
  rating: string;
  review: string;
};

type ISchedule = {
  id: number;
  lecturer: ILecturer;
  start_time: string;
  end_time: string;
};

type IReservation = {
  id: number;
  schedule: ISchedule;
};

type IPurchase = {
  id: number;
  lesson: ILesson;
  lesson_status: ILessonStatus;
  reservation: IReservation;
  review_status: IReviewStatus;
  review: IReview | null;
  created_at: string;
  price: number;
};

type ICreatePurchase = {
  lessons: { lesson: string }[];
  coupon: string;
};

type ICreatePurchaseReturn = IPurchase[];

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
        reservation,
        review_status,
        review,
        created_at,
      }: IPurchase) => {
        const { id: lessonId, title: lessonTitle, duration } = lesson;
        return {
          id,
          lessonId,
          lessonTitle,
          lessonDuration: duration,
          lessonStatus: lesson_status,
          lessonSlot: reservation
            ? [reservation.schedule.start_time, reservation.schedule.end_time]
            : [null, null],
          reservationId: reservation?.id,
          teacher: reservation?.schedule.lecturer
            ? {
                id: reservation?.schedule.lecturer.uuid,
                name: reservation?.schedule.lecturer.full_name,
                email: reservation?.schedule.lecturer.email,
                avatarUrl: reservation?.schedule.lecturer.image,
                gender: reservation?.schedule.lecturer.gender,
              }
            : {},
          reviewStatus: review_status,
          reviewId: review?.id,
          ratingNumber: review?.rating,
          review: review?.review,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePurchase = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = purchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPurchaseItemProp[], ...rest };
};

export const usePurchasePageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = purchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreatePurchase = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreatePurchaseReturn, AxiosError, ICreatePurchase>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
