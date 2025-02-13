import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { ILessonStatus, IReviewStatus, IPurchaseItemProp } from "src/types/purchase";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/purchases" as const;

type ILecturer = {
  id: string;
  full_name: string;
  gender: IGender | null;
  image: string | null;
};

type ILesson = {
  id: string;
  title: string;
  duration: number;
  github_url: string;
};

type IReview = {
  id: string;
  rating: string;
  review: string;
};

type ISchedule = {
  id: string;
  lecturer: ILecturer;
  start_time: string;
  end_time: string;
};

type IReservation = {
  id: string;
  schedule: ISchedule;
};

type IRecording = {
  file_name: string;
  file_url: string;
};

type IPurchase = {
  id: string;
  lesson: ILesson;
  lesson_status: ILessonStatus;
  reservation: IReservation;
  review_status: IReviewStatus;
  review: IReview | null;
  created_at: string;
  price: number;
  meeting_url?: string;
  recordings: IRecording[];
  payment: string;
};

type ICreatePurchase = {
  lessons: { lesson: string }[];
  coupon: string;
};

type ICreatePurchaseReturn = {
  token?: string;
  error?: string;
  responseCode: 0;
};

export const purchasesQuery = (query?: IQueryParams) => {
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
        price,
        lesson_status,
        reservation,
        review_status,
        review,
        meeting_url,
        recordings,
        payment,
        created_at,
      }: IPurchase) => {
        const { id: lessonId, title: lessonTitle, duration, github_url } = lesson;
        return {
          id,
          lessonId,
          lessonTitle,
          lessonResource: github_url,
          lessonDuration: duration,
          lessonPrice: price,
          lessonStatus: lesson_status,
          lessonSlot: reservation
            ? [reservation.schedule.start_time, reservation.schedule.end_time]
            : [null, null],
          reservationId: reservation?.id,
          teacher: reservation?.schedule.lecturer
            ? {
                id: reservation?.schedule.lecturer.id,
                name: reservation?.schedule.lecturer.full_name,
                avatarUrl: reservation?.schedule.lecturer.image,
                gender: reservation?.schedule.lecturer.gender,
              }
            : {},
          reviewStatus: review_status,
          reviewId: review?.id,
          ratingNumber: review?.rating,
          review: review?.review,
          meetingUrl: meeting_url,
          recordings: (recordings ?? []).map(({ file_name, file_url }: IRecording) => ({
            name: file_name,
            url: file_url,
          })),
          paymentId: payment,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePurchases = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = purchasesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPurchaseItemProp[], count: data?.count, ...rest };
};

export const usePurchasesPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = purchasesQuery(query);
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
