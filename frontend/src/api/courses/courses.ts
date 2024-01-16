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
  description: string;
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

export const coursesQuery = (page?: number, sort?: string) => {
  const url = endpoint;

  const queryFn = async () => {
    const urlParams = [`page=${page ?? 1}`, `sort_by=${sort ?? "-students_count"}`];
    const { data } = await Api.get(`${url}?${urlParams.join("&")}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({
        id,
        description,
        price,
        level,
        image,
        title,
        technology,
        previous_price,
        lowest_30_days_price,
        duration,
        rating,
        rating_count,
        students_count,
        lecturers,
      }: ICourse) => {
        const { name } = technology;
        return {
          id,
          description,
          price,
          level,
          coverUrl: image,
          slug: title,
          category: name,
          priceSale: previous_price,
          lowest30DaysPrice: lowest_30_days_price,
          totalHours: duration / 60,
          ratingNumber: rating,
          totalReviews: rating_count,
          totalStudents: students_count,
          teachers: lecturers.map(({ uuid, full_name, image: lecturerImage }: ILecturer) => ({
            id: uuid,
            name: full_name,
            avatarUrl: lecturerImage,
          })),
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, page, sort]) };
};

export const useCourses = (page?: number, sort?: string) => {
  const { queryKey, queryFn } = coursesQuery(page, sort);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseProps[], ...rest };
};

export const useCoursesPagesCount = () => {
  const { queryKey, queryFn } = coursesQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
