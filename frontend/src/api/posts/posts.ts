import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IPostProps } from "src/types/blog";
import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/posts" as const;

type ICategory = {
  id: string;
  name: string;
};

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: IGender | null;
};

type IPost = {
  id: string;
  title: string;
  description: string;
  category: ICategory;
  duration: number;
  authors: ILecturer[];
  active: boolean;
  image: string;
  publication_date: string;
};

type ICreatePost = Omit<IPost, "id" | "authors" | "category" | "tags" | "duration"> & {
  content: string;
  category: string;
  active: boolean;
  authors: string[];
  tags: string[];
};

type ICreatePostReturn = ICreatePost;

export const postsQuery = (query?: IQueryParams) => {
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
    const modifiedResults = results.map(
      ({
        id,
        title,
        description,
        category,
        duration,
        authors,
        active,
        image,
        publication_date,
      }: IPost) => ({
        id,
        title,
        description,
        category: category.name,
        duration: `${duration} min`,
        coverUrl: image,
        authors: authors.map(
          ({ id: lecturerId, full_name, gender, image: lecturerImage }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            avatarUrl: lecturerImage,
            gender,
          }),
        ),
        active,
        publicationDate: publication_date,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const usePosts = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = postsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IPostProps[], count: data?.count, ...rest };
};

export const usePostsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = postsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreatePost = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreatePostReturn, AxiosError, ICreatePost>(
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
