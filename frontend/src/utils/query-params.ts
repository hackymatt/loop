import { IQueryParams } from "src/types/query-params";

export const formatQueryParams = (query?: IQueryParams) =>
  query
    ? Object.entries(query)
        .map((param) => param.join("="))
        .join("&")
    : "";
