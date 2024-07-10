import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IScheduleProp } from "src/types/course";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/lesson-schedules" as const;

type ILessonSchedule = {
  id: string;
  start_time: string;
  end_time: string;
  students_required: number;
};

export const lessonSchedulesQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async () => {
    let data;
    try {
      const response = await Api.get(queryUrl);
      ({ data } = response);
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        data = { results: [], records_count: 0, pages_count: 0 };
      }
    }
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, start_time, end_time, students_required }: ILessonSchedule) => ({
        id,
        startTime: start_time,
        endTime: end_time,
        studentsRequired: students_required,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessonSchedules = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonSchedulesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as IScheduleProp[], count: data?.count, ...rest };
};
