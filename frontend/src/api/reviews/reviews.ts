import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IReviewItemProp } from "src/types/review";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";
import { purchaseQuery } from "../purchase/purchase";

const endpoint = "/reviews" as const;

type IStudent = {
  first_name: string;
  email: string;
  gender: IGender | null;
  image: string | null;
};

type ILecturer = {
  full_name: string;
  email: string;
  gender: IGender | null;
  image: string | null;
};

type IReview = {
  id: number;
  lesson_title: string;
  student: IStudent;
  lecturer: ILecturer;
  created_at: string;
  review?: string | null;
  rating: number;
};

type ICreateReview = Pick<IReview, "rating" | "review"> & { lesson: string; lecturer: string };
type ICreateReviewReturn = ICreateReview;
export const reviewsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, lesson_title, student, lecturer, created_at, review, rating }: IReview) => {
        const {
          first_name: studentFirstName,
          gender: studentGender,
          image: studentImage,
        } = student;
        const { full_name: lecturerFullName } = lecturer;
        return {
          id,
          name: studentFirstName,
          rating: parseFloat(rating.toString()),
          createdAt: created_at,
          gender: studentGender,
          message: review,
          avatarUrl: studentImage,
          lessonTitle: lesson_title,
          teacherName: lecturerFullName,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useReviews = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = reviewsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IReviewItemProp[], ...rest };
};

export const useReviewsPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = reviewsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateReview = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateReviewReturn, AxiosError, ICreateReview>(
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
        queryClient.invalidateQueries({ queryKey: purchaseQuery().queryKey });
      },
    },
  );
};
