import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICourseProps } from "src/types/course";
import { IGender } from "src/types/testimonial";

import { Api } from "../service";

const endpoint = "/best-courses" as const;

type ILevel = "P" | "Ś" | "Z" | "E";

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

type ICourse = {
  id: number;
  price: number;
  previous_price: number | null;
  lowest_30_days_price: number | null;
  is_bestseller: boolean;
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
};

export const bestCoursesQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map(
      ({
        id,
        price,
        level,
        image,
        title,
        technologies,
        previous_price,
        lowest_30_days_price,
        is_bestseller,
        duration,
        rating,
        rating_count,
        students_count,
        lecturers,
      }: ICourse) => ({
        id,
        price,
        level,
        coverUrl: image,
        slug: title,
        category: technologies.map(({ name }: ITechnology) => name),
        priceSale: previous_price,
        lowest30DaysPrice: lowest_30_days_price,
        totalHours: duration / 60,
        bestSeller: is_bestseller,
        ratingNumber: rating,
        totalReviews: rating_count,
        totalStudents: students_count,
        teachers: lecturers.map(({ uuid, full_name, image: lecturerImage }: ILecturer) => ({
          id: uuid,
          name: full_name,
          avatarUrl: lecturerImage,
        })),
      }),
    );
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useBestCourses = () => {
  const { queryKey, queryFn } = bestCoursesQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseProps[], count: data?.count, ...rest };
};
