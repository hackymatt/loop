import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { ITeamMemberProps } from "src/types/team";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/lecturers" as const;

type ILecturer = {
  uuid: string;
  full_name: string;
  email: string;
  user_title: string | null;
  image: string | null;
  gender: IGender;
  rating: number | null;
  rating_count: number;
  lessons_count: number;
};

export const lecturersQuery = (query?: IQueryParams) => {
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
      ({
        uuid,
        full_name,
        email,
        user_title,
        image,
        gender,
        rating,
        rating_count,
        lessons_count,
      }: ILecturer) => ({
        id: uuid,
        name: full_name,
        email,
        role: user_title,
        photo: image,
        gender,
        ratingNumber: rating,
        totalReviews: rating_count,
        totalLessons: lessons_count,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useLecturers = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lecturersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITeamMemberProps[], ...rest };
};

export const useLecturersPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lecturersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
