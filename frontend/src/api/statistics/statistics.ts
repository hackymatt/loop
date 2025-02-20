import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IStatistics } from "src/types/statistics";

import { getData } from "../utils";
import { GetQueryResponse } from "../types";

const endpoint = "/stats" as const;

type IStats = {
  students_count: number;
  course_count: number;
  lessons_count: number;
  technology_count: number;
  lecturers_count: number;
  purchase_count: number;
  hours_sum: number;
  rating: number;
  rating_count: number;
};

export const statisticsQuery = () => {
  const url = endpoint;

  const queryFn = async (): Promise<GetQueryResponse<IStatistics>> => {
    const { result } = await getData<IStats>(url);
    const {
      students_count,
      course_count,
      lessons_count,
      technology_count,
      lecturers_count,
      purchase_count,
      hours_sum,
      rating,
      rating_count,
    } = result;
    const modifiedData = {
      studentsCount: students_count,
      courseCount: course_count,
      lessonsCount: lessons_count,
      technologyCount: technology_count,
      lecturersCount: lecturers_count,
      purchaseCount: purchase_count,
      hoursSum: hours_sum,
      rating,
      ratingCount: rating_count,
    };
    return { results: modifiedData };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useStatistics = () => {
  const { queryKey, queryFn } = statisticsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};
