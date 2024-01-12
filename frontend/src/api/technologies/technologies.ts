import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICourseByCategoryProps } from "src/types/course";

import { Api } from "../service";

const statsEndpoint = "/technologies?sort_by=-courses_count" as const;

type ITechnology = {
  id: number;
  courses_count: number;
  modified_at: string;
  created_at: string;
  name: string;
};

export const technologiesQuery = () => {
  const url = statsEndpoint;

  const queryFn = async () => {
    const { data } = await Api.get(url);
    const { results, records_count } = data;
    const modifiedResults = results.map(({ id, name, courses_count }: ITechnology) => ({
      id,
      name,
      totalStudents: courses_count,
    }));
    return { results: modifiedResults, count: records_count };
  };

  return { url, queryFn, queryKey: compact([url]) };
};

export const useTechnologies = () => {
  const { queryKey, queryFn } = technologiesQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ICourseByCategoryProps[], ...rest };
};
