import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICourseProps } from "src/types/course";
import { IGender } from "src/types/testimonial";

import { Api } from "../service";

const endpoint = "/courses" as const;

type ILevel = "P" | "Ś" | "Z" | "E";

type ILecturer = {
  full_name: string;
  uuid: string;
  email: string;
  image: string | null;
  gender: IGender | null;
  lessons_count: number;
  rating: number | null;
  rating_count: number;
  user_title: string | null;
};

type ITechnology = {
  id: number;
  name: string;
};

type ISkill = {
  id: number;
  name: string;
};

type ITopic = {
  id: number;
  name: string;
};

type ILesson = {
  id: number;
  title: string;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
};

type ICourse = {
  id: number;
  level: ILevel;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  is_bestseller: boolean;
  duration: number;
  lessons: ILesson[];
  technologies: ITechnology[];
  skills: ISkill[];
  topics: ITopic[];
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  image: string;
  video: string | null;
  title: string;
  description: string;
  active: boolean;
};

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
        lessons,
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
            uuid,
            full_name,
            gender,
            image: lecturerImage,
            lessons_count,
            rating: lecturerRating,
            rating_count: lecturerRatingCount,
            user_title,
          }: ILecturer) => ({
            id: uuid,
            name: full_name,
            gender,
            avatarUrl: lecturerImage,
            totalCourses: lessons_count,
            ratingNumber: lecturerRating,
            totalReviews: lecturerRatingCount,
            role: user_title,
          }),
        ),
        skills: skills.map((skill: ISkill) => skill.name),
        learnList: topics.map((topic: ITopic) => topic.name),
        lessons: lessons.map(
          ({
            id: lessonId,
            title: titleId,
            lowest_30_days_price: lessonLowest30DaysPrice,
            previous_price: lessonPreviousPrice,
            price: lessonPrice,
          }: ILesson) => ({
            id: lessonId,
            title: titleId,
            lowest30DaysPrice: lessonLowest30DaysPrice,
            priceSale: lessonPreviousPrice,
            price: lessonPrice,
          }),
        ),
      };
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useCourse = (id: string) => {
  const { queryKey, queryFn } = courseQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseProps, ...rest };
};
