import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ITopicProps } from "src/types/topic";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { ListQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/topics" as const;

type ITopic = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICreateTopic = Pick<ITopic, "name">;

type ICreateTopicReturn = ICreateTopic;

export const topicsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = `${url}?${urlParams}`;

  const queryFn = async (): Promise<ListQueryResponse<ITopicProps[]>> => {
    const { results, records_count, pages_count } = await getData<ITopic>(queryUrl);
    const modifiedResults = results.map(({ id, name, created_at }: ITopic) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useTopics = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = topicsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useTopicsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = topicsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateTopic = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateTopicReturn, AxiosError, ICreateTopic>(
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
