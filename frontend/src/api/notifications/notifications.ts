import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { INotificationProp } from "src/types/notification";

import { Api } from "../service";

const endpoint = "/notifications" as const;

type INotification = {
  id: string;
  title: string;
  lesson: string | null;
  description: string;
  status: "NEW" | "READ";
  url: string;
  icon: string;
  modified_at: string;
  created_at: string;
};

export const notificationsQuery = (query?: IQueryParams) => {
  const url = endpoint;
  const urlParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${url}?${urlParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({
        id,
        title,
        lesson,
        description,
        status,
        url: notificationUrl,
        icon,
        modified_at,
        created_at,
      }: INotification) => ({
        id,
        title,
        lesson,
        description,
        status,
        url: notificationUrl,
        icon,
        modifiedAt: modified_at,
        createdAt: created_at,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { url, queryFn, queryKey: compact([url, urlParams]) };
};

export const useNotifications = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = notificationsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as INotificationProp[], count: data?.count, ...rest };
};
