import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { ICourseLessonProp } from "src/types/course";

import { Api } from "../service";

const endpoint = "/lessons" as const;

type ILecturer = {
  full_name: string;
  uuid: string;
  email: string;
  image: string | null;
  gender: IGender | null;
};

type ITechnology = {
  id: number;
  name: string;
};

type ILesson = {
  id: number;
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  technologies: ITechnology[];
  title: string;
  description: string;
  duration: number;
  github_url: string;
  price: string;
  active: boolean;
};
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
        category: technologies.map(({ name }: ITechnology) => name),
        teachers: lecturers.map(({ uuid, full_name, gender, image: lecturerImage }: ILecturer) => ({
          id: uuid,
          name: full_name,
          gender,
          avatarUrl: lecturerImage,
        })),
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

  return { url, queryFn, queryKey: compact([queryUrl]) };
};

export const useLesson = (id: string) => {
  const { queryKey, queryFn } = lessonQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseLessonProp, ...rest };
};
