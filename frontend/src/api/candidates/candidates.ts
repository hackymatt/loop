import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { ICandidateProps } from "src/types/candidate";

import { Api } from "../service";
import { ListQueryResponse } from "../types";
import { getListData, getCsrfToken } from "../utils";

const endpoint = "/candidates" as const;

type ICandidate = {
  id: string;
  created_at: string;
  name: string;
};

type ICreateCandidate = Pick<ICandidate, "name">;

type ICreateCandidateReturn = ICreateCandidate;

export const candidatesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<ICandidateProps[]>> => {
    const { results, records_count, pages_count } = await getListData<ICandidate>(queryUrl);
    const modifiedResults = results.map(({ id, name, created_at }: ICandidate) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useCandidates = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = candidatesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useCandidatesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = candidatesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateCandidate = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateCandidateReturn, AxiosError, ICreateCandidate>(
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
