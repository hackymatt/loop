import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { ICourseTeacherProp } from "src/types/course";

import { Api } from "../service";

const endpoint = "/lecturers" as const;

type ILesson = {
  id: string;
  title: string;
  price: number;
  previous_price?: number | null;
  lowest_30_days_price?: number | null;
};

type ILecturer = {
  id: string;
  full_name: string;
  description: string | null;
  email: string;
  linkedin_url: string | null;
  title: string | null;
  image: string | null;
  gender: IGender;
  students_count: number;
  rating: number | null;
  rating_count: number;
  lessons: ILesson[];
  lessons_duration: number;
  lessons_price: number;
  lessons_previous_price: number;
  lessons_lowest_30_days_price: number;
};

export const lecturerQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<ILecturer>(queryUrl);
      const { data } = response;
      const {
        id: teacherId,
        full_name,
        description,
        email,
        linkedin_url,
        title,
        image,
        gender,
        students_count,
        rating,
        rating_count,
        lessons,
        lessons_duration,
        lessons_price,
        lessons_previous_price,
        lessons_lowest_30_days_price,
      } = data;
      modifiedResults = {
        id: teacherId,
        name: full_name,
        description,
        linkedinUrl: linkedin_url,
        email,
        role: title,
        avatarUrl: image,
        gender,
        totalStudents: students_count,
        ratingNumber: rating,
        totalReviews: rating_count,
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
        totalHours: lessons_duration / 60,
        lessonsPrice: lessons_price,
        lessonsPreviousPrice: lessons_previous_price,
        lessonsLowest30DaysPrice: lessons_lowest_30_days_price,
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

export const useLecturer = (id: string) => {
  const { queryKey, queryFn } = lecturerQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICourseTeacherProp, ...rest };
};
