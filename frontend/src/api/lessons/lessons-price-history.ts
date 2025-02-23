import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { ILessonPriceHistoryProps } from "src/types/lesson";

import { getListData } from "../utils";
import { ListQueryResponse } from "../types";

const endpoint = "/lesson-price-history" as const;

type ITechnology = {
  id: string;
  name: string;
};

type ILesson = {
  id: string;
  technologies: ITechnology[];
  title: string;
  description: string;
  duration: number;
  github_url: string;
  price: number;
  active: boolean;
};

type ILessonPriceHistory = {
  id: string;
  lesson: ILesson;
  price: number;
  created_at: string;
};

export const lessonsPriceHistoryQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<ILessonPriceHistoryProps[]>> => {
    const { results, records_count, pages_count } =
      await getListData<ILessonPriceHistory>(queryUrl);
    const modifiedResults = (results ?? []).map(
      ({ id, lesson, price, created_at }: ILessonPriceHistory) => {
        const {
          id: lessonId,
          title,
          description,
          duration,
          github_url,
          price: lessonPrice,
          active,
          technologies,
        } = lesson;
        return {
          id,
          lesson: {
            id: lessonId,
            title,
            description,
            price: lessonPrice,
            duration,
            technologies,
            githubUrl: github_url,
            active,
          },
          price,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessonsPriceHistory = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = lessonsPriceHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useLessonsPriceHistoryPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonsPriceHistoryQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
