import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { ICourseByCategoryProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/skills" as const;

type ISkill = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICreateSkill = Pick<ISkill, "name">;

type ICreateSkillReturn = ICreateSkill;

export const skillsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, name, created_at }: ISkill) => ({
      id,
      name,
      createdAt: created_at,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useSkills = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = skillsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICourseByCategoryProps[], count: data?.count, ...rest };
};

export const useSkillsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = skillsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateSkill = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateSkillReturn, AxiosError, ICreateSkill>(
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
