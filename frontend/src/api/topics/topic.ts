import { AxiosError } from "axios";
import { useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/topics" as const;

type ITopic = {
  id: number;
  modified_at: string;
  created_at: string;
  name: string;
};

type IEditTopic = Pick<ITopic, "name">;

type IEditTopicReturn = IEditTopic;

type IDeleteTopic = {};

type IDeleteTopicReturn = {};

export const useEditTopic = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditTopicReturn, AxiosError, IEditTopic>(
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

export const useDeleteTopic = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IDeleteTopicReturn, AxiosError, IDeleteTopic>(
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
