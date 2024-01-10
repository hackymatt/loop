import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICourseProps } from "src/types/course";

import { Api } from "../service";

const statsEndpoint = "/best-courses" as const;

type ILevel = "P" | "Ś" | "Z" | "E";

type ILecturer = {
  full_name: string;
  uuid: string;
  image: string | null;
};

type ITechnology = {
  id: 1;
  modified_at: "2024-01-09T13:39:27.256007Z";
  created_at: "2024-01-09T13:39:27.256040Z";
  name: "Javascript";
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
      price: course.previous_price ? course.previous_price : course.price,
      level: course.level,
      coverUrl: course.image,
      slug: course.title,
      category: course.technology.name,
      priceSale: course.previous_price ? course.price : course.previous_price,
      totalHours: course.duration / 17,
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
