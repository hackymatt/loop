import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { ICourseDetailsProps } from "src/types/course";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/courses" as const;

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: IGender;
  lessons_count: number;
  rating: number | null;
  rating_count: number;
  title: string;
};

type ITechnology = {
  id: string;
  name: string;
  description: string;
};

type ITag = {
  id: string;
  name: string;
};

type ITopic = {
  id: string;
  name: string;
};

type ICandidate = {
  id: string;
  name: string;
};

type ILesson = {
  id: string;
  title: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  progress: number | null;
};

type IModule = {
  id: string;
  title: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  lessons: ILesson[];
  progress: number | null;
};

type ICourse = {
  id: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  duration: number;
  modules: IModule[];
  technologies: ITechnology[];
  tags: ITag[];
  topics: ITopic[];
  candidates: ICandidate[];
  lecturers: ILecturer[];
  students_count: number;
  rating: number | null;
  rating_count: number;
  progress: number | null;
  image: string;
  video: string | null;
  title: string;
  description: string;
  overview: string;
  level: "Podstawowy" | "Średniozaawansowany" | "Zaawansowany" | "Ekspert";
  active?: boolean;
};

type IEditCourse = Omit<
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
  | "tags"
  | "topics"
  | "candidates"
  | "progress"
> & { modules: string[]; tags: string[]; topics: string[]; candidates: string[] };

type IEditCourseReturn = IEditCourse;

type IDeleteCourse = { id: string };

type IDeleteCourseReturn = {};

export const courseQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<ICourseDetailsProps>> => {
    const { data } = await getData<ICourse>(queryUrl);
    const {
      id: courseId,
      description,
      overview,
      price,
      level,
      image,
      video,
      title,
      technologies,
      previous_price,
      lowest_30_days_price,
      duration,
      rating,
      rating_count,
      students_count,
      lecturers,
      tags,
      topics,
      candidates,
      modules,
      active,
      progress,
    } = data;

    const modifiedResults: ICourseDetailsProps = {
      id: courseId,
      description,
      overview,
      price,
      level,
      image,
      video,
      title,
      technologies,
      priceSale: previous_price,
      lowest30DaysPrice: lowest_30_days_price,
      totalHours: duration / 60,
      ratingNumber: rating,
      totalReviews: rating_count,
      totalStudents: students_count,
      teachers: lecturers.map(
        ({
          id: lecturerId,
          full_name,
          gender,
          image: lecturerImage,
          lessons_count,
          rating: lecturerRating,
          rating_count: lecturerRatingCount,
          title: lecturerTitle,
        }: ILecturer) => ({
          id: lecturerId,
          name: full_name,
          gender,
          image: lecturerImage,
          totalLessons: lessons_count,
          ratingNumber: lecturerRating,
          totalReviews: lecturerRatingCount,
          role: lecturerTitle,
        }),
      ),
      tags,
      topics,
      candidates,
      modules: modules.map(
        ({
          id: moduleId,
          title: moduleTitle,
          lowest_30_days_price: moduleLowest30DaysPrice,
          previous_price: modulePreviousPrice,
          price: modulePrice,
          lessons,
          progress: moduleProgress,
        }: IModule) => ({
          id: moduleId,
          title: moduleTitle,
          lowest30DaysPrice: moduleLowest30DaysPrice,
          priceSale: modulePreviousPrice,
          price: modulePrice,
          progress: moduleProgress !== null ? moduleProgress * 100 : null,
          lessons: lessons.map(
            ({
              id: lessonId,
              title: lessonTitle,
              lowest_30_days_price: lessonLowest30DaysPrice,
              previous_price: lessonPreviousPrice,
              price: lessonPrice,
              progress: lessonProgress,
            }: ILesson) => ({
              id: lessonId,
              title: lessonTitle,
              lowest30DaysPrice: lessonLowest30DaysPrice,
              priceSale: lessonPreviousPrice,
              price: lessonPrice,
              progress: lessonProgress !== null ? lessonProgress * 100 : null,
            }),
          ),
        }),
      ),
      active: active ?? true,
      progress: progress !== null ? progress * 100 : null,
    };

    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useCourse = (id: string) => {
  const { queryKey, queryFn } = courseQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditCourse = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditCourseReturn, AxiosError, IEditCourse>(
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

export const useDeleteCourse = () => {
  const queryClient = useQueryClient();
  return useMutation<IDeleteCourseReturn, AxiosError, IDeleteCourse>(
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
