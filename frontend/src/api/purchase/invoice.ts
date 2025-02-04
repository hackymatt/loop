import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { IInvoiceProp } from "src/types/invoice";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

const endpoint = "/invoice" as const;

type ICustomer = {
  id: number;
  full_name: string;
  street_address: string;
  city: string;
  zip_code: string;
  country: string;
};

type IItem = {
  id: number;
  name: string;
  price: number;
};

type IPayment = {
  id: number;
  amount: number;
  status: "Zapłacono" | "Do zapłaty";
  method: "Przelewy24" | "Przelew";
  account: string;
};

type IInvoice = {
  customer: ICustomer;
  items: IItem[];
  payment: IPayment;
};

type ICreateInvoice = IInvoice;

type ICreateInvoiceReturn = ICreateInvoice;

export const invoiceQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IInvoice>(queryUrl);
      const { data } = response;
      const { customer, items, payment } = data;
      const {
        full_name: name,
        street_address: streetAddress,
        zip_code: zipCode,
        ...rest
      } = customer;

      modifiedResults = {
        customer: { ...rest, name, streetAddress, zipCode },
        items,
        payment,
      };
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useInvoice = (id: string) => {
  const { queryKey, queryFn } = invoiceQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IInvoiceProp, ...rest };
};

export const useCreateInvoice = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateInvoiceReturn, AxiosError, ICreateInvoice>(
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
