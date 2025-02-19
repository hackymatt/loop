import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICourseModuleProp } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/modules" as const;

type ILesson = {
  id: string;
  title: string;
};

type IModule = {
  id: string;
  title: string;
  lessons: ILesson[];
};

type IEditModule = Omit<IModule, "id" | "lessons" | "price" | "duration"> & { lessons: string[] };
type IEditModuleReturn = IEditModule;

type IDeleteModule = { id: string };
type IDeleteModuleReturn = IDeleteModule;
export const moduleQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IModule>(queryUrl);
      const { data } = response;
      const { id: moduleId, title, lessons } = data;

      modifiedResults = {
        id: moduleId,
        title,
        lessons: lessons.map(({ id: lessonId, title: titleId }: ILesson) => ({
          id: lessonId,
          title: titleId,
        })),
      };
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useModule = (id: string) => {
  const { queryKey, queryFn } = moduleQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseModuleProp, ...rest };
};

export const useEditModule = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditModuleReturn, AxiosError, IEditModule>(
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

export const useDeleteModule = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteModuleReturn, AxiosError, IDeleteModule>(
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
