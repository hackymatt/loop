import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ITeachingProp } from "src/types/course";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/teaching" as const;

type ITeaching = {
  id: number;
  teaching: boolean;
  teaching_id: number | null;
  title: string;
  duration: number;
  github_url: string;
  price: number;
  active: boolean;
};

type ICreateTeaching = { lesson: string };
type ICreateTeachingReturn = ICreateTeaching;

export const teachingsQuery = (query?: IQueryParams) => {
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
      ({ id, teaching, teaching_id, price, title, duration, github_url, active }: ITeaching) => ({
        id,
        teaching,
        teachingId: teaching_id,
        price,
        title,
        duration,
        githubUrl: github_url,
        active,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useTeachings = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = teachingsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ITeachingProp[], count: data?.count, ...rest };
};

export const useTeachingsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = teachingsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateTeaching = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateTeachingReturn, AxiosError, ICreateTeaching>(
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
