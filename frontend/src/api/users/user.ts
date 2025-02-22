import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IUserDetailsProps } from "src/types/user";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/users" as const;

export type IUser = {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string | null;
  dob: string | null;
  gender: "Mężczyzna" | "Kobieta" | "Inne";
  street_address: string | null;
  zip_code: string | null;
  city: string | null;
  country: string | null;
  image: string | null;
  active: boolean;
  user_type: "Admin" | "Wykładowca" | "Student" | "Inny";
  created_at: string;
};

type IEditUser = Omit<IUser, "id" | "active" | "image" | "created_at" | "gender" | "user_type"> & {
  gender: string;
  user_type: string;
};

type IEditUserReturn = IEditUser;

export const userQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async (): Promise<GetQueryResponse<IUserDetailsProps>> => {
    const { data } = await getData<IUser>(queryUrl);

    const {
      id: userId,
      first_name,
      last_name,
      email,
      phone_number,
      dob,
      gender,
      street_address,
      zip_code,
      city,
      country,
      image,
      active,
      user_type,
      created_at,
    } = data;

    const modifiedData = {
      id: userId,
      firstName: first_name,
      lastName: last_name,
      email,
      phoneNumber: phone_number,
      dob,
      gender,
      streetAddress: street_address,
      zipCode: zip_code,
      city,
      country,
      image,
      active,
      userType: user_type,
      createdAt: created_at,
    };

    return { results: modifiedData };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useUser = (id: string) => {
  const { queryKey, queryFn } = userQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results, ...rest };
};

export const useEditUser = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditUserReturn, AxiosError, IEditUser>(
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
