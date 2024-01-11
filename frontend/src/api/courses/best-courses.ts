import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICourseProps } from "src/types/course";
import { IGender } from "src/types/testimonial";

import { Api } from "../service";

const statsEndpoint = "/best-courses" as const;

type ILevel = "P" | "Ś" | "Z" | "E";

type ILecturer = {
  full_name: string;
  uuid: string;
  image: string | null;
  gender: IGender | null;
};

type ITechnology = {
  id: number;
  modified_at: string;
  created_at: string;
  name: string;
};

type ICourse = {
  id: number;
  technology: ITechnology;
  previous_price: string | null;
  lowest_30_days_price: string | null;
  duration: number;
  lecturers: ILecturer[];
  students_count: number;
  rating: number;
  rating_count: number;
  image: string;
  title: string;
  level: ILevel;
  price: string;
};

export const bestCoursesQuery = () => {
  const url = statsEndpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map((course: ICourse) => ({
      id: course.id,
      price: course.price,
      level: course.level,
      coverUrl: course.image,
      slug: course.title,
      category: course.technology.name,
      priceSale: course.previous_price,
      lowest30DaysPrice: course.lowest_30_days_price,
      totalHours: course.duration / 60,
      ratingNumber: course.rating,
      totalReviews: course.rating_count,
      totalStudents: course.students_count,
      teachers: course.lecturers.map((lecturer: ILecturer) => ({
        id: lecturer.uuid,
        name: lecturer.full_name,
        avatarUrl: lecturer.image,
      })),
    }));
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([url]) };
};

export const useBestCourses = () => {
  const { queryKey, queryFn } = bestCoursesQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseProps[], ...rest };
};
