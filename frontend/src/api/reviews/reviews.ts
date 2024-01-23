import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IReviewItemProp } from "src/types/review";
import { IQueryParams } from "src/types/queryParams";

import { Api } from "../service";

const endpoint = "/reviews" as const;

type IProfile = {
  full_name: string;
  email: string;
  gender: IGender | null;
  image: string | null;
};

type IReview = {
  id: number;
  lesson_title: string;
  student: IProfile;
  lecturer: IProfile;
  created_at: string;
  review: string;
  rating: string;
};

export const reviewsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, lesson_title, student, lecturer, created_at, review, rating }: IReview) => {
        const { full_name: studentFullName, gender: studentGender, image: studentImage } = student;
        const { full_name: lecturerFullName } = lecturer;
        return {
          id,
          name: studentFullName,
          rating: parseFloat(rating),
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

  return { url, queryFn, queryKey: compact([queryUrl]) };
};

export const useReviews = (query?: IQueryParams) => {
  const { queryKey, queryFn } = reviewsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IReviewItemProp[], ...rest };
};

export const useReviewsPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = reviewsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
