import { Api } from "./service";
import { ApiResponse } from "./types";

export async function getData<T>(queryUrl: string) {
  let data: ApiResponse<T> = { results: [], records_count: 0, pages_count: 0 };

  try {
    const response = await Api.get<ApiResponse<T>>(queryUrl);
    ({ data } = response);
  } catch (error) {
    if (error.response && (error.response.status === 400 || error.response.status === 404)) {
      data = { results: [], records_count: 0, pages_count: 0 };
    }
  }
  return data;
}
