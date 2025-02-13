import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { IPurchaseItemProp } from "src/types/purchase";

import { Api } from "../service";

const endpoint = "/purchases" as const;

type ILesson = {
  id: string;
  title: string;
  duration: number;
  github_url: string;
};

type IPurchase = {
  id: string;
  lesson: ILesson;
  created_at: string;
  price: number;
  payment: string;
};

export const lessonPurchaseQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    const { data } = await Api.get(queryUrl);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, lesson, price, payment, created_at }: IPurchase) => {
      const { id: lessonId, title: lessonTitle, duration, github_url } = lesson;
      return {
        id,
        lessonId,
        lessonTitle,
        lessonResource: github_url,
        lessonDuration: duration,
        lessonPrice: price,
        paymentId: payment,
        createdAt: created_at,
      };
    });
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessonPurchases = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = lessonPurchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPurchaseItemProp[], count: data?.count, ...rest };
};

export const useLessonPurchasesPageCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonPurchaseQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
