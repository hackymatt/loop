import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ICartProp } from "src/types/cart";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/cart" as const;

type ILecturer = {
  full_name: string;
};

type ITechnology = {
  name: string;
};

type ILesson = {
  id: number;
  lecturers: ILecturer[];
  technologies: ITechnology[];
  title: string;
  duration: number;
  price: number;
};

type ICart = { id: number; lesson: ILesson };

type ICreateCart = { lesson: string };
type ICreateCartReturn = ICreateCart;
export const cartsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let data;
    try {
      const response = await Api.get(queryUrl);
      ({ data } = response);
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        data = { results: [], records_count: 0, pages_count: 0 };
      }
    }
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(({ id, lesson }: ICart) => {
      const { id: lessonId, title, duration, price, lecturers, technologies } = lesson;
      return {
        id,
        lesson: {
          id: lessonId,
          title,
          duration,
          price,
          teachers: lecturers.map(({ full_name }: ILecturer) => ({ name: full_name })),
          category: technologies.map(({ name }: ITechnology) => name),
        },
      };
    });

    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useCarts = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = cartsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICartProp[], count: data?.count, ...rest };
};

export const useCartsRecordsCount = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = cartsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.count, ...rest };
};

export const useCreateCart = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateCartReturn, AxiosError, ICreateCart>(
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
