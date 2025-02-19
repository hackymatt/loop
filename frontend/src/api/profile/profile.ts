import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/profile-data" as const;

type ILecturerProfile = {
  title: string;
  linkedin_url: string;
  description: string;
};

type IEditLecturerProfile = ILecturerProfile;

type IEditLecturerProfileReturn = IEditLecturerProfile;

export const userProfileQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const response = await Api.get<IEditLecturerProfile>(url, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    const { data } = response;

    return { results: data };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useUserProfile = () => {
  const { queryKey, queryFn } = userProfileQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditUserProfile = () => {
  const queryClient = useQueryClient();
  const url = endpoint;
  return useMutation<IEditLecturerProfileReturn, AxiosError, IEditLecturerProfile>(
    async (variables) => {
      const result = await Api.put(url, variables, {
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      return result.data;
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: [endpoint] });
      },
    },
  );
};
