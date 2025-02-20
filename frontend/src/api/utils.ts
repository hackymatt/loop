import { Api } from "./service";
import { GetApiResponse, ListApiResponse } from "./types";

export async function getListData<T>(queryUrl: string) {
  let data: ListApiResponse<T> = { results: [], records_count: 0, pages_count: 0 };

  try {
    const response = await Api.get<ListApiResponse<T>>(queryUrl);
    ({ data } = response);
  } catch (error) {
    if (error.response && (error.response.status === 400 || error.response.status === 404)) {
      data = { results: [], records_count: 0, pages_count: 0 };
    }
  }
  return data;
}

export async function getData<T>(queryUrl: string) {
  let data: GetApiResponse<T> = { result: <T>{} };

  try {
    const response = await Api.get<GetApiResponse<T>>(queryUrl);
    ({ data } = response);
  } catch (error) {
    if (error.response && (error.response.status === 400 || error.response.status === 404)) {
      data = { result: <T>{} };
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
