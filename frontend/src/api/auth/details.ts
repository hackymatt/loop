import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IGender } from "src/types/testimonial";
import { IUserType, IUserDetailsProps } from "src/types/user";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/details" as const;

export type IDetail = {
  first_name: string;
  last_name: string;
  email: string;
  user_type?: IUserType;
  phone_number: string | null;
  dob: string | null;
  gender: IGender;
  street_address: string | null;
  zip_code: string | null;
  city: string | null;
  country: string | null;
  image?: string | null;
};

type IDetailReturn = IDetail;

export const userDetailsQuery = () => {
  const url = endpoint;

  const queryFn = async () => {
    const response = await Api.get<IDetail>(url, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });
    const { data } = response;

    return { results: data };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useUserDetails = () => {
  const { queryKey, queryFn } = userDetailsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IUserDetailsProps, ...rest };
};

export const useUpdateUserDetails = () => {
  const queryClient = useQueryClient();
  return useMutation<IDetailReturn, AxiosError, IDetail>(
    async (variables) => {
      const result = await Api.put(endpoint, variables, {
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
