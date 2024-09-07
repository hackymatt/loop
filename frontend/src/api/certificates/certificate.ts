import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICertificateProps } from "src/types/certificate";

import { Api } from "../service";

const endpoint = "/certificate" as const;

type ICertificate = {
  reference_number: string;
  type: string;
  title: string;
  duration: string;
  student_full_name: string;
  completed_at: string;
  authorized?: boolean;
};

export const certificateQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<ICertificate>(queryUrl);

      const { data } = response;
      const {
        reference_number,
        type,
        title,
        duration,
        student_full_name,
        completed_at,
        authorized,
      } = data;
      modifiedResults = {
        referenceNumber: reference_number,
        type,
        title,
        duration,
        studentName: student_full_name,
        completedAt: completed_at,
        isAuthorized: authorized,
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

export const useCertificate = (id: string) => {
  const { queryKey, queryFn } = certificateQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as ICertificateProps, ...rest };
};
