import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/query-params";
import { ILevel, ICourseProps } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/courses" as const;

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: IGender | null;
};

export type ITechnology = {
  id: string;
  name: string;
};

type ICourse = {
  id: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  duration: number;
  technologies: ITechnology[];
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  image: string;
  level: ILevel;
  title: string;
  description: string;
  active: boolean;
  progress: number | null;
};

type ICreateCourse = Omit<
  ICourse,
  | "id"
  | "price"
  | "previous_price"
  | "lowest_30_days_price"
  | "duration"
  | "technologies"
  | "lecturers"
  | "students_count"
  | "rating"
  | "rating_count"
  | "modules"
  | "skills"
  | "topics"
  | "progress"
> & { modules: string[]; skills: string[]; topics: string[] };

type ICreateCourseReturn = ICreateCourse;

export const coursesQuery = (query?: IQueryParams) => {
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
        description,
        price,
        level,
        image,
        title,
        technologies,
        previous_price,
        lowest_30_days_price,
        duration,
        rating,
        rating_count,
        students_count,
        lecturers,
        active,
        progress,
      }: ICourse) => ({
        id,
        description,
        price,
        level,
        coverUrl: image,
        slug: title,
        category: technologies.map(({ name }: ITechnology) => name),
        priceSale: previous_price,
        lowest30DaysPrice: lowest_30_days_price,
        totalHours: duration / 60,
        ratingNumber: rating,
        totalReviews: rating_count,
        totalStudents: students_count,
        teachers: lecturers.map(
          ({ id: lecturerId, full_name, gender, image: lecturerImage }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            avatarUrl: lecturerImage,
            gender,
          }),
        ),
        active,
        progress: progress !== null ? progress * 100 : undefined,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useCourses = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = coursesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICourseProps[], count: data?.count, ...rest };
};

export const useCoursesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = coursesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateCourseReturn, AxiosError, ICreateCourse>(
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
