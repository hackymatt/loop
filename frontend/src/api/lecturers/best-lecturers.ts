import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { ITeamMemberProps } from "src/types/team";

import { Api } from "../service";

const endpoint = "/best-lecturers" as const;

type ILecturer = {
  id: string;
  full_name: string;
  user_title: string | null;
  image: string | null;
  gender: IGender;
};

export const bestLecturersQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map(
      ({ id, full_name, user_title, image, gender }: ILecturer) => ({
        id,
        name: full_name,
        role: user_title,
        photo: image,
        gender,
      }),
    );
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useBestLecturers = () => {
  const { queryKey, queryFn } = bestLecturersQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITeamMemberProps[], count: data?.count, ...rest };
};
