import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { ICourseProps } from "src/types/course";
import { IGender } from "src/types/testimonial";
import { IQueryParams } from "src/types/queryParams";

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

export const coursesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
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

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useCourses = (query?: IQueryParams) => {
  const { queryKey, queryFn } = coursesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseProps[], ...rest };
};

export const useCoursesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = coursesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
