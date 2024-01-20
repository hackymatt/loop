import { IQueryParams } from "src/types/queryParams";

export const formatQueryParams = (query?: IQueryParams) =>
  query
    ? Object.entries(query)
        .map((param) => param.join("="))
        .join("&")
    : "";
