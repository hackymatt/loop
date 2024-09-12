import { compact } from "lodash-es";
import { useQuery } from "@tanstack/react-query";

import { formatQueryParams } from "src/utils/query-params";

import { IQueryParams } from "src/types/query-params";
import { INotificationProp } from "src/types/notification";

import { Api } from "../service";

const endpoint = "/notifications" as const;

const test = [
  {
    id: "1",
    title: "Gratulacje! Otrzymujesz nowe certyfikaty",
    subtitle: "",
    target: "s",
    description: "Poniżej znajduje się lista nowo otrzymanych certyfikatów…",
    status: "NEW" as "NEW" | "READ",
    path: "/account/certificates?sort_by=-completed_at&page_size=10&completed_at=2024-09-07",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:certificate",
  },
  {
    id: "1",
    title: "Nowy zapis",
    subtitle: "Podstawy React",
    target: "l",
    description:
      "Lista potencjalnych uczestników lekcji, która planowo odbędzie się {{subtitle_start_time}} (PL) została powiększona o nowy zapis studenta {{student_full_name}}. Aktualna liczba uczestników: {{students_count}}.",
    status: "NEW" as "NEW" | "READ",
    path: null,
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:invoice-text-new",
  },
  {
    id: "1",
    title: "Brak realizacji szkolenia",
    subtitle: "Podstawy React",
    target: "s",
    description:
      "Niestety, nie udało się zrealizować lekcję, która planowo odbyłaby się {{subtitle_start_time}} (PL) i byłaby prowadzona przez {{lecturer_full_name}} z powodu niewystarczającej ilości zapisów.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/subtitles?sort_by=-created_at&page_size=10&subtitle_title=Wstęp+do+React",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:school",
  },
  {
    id: "1",
    title: "Potwierdzenie realizacji szkolenia",
    subtitle: "Podstawy React",
    target: "s",
    description:
      "Udało się! Potwierdzamy realizację lekcji, która odbędzie się {{subtitle_start_time}} (PL) i będzie prowadzona przez {{lecturer_full_name}}.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/subtitles?sort_by=-created_at&page_size=10&subtitle_title=Wstęp+do+React",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:school",
  },
  {
    id: "1",
    title: "Brak realizacji szkolenia",
    subtitle: "Podstawy React",
    target: "l",
    description:
      "Niestety, nie udało się zrealizować lekcję, która planowo odbyłaby się {{subtitle_start_time}} (PL) z powodu niewystarczającej ilości zapisów.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/teacher/calendar",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:school",
  },
  {
    id: "1",
    title: "Potwierdzenie realizacji szkolenia",
    subtitle: "Podstawy React",
    target: "l",
    description:
      "Udało się! Potwierdzamy realizację lekcji, która odbędzie się {{subtitle_start_time}} (PL).",
    status: "NEW" as "NEW" | "READ",
    path: "/account/teacher/calendar",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:school",
  },
  {
    id: "1",
    title: "Prośba o ocenę szkolenia",
    subtitle: "Podstawy React",
    target: "s",
    description:
      "Proszę daj nam znać jak nam poszło. Dodaj recenzję lekcji, która odbyła się {{subtitle_start_time}} (PL) i była prowadzona przez {{lecturer_full_name}}.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/reviews?review_status_exclude=brak&page_size=10&subtitle_title=Wstęp+do+React",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:rate-review",
  },
  {
    id: "1",
    title: "Twoja lekcja została odwołana",
    subtitle: "Podstawy React",
    target: "s",
    description:
      "Przepraszamy za zmianę planów. Lekcja, która planowo miała się odbyć {{subtitle_start_time}} (PL) została odwołana przez prowadzącego {{lecturer_full_name}}.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/subtitles?sort_by=-created_at&page_size=10&subtitle_title=Wstęp+do+React",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:calendar-remove",
  },
  {
    id: "1",
    title: "Nowa recenzja",
    subtitle: "Podstawy React",
    target: "l",
    description: "Otrzymano nową recenzję. Ocena 5.0, komentarz: brak.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/teacher/reviews/?sort_by=-created_at&page_size=10&subtitle_id=1",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:star-rate",
  },
  {
    id: "1",
    title: "Zostałeś nauczycielem",
    subtitle: "",
    target: "l",
    description:
      "Zostałeś nauczycielem, w celu prowadzenia szkoleń uzupełnij swój profil instruktora.",
    status: "NEW" as "NEW" | "READ",
    path: "/account/teacher/profile",
    modified_at: "2024-09-08T13:13:31.710729Z",
    created_at: "2024-09-08T13:13:31.710729Z",
    icon: "mdi:teach",
  },
];

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
    // const { data } = await Api.get(`${path}?${pathParams}`);
    // const { results, records_count, pages_count } = data;
    const modifiedResults = test.map(
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
    return { results: modifiedResults, count: test.length, pagesCount: 1 };
  };

  return { path, queryFn, queryKey: compact([path, pathParams]) };
};

export const useNotifications = (query?: IQueryParams, enabled: boolean = true) => {
  const { queryKey, queryFn } = notificationsQuery(query);
  const { data, ...rest } = useQuery({ queryKey, queryFn, enabled });
  return { data: data?.results as INotificationProp[], count: data?.count, ...rest };
};
