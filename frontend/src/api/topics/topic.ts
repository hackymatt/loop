import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ITopicProps } from "src/types/topic";

import { Api } from "../service";
import { getCsrfToken } from "../utils";
import { GetQueryResponse } from "../types";

const endpoint = "/topics" as const;

type ITopic = {
  id: string;
  modified_at: string;
  created_at: string;
  name: string;
};

type IEditTopic = Pick<ITopic, "name">;

type IEditTopicReturn = IEditTopic;

type IDeleteTopic = { id: string };

type IDeleteTopicReturn = {};

export const topicQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<ITopicProps>> => {
    const response = await Api.get<ITopic>(queryUrl);
    const { data } = response;
    const { id: topicId, name, created_at } = data;

    const modifiedResults: ITopicProps = {
      id: topicId,
      name,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useTopic = (id: string) => {
  const { queryKey, queryFn } = topicQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};
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
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};

export const useDeleteTopic = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteTopicReturn, AxiosError, IDeleteTopic>(
    async ({ id }) => {
      const result = await Api.delete(`${endpoint}/${id}`, {
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
