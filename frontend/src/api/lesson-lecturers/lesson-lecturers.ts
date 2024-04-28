import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { ITeamMemberProps } from "src/types/team";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/lesson-lecturers" as const;

type ILecturer = {
  uuid: string;
  first_name: string;
  email: string;
  image: string | null;
  gender: IGender;
};

type ILessonLecturer = {
  id: number;
  lecturer: ILecturer;
};

export const lessonLecturersQuery = (query?: IQueryParams) => {
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
    const modifiedResults = results.map(({ lecturer }: ILessonLecturer) => {
      const { uuid, first_name, email, gender, image } = lecturer;
      return {
        id: uuid,
        name: first_name,
        gender,
        email,
        avatarUrl: image,
      };
    });
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useLessonLecturers = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lessonLecturersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITeamMemberProps[], count: data?.count, ...rest };
};
