import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICourseBySkillProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/skills" as const;

type ISkill = {
  id: number;
  created_at: string;
  name: string;
};

type IEditSkill = Pick<ISkill, "name">;

type IEditSkillReturn = IEditSkill;

type IDeleteSkill = {};

type IDeleteSkillReturn = {};

export const skillQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    const response = await Api.get<ISkill>(queryUrl);
    const { data } = response;
    const { id: skillId, name, created_at } = data;

    const modifiedResults = {
      id: skillId,
      name,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useSkill = (id: string) => {
  const { queryKey, queryFn } = skillQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseBySkillProps, ...rest };
};

export const useEditSkill = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditSkillReturn, AxiosError, IEditSkill>(
    async (variables) => {
      const result = await Api.put(url, variables, {
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

export const useDeleteSkill = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteSkillReturn, AxiosError, IDeleteSkill>(
    async () => {
      const result = await Api.delete(url, {
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
