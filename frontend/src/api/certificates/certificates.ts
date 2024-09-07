import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { ICertificateProps } from "src/types/certificate";

import { Api } from "../service";

const endpoint = "/certificate" as const;

type ICertificate = {
  id: string;
  type: string;
  title: string;
  completed_at: string;
};

export const certificatesQuery = (query?: IQueryParams) => {
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
    const modifiedResults = results.map(({ id, type, title, completed_at }: ICertificate) => ({
      id,
      type,
      title,
      completedAt: completed_at,
    }));

    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([endpoint, urlParams]) };
};

export const useCertificates = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = certificatesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as ICertificateProps[], count: data?.count, ...rest };
};

export const useCertificatesPagesCount = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = certificatesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.pagesCount, ...rest };
};
