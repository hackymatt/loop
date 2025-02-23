import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IModuleProps } from "src/types/module";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { ListQueryResponse } from "../types";
import { getListData, getCsrfToken } from "../utils";

const endpoint = "/modules" as const;

type ILesson = {
  id: string;
  title: string;
};

type IModule = {
  id: string;
  title: string;
  price: number;
  duration: number;
  lessons: ILesson[];
};

type ICreateModule = Omit<IModule, "id" | "lessons" | "price" | "duration"> & {
  lessons: string[];
};
type ICreateModuleReturn = ICreateModule;
export const modulesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<IModuleProps[]>> => {
    const { results, records_count, pages_count } = await getListData<IModule>(queryUrl);
    const modifiedResults = (results ?? []).map(
      ({ id, title, price, duration, lessons }: IModule) => ({
        id,
        title,
        duration,
        price,
        lessons,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useModules = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = modulesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useModulesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = modulesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateModule = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateModuleReturn, AxiosError, ICreateModule>(
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
