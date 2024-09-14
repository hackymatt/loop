import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { IScheduleProp } from "src/types/course";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/schedules" as const;

type ILesson = {
  id: string;
  title: string;
};

type IStudent = {
  id: string;
  full_name: string;
  gender: IGender;
  image: string | null;
};

type ISchedule = {
  id: string;
  start_time: string;
  end_time: string;
  lesson: ILesson | null;
  meeting_url: string | null;
  students: IStudent[];
};

type ICreateSchedule = Omit<ISchedule, "id" | "lesson" | "meeting_url" | "students">;
type ICreateScheduleReturn = ICreateSchedule;
export const schedulesQuery = (query?: IQueryParams) => {
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
      ({ id, start_time, end_time, lesson, meeting_url, students }: ISchedule) => ({
        id,
        startTime: start_time,
        endTime: end_time,
        lesson,
        meetingUrl: meeting_url,
        students: students.map(({ id: studentId, full_name, gender, image }: IStudent) => ({
          id: studentId,
          name: full_name,
          gender,
          image,
        })),
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useSchedules = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = schedulesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as IScheduleProp[], count: data?.count, ...rest };
};

export const useCreateSchedule = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateScheduleReturn, AxiosError, ICreateSchedule>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
