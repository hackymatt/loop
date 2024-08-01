import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { ICertificateProps } from "src/types/certificate";

import { Api } from "../service";

const endpoint = "/certificate" as const;

type ICertificate = {
  reference_number: string;
  lesson_title: string;
  teacher_name: string;
  student_name: string;
  lesson_duration: string;
  completion_date: string;
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
        lesson_title,
        lesson_duration,
        student_name,
        teacher_name,
        completion_date,
        authorized,
      } = data;
      modifiedResults = {
        referenceNumber: reference_number,
        lessonTitle: lesson_title,
        lessonDuration: lesson_duration,
        studentName: student_name,
        teacherName: teacher_name,
        completionDate: completion_date,
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
