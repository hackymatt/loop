import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { ICourseLessonPriceHistoryProp } from "src/types/course";

import { Api } from "../service";

const endpoint = "/lesson-price-history" as const;

type ILecturer = {
  full_name: string;
  uuid: string;
  email: string;
  image: string | null;
  gender: IGender | null;
};

type ITechnology = {
  id: number;
  name: string;
};

type ILesson = {
  id: number;
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  technologies: ITechnology[];
  title: string;
  description: string;
  duration: number;
  github_url: string;
  price: string;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  active: boolean;
};

type ILessonPriceHistory = {
  id: number;
  lesson: ILesson;
  price: number;
  created_at: string;
};

export const lessonsPriceHistoryQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let data;
    try {
      const response = await Api.get(queryUrl);
      ({ data } = response);
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        data = { results: [], records_count: 0, pages_count: 0 };
      }
    }
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, lesson, price, created_at }: ILessonPriceHistory) => ({
        id,
        lesson,
        price,
        createdAt: created_at,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessonsPriceHistory = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = lessonsPriceHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICourseLessonPriceHistoryProp[], ...rest };
};

export const useLessonsPriceHistoryPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonsPriceHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
