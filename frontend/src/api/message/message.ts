import { AxiosError } from "axios";
import { compact } from "lodash-es";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

import { UserType } from "src/types/user";
import { IMessageProp } from "src/types/message";

import { Api } from "../service";
import { getCsrfToken } from "../utils/csrf";

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

type IEditMessage = Omit<
  IMessage,
  "id" | "sender" | "recipient" | "user_type" | "modified_at" | "created_at"
>;

type IEditMessageReturn = IEditMessage;

export const messageQuery = (id: string) => {
  const url = endpoint;
  const queryUrl = `${url}/${id}`;

  const queryFn = async () => {
    let modifiedResults;
    try {
      const response = await Api.get<IMessage>(queryUrl);
      const { data } = response;
      const {
        id: messageId,
        subject,
        body,
        status,
        sender,
        recipient,
        modified_at,
        created_at,
      } = data;

      const { id: senderId, full_name: senderName, user_type: senderType } = sender;
      const { id: recipientId, full_name: recipientName, user_type: recipientType } = recipient;

      modifiedResults = {
        id: messageId,
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
    } catch (error) {
      if (error.response && (error.response.status === 400 || error.response.status === 404)) {
        modifiedResults = {};
      }
    }
    return { results: modifiedResults };
  };

  return { url, queryFn, queryKey: compact([endpoint, id]) };
};

export const useMessage = (id: string) => {
  const { queryKey, queryFn } = messageQuery(id);
  const { data, ...rest } = useQuery({ queryKey, queryFn });
  return { data: data?.results as any as IMessageProp, ...rest };
};
export const useEditMessage = (id: string) => {
  const queryClient = useQueryClient();
  const url = `${endpoint}/${id}`;
  return useMutation<IEditMessageReturn, AxiosError, IEditMessage>(
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
