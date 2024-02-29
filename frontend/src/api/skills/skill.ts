import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/skills" as const;

type ISkill = {
  id: number;
  modified_at: string;
  created_at: string;
  name: string;
};

type IEditSkill = Pick<ISkill, "name">;

type IEditSkillReturn = IEditSkill;

type IDeleteSkill = {};

type IDeleteSkillReturn = {};

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
        queryClient.invalidateQueries({ queryKey: [endpoint, id] });
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
