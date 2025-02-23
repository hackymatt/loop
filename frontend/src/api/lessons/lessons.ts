import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ILessonProps } from "src/types/lesson";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { ListQueryResponse } from "../types";
import { getListData, getCsrfToken } from "../utils";

const endpoint = "/lessons" as const;

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: "Mężczyzna" | "Kobieta" | "Inne";
};

type ITechnology = {
  id: string;
  name: string;
};

type ILesson = {
  id: string;
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  technologies: ITechnology[];
  title: string;
  description: string;
  duration: number;
  github_url: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  active: boolean;
};

type ICreateLesson = Omit<
  ILesson,
  | "id"
  | "lecturers"
  | "students_count"
  | "rating"
  | "rating_count"
  | "previous_price"
  | "lowest_30_days_price"
  | "technologies"
> & { technologies: string[] };
type ICreateLessonReturn = ICreateLesson;
export const lessonsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<ILessonProps[]>> => {
    const { results, records_count, pages_count } = await getListData<ILesson>(queryUrl);
    const modifiedResults = (results ?? []).map(
      ({
        id,
        description,
        price,
        previous_price,
        lowest_30_days_price,
        title,
        technologies,
        duration,
        rating,
        rating_count,
        students_count,
        lecturers,
        github_url,
        active,
      }: ILesson) => ({
        id,
        description,
        price,
        priceSale: previous_price,
        lowest30DaysPrice: lowest_30_days_price,
        title,
        technologies,
        duration,
        ratingNumber: rating,
        totalReviews: rating_count,
        totalStudents: students_count,
        teachers: (lecturers ?? []).map(
          ({ id: lecturerId, full_name, gender, image: lecturerImage }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            image: lecturerImage,
            gender,
          }),
        ),
        githubUrl: github_url,
        active,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessons = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = lessonsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useLessonsPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateLesson = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateLessonReturn, AxiosError, ICreateLesson>(
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
