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

function getCookie(name: string) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i += 1) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const getCsrfToken = () => getCookie("csrftoken");
