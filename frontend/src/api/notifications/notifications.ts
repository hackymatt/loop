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
  subtitle: string | null;
  description: string;
  status: "NEW" | "READ";
  path: string | null;
  icon: string;
  modified_at: string;
  created_at: string;
};

export const notificationsQuery = (query?: IQueryParams) => {
  const path = endpoint;
  const pathParams = formatQueryParams(query);

  const queryFn = async () => {
    const { data } = await Api.get(`${path}?${pathParams}`);
    const { results, records_count, pages_count } = data;
    const modifiedResults = results.map(
      ({
        id,
        title,
        subtitle,
        description,
        status,
        path: notificationUrl,
        icon,
        modified_at,
        created_at,
      }: INotification) => ({
        id,
        title,
        subtitle: subtitle === null ? undefined : subtitle,
        description,
        status,
        path: notificationUrl === null ? undefined : notificationUrl,
        icon,
        modifiedAt: modified_at,
        createdAt: created_at,
      }),
    );
    return { results: modifiedResults, count: records_count, pagesCount: pages_count };
  };

  return { path, queryFn, queryKey: compact([path, pathParams]) };
};

export const useNotifications = (
  query?: IQueryParams,
  enabled: boolean = true,
  refetchInterval: number = 0,
) => {
  const { queryKey, queryFn } = notificationsQuery(query);
  const { data, ...rest } = useQuery({
    queryKey,
    queryFn,
    enabled,
    refetchInterval,
  });
  return { data: data?.results as INotificationProp[], count: data?.count, ...rest };
};
