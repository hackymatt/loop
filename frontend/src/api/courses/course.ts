import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { ICourseProps } from "src/types/course";
import { IGender } from "src/types/testimonial";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/courses" as const;

type ILevel = "P" | "Ś" | "Z" | "E";

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: IGender | null;
  lessons_count: number;
  rating: number | null;
  rating_count: number;
  user_title: string | null;
};

type ITechnology = {
  id: string;
  name: string;
};

type ISkill = {
  id: string;
  name: string;
};

type ITopic = {
  id: string;
  name: string;
};

type ILesson = {
  id: string;
  title: string;
  price: number;
  previous_price?: number | null;
  lowest_30_days_price?: number | null;
  progress: number | null;
};

type IModule = {
  id: string;
  title: string;
  price: number;
  previous_price?: number | null;
  lowest_30_days_price?: number | null;
  lessons: ILesson[];
  progress: number | null;
};

type ICourse = {
  id: string;
  level: ILevel;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  duration: number;
  modules: IModule[];
  technologies: ITechnology[];
  skills: ISkill[];
  topics: ITopic[];
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  image: string;
  video?: string;
  title: string;
  description: string;
  active: boolean;
  progress: number | null;
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
  | "skills"
  | "topics"
  | "progress"
> & { modules: string[]; skills: string[]; topics: string[] };

type IEditCourseReturn = IEditCourse;

type IDeleteCourse = { id: string };

type IDeleteCourseReturn = {};

export const courseQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<ICourse>(queryUrl);
      const { data } = response;
      const {
        id: courseId,
        description,
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
        skills,
        topics,
        modules,
        active,
        progress,
      } = data;

      modifiedResults = {
        id: courseId,
        description,
        price,
        level,
        coverUrl: image,
        video,
        slug: title,
        category: technologies.map(({ name }: ITechnology) => name),
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
            user_title,
          }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            gender,
            avatarUrl: lecturerImage,
            totalLessons: lessons_count,
            ratingNumber: lecturerRating,
            totalReviews: lecturerRatingCount,
            role: user_title,
          }),
        ),
        skills: skills.map((skill: ISkill) => skill.name),
        learnList: topics.map((topic: ITopic) => topic.name),
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
            progress: moduleProgress !== null ? moduleProgress * 100 : undefined,
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
                progress: lessonProgress !== null ? lessonProgress * 100 : undefined,
              }),
            ),
          }),
        ),
        active,
        progress: progress !== null ? progress * 100 : undefined,
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

export const useCourse = (id: string) => {
  const { queryKey, queryFn } = courseQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseProps, ...rest };
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
