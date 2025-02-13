import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IGender } from "src/types/testimonial";
import { ITeamMemberProps } from "src/types/team";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";

const endpoint = "/others" as const;

type IOther = {
  id: string;
  full_name: string;
  image: string | null;
  gender: IGender;
};

export const othersQuery = (query?: IQueryParams) => {
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
    const modifiedResults = results.map(({ id, full_name, image, gender }: IOther) => ({
      id,
      name: full_name,
      avatarUrl: image,
      gender,
    }));
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useOthers = (query?: IQueryParams) => {
  const { queryKey, queryFn } = othersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as ITeamMemberProps[], count: data?.count, ...rest };
};

export const useOthersPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = othersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};
