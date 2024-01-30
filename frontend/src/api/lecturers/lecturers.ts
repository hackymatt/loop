import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { ITeamMemberProps } from "src/types/team";
import { IQueryParams } from "src/types/queryParams";

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
};

export const lecturersQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count } = data;
    const modifiedResults = results.map(
      ({ uuid, full_name, email, user_title, image, gender, rating }: ILecturer) => ({
        id: uuid,
        name: full_name,
        email,
        role: user_title,
        photo: image,
        gender,
        ratingNumber: rating,
      }),
    );
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useLecturers = (query?: IQueryParams) => {
  const { queryKey, queryFn } = lecturersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITeamMemberProps[], ...rest };
};
