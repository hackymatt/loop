export interface GetApiResponse<T = any> {
  data: T;
}

export interface ListApiResponse<T = any> {
  results: T[];
  records_count: number;
  pages_count: number;
}

export interface GetQueryResponse<T = any> {
  results: T;
}

export interface ListQueryResponse<T = any> extends GetQueryResponse<T> {
  count: number;
  pagesCount: number;
}
