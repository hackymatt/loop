import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IPostProps } from "src/types/blog";
import { IGender } from "src/types/testimonial";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/posts" as const;

type ICategory = {
  id: string;
  name: string;
};

type ILecturer = {
  full_name: string;
  id: string;
  title: string;
  description: string;
  date_joined: string;
  image: string | null;
  gender: IGender | null;
};

type IPostNavigation = {
  id: string;
  title: string;
  image: string;
};

type IPost = {
  id: string;
  title: string;
  description: string;
  content: string;
  category: ICategory;
  duration: number;
  authors: ILecturer[];
  active: boolean;
  image: string;
  created_at: string;
  previous_post: IPostNavigation;
  next_post: IPostNavigation;
};

type IEditPost = Omit<
  IPost,
  "id" | "authors" | "category" | "duration" | "created_at" | "previous_post" | "next_post"
> & {
  content: string;
  category: string;
  active: boolean;
  authors: string[];
};

type IEditPostReturn = IEditPost;

type IDeletePost = { id: string };

type IDeletePostReturn = {};

export const postQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IPost>(queryUrl);
      const { data } = response;
      const {
        id: postId,
        title,
        description,
        content,
        category,
        duration,
        authors,
        active,
        image,
        created_at,
        previous_post,
        next_post,
      } = data;

      modifiedResults = {
        id: postId,
        title,
        description,
        content,
        category: category.name,
        duration: `${duration} min`,
        coverUrl: image,
        authors: authors.map(
          ({
            id: lecturerId,
            full_name,
            gender,
            image: lecturerImage,
            title: lecturerTitle,
            description: lecturerDescription,
            date_joined,
          }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            gender,
            avatarUrl: lecturerImage,
            role: lecturerTitle,
            description: lecturerDescription,
            dateJoined: date_joined,
          }),
        ),
        active,
        createdAt: created_at,
        previousPost: previous_post,
        nextPost: next_post,
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

export const usePost = (id: string) => {
  const { queryKey, queryFn } = postQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IPostProps, ...rest };
};

export const useEditPost = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditPostReturn, AxiosError, IEditPost>(
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

export const useDeletePost = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeletePostReturn, AxiosError, IDeletePost>(
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
