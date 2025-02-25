import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IUserProps } from "src/types/user";

import { Api } from "../service";
import { GetQueryResponse } from "../types";
import { getData, getCsrfToken } from "../utils";

const endpoint = "/personal-data" as const;

export type IUser = {
  uuid: string;
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
};

type IEditUser = Omit<IUser, "uuid" | "gender"> & { gender: string };
type IEditUserReturn = IEditUser;

export const userDetailsQuery = () => {
  const url = endpoint;

  const queryFn = async (): Promise<GetQueryResponse<IUserProps>> => {
    const { data } = await getData<IUser>(url, {
      headers: {
        "X-CSRFToken": getCsrfToken(),
      },
    });

    const {
      uuid,
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
    } = data;

    const modifiedData: IUserProps = {
      id: uuid,
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
    };

    return { results: { ...modifiedData, id: uuid } };
  };

  return { url, queryFn, queryKey: compact([endpoint]) };
};

export const useUserDetails = (enabled: boolean = true) => {
  const { queryKey, queryFn } = userDetailsQuery();
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, ...rest };
};

export const useUpdateUserDetails = () => {
  const queryClient = useQueryClient();
  return useMutation<IEditUserReturn, AxiosError, IEditUser>(
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
