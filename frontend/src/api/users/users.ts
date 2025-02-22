import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IUserDetailsProps } from "src/types/user";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { ListQueryResponse } from "../types";
import { getListData, getCsrfToken } from "../utils";

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

type ICreateUser = Omit<IUser, "id" | "image" | "active" | "created_at">;

type ICreateUserReturn = ICreateUser;

export const usersQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);
  const queryUrl = urlParams ? `${url}?${urlParams}` : url;

  const queryFn = async (): Promise<ListQueryResponse<IUserDetailsProps[]>> => {
    const { results, records_count, pages_count } = await getListData<IUser>(queryUrl);

    const modifiedResults: IUserDetailsProps[] = (results ?? []).map(
      ({
        id,
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
      }: IUser) => ({
        id,
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
      }),
    );

    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useUsers = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = usersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results, count: data?.count, ...rest };
};

export const useUsersPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = usersQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateUserReturn, AxiosError, ICreateUser>(
    async (variables) => {
      const result = await Api.post(endpoint, variables, {
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
