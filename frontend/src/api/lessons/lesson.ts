import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { ICourseLessonProp } from "src/types/course";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/lessons" as const;

type ILecturer = {
  full_name: string;
  id: string;
  image: string | null;
  gender: IGender | null;
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
  active: boolean;
};

type IEditLesson = Omit<
  ILesson,
  "id" | "lecturers" | "students_count" | "rating" | "rating_count" | "technologies"
> & { technologies: string[] };
type IEditLessonReturn = IEditLesson;
export const lessonQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<ILesson>(queryUrl);
      const { data } = response;
      const {
        id: lessonId,
        lecturers,
        students_count,
        rating,
        rating_count,
        title,
        description,
        duration,
        github_url,
        price,
        active,
        technologies,
      } = data;

      modifiedResults = {
        id: lessonId,
        title,
        description,
        price,
        duration,
        ratingNumber: rating,
        totalReviews: rating_count,
        totalStudents: students_count,
        technologies,
        teachers: lecturers.map(
          ({ id: lecturerId, full_name, gender, image: lecturerImage }: ILecturer) => ({
            id: lecturerId,
            name: full_name,
            gender,
            avatarUrl: lecturerImage,
          }),
        ),
        githubUrl: github_url,
        active,
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

export const useLesson = (id: string) => {
  const { queryKey, queryFn } = lessonQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseLessonProp, ...rest };
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
