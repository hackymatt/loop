import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { UserType } from "src/types/user";
import { IMessageProp } from "src/types/message";
import { IQueryParams } from "src/types/query-params";

import { Api } from "../service";
import { getCsrfToken } from "../utils";

const endpoint = "/messages" as const;

type IProfile = {
  id: string;
  full_name: string;
  user_type: UserType;
};

type IMessage = {
  id: string;
  sender: IProfile;
  recipient: IProfile;
  subject: string;
  body: string;
  status: "NEW" | "READ";
  modified_at: string;
  created_at: string;
};

type ICreateMessage = Omit<
  IMessage,
  "id" | "sender" | "recipient" | "user_type" | "modified_at" | "created_at"
> & { recipient_id?: string; recipient_uuid?: string; recipient_type?: UserType };

type ICreateMessageReturn = ICreateMessage;

export const messagesQuery = (query?: IQueryParams) => {
  const path = endpoint;
  const pathParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${path}?${pathParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({ id, sender, recipient, subject, body, status, modified_at, created_at }: IMessage) => {
        const { id: senderId, full_name: senderName, user_type: senderType } = sender;
        const { id: recipientId, full_name: recipientName, user_type: recipientType } = recipient;
        return {
          id,
          subject,
          body,
          status,
          sender: {
            id: senderId,
            name: senderName,
            type: senderType,
          },
          recipient: {
            id: recipientId,
            name: recipientName,
            type: recipientType,
          },
          modifiedAt: modified_at,
          createdAt: created_at,
        };
      },
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { path, queryFn, queryKey: compact([path, pathParams]) };
};

export const useMessages = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = messagesQuery(query);
  const { data, ...rest } = useQuery({
    queryKey,
    queryFn,
    enabled,
  });
  return { data: data?.results as IMessageProp[], count: data?.count, ...rest };
};

export const useMessagesPagesCount = (query?: IQueryParams) => {
  const { queryKey, queryFn } = messagesQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.pagesCount, ...rest };
};

export const useCreateMessage = () => {
  const queryClient = useQueryClient();
  return useMutation<ICreateMessageReturn, AxiosError, ICreateMessage>(
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
