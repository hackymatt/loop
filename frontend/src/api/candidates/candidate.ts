import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICandidateProps } from "src/types/candidate";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/candidates" as const;

type ICandidate = {
  id: string;
  created_at: string;
  name: string;
};

type IEditCandidate = Pick<ICandidate, "name">;

type IEditCandidateReturn = IEditCandidate;

type IDeleteCandidate = { id: string };

type IDeleteCandidateReturn = {};

export const candidateQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<ICandidateProps>> => {
    const { data } = await getData<ICandidate>(queryUrl);
    const { id: candidateId, name, created_at } = data;

    const modifiedResults = {
      id: candidateId,
      name,
      createdAt: created_at,
    };
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useCandidate = (id: string) => {
  const { queryKey, queryFn } = candidateQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};
export const useEditCandidate = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditCandidateReturn, AxiosError, IEditCandidate>(
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

export const useDeleteCandidate = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteCandidateReturn, AxiosError, IDeleteCandidate>(
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
