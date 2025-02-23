import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ILessonProps } from "src/types/lesson";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/lessons" as const;

type ITechnology = {
  id: string;
  name: string;
};

type ILesson = {
  id: string;
  technologies: ITechnology[];
  title: string;
  description: string;
  duration: number;
  github_url: string;
  price: number;
  active: boolean;
};

type IEditLesson = Omit<ILesson, "id" | "technologies"> & { technologies: string[] };
type IEditLessonReturn = IEditLesson;
export const lessonQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<ILessonProps>> => {
    const { data } = await getData<ILesson>(queryUrl);
    const {
      id: lessonId,
      title,
      description,
      duration,
      github_url,
      price,
      active,
      technologies,
    } = data;

    const modifiedResults = {
      id: lessonId,
      title,
      description,
      price,
      duration,
      technologies,
      githubUrl: github_url,
      active,
    };

    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useLesson = (id: string) => {
  const { queryKey, queryFn } = lessonQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditLesson = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditLessonReturn, AxiosError, IEditLesson>(
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
