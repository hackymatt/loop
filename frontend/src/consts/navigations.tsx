import { paths } from "src/routes/paths";

import Iconify from "src/components/iconify";

import { MessageType } from "src/types/message";
import { ReviewStatus } from "src/types/purchase";

const userNavigation = [
  {
    title: "Dane osobowe",
    path: paths.account.personal,
    icon: <Iconify icon="carbon:user" />,
    children: [],
  },
  {
    title: "Zarządzaj kontem",
    path: paths.account.manage,
    icon: <Iconify icon="carbon:password" />,
    children: [],
  },
  {
    title: "Wiadomości",
    path: `${paths.account.messages}/?sort_by=-created_at&page_size=10&type=${MessageType.INBOX}`,
    icon: <Iconify icon="carbon:email" />,
    children: [],
  },
];

export const studentNavigation = [
  ...userNavigation,
  ...[
    {
      title: "Lekcje",
      path: `${paths.account.lessons}/?sort_by=-created_at&page_size=10`,
      icon: <Iconify icon="carbon:book" />,
      children: [],
    },
    {
      title: "Recenzje",
      path: `${paths.account.reviews}/?review_status_exclude=${ReviewStatus.brak}&page_size=10`,
      icon: <Iconify icon="carbon:review" />,
      children: [],
    },
    {
      title: "Certyfikaty",
      path: `${paths.account.certificates}/?sort_by=-completed_at&page_size=10`,
      icon: <Iconify icon="carbon:certificate" />,
      children: [],
    },
  ],
];

export const teacherNavigation = [
  ...userNavigation,
  ...[
    {
      title: "Profil instruktora",
      path: paths.account.teacher.profile,
      icon: <Iconify icon="carbon:user-profile" />,
      children: [],
    },
    {
      title: "Dane finansowe",
      path: paths.account.teacher.finance,
      icon: <Iconify icon="carbon:finance" />,
      children: [],
    },
    {
      title: "Nauczanie",
      path: `${paths.account.teacher.teaching}/?sort_by=title&page_size=10`,
      icon: <Iconify icon="carbon:education" />,
      children: [],
    },
    {
      title: "Terminarz",
      path: paths.account.teacher.calendar,
      icon: <Iconify icon="carbon:calendar" />,
      children: [],
    },
    {
      title: "Recenzje",
      path: `${paths.account.teacher.reviews}/?sort_by=-created_at&page_size=10`,
      icon: <Iconify icon="carbon:review" />,
      children: [],
    },
    {
      title: "Zarobki",
      path: `${paths.account.teacher.earnings}/?page_size=12`,
      icon: <Iconify icon="carbon:currency-dollar" />,
      children: [],
    },
  ],
];

export const adminNavigation = [
  ...userNavigation,
  ...[
    {
      title: "Kursy",
      path: paths.account.admin.courses.list,
      icon: <Iconify icon="carbon:book" />,
      children: [
        {
          title: "Spis kursów",
          path: `${paths.account.admin.courses.list}/?sort_by=title&page_size=10`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Umiejętności",
          path: `${paths.account.admin.courses.skills}/?sort_by=name&page_size=10`,
          icon: <Iconify icon="carbon:policy" />,
          children: [],
        },
        {
          title: "Tematy",
          path: `${paths.account.admin.courses.topics}/?sort_by=name&page_size=10`,
          icon: <Iconify icon="carbon:query" />,
          children: [],
        },
      ],
    },
    {
      title: "Moduły",
      path: `${paths.account.admin.modules.list}/?sort_by=title&page_size=10`,
      icon: <Iconify icon="carbon:notebook-reference" />,
      children: [],
    },
    {
      title: "Lekcje",
      path: paths.account.admin.lessons.list,
      icon: <Iconify icon="carbon:notebook" />,
      children: [
        {
          title: "Spis lekcji",
          path: `${paths.account.admin.lessons.list}/?sort_by=title&page_size=10`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Historia cen",
          path: `${paths.account.admin.lessons.priceHistory}/?sort_by=-created_at&page_size=10`,
          icon: <Iconify icon="carbon:chart-line" />,
          children: [],
        },
        {
          title: "Technologie",
          path: `${paths.account.admin.lessons.technologies}/?sort_by=name&page_size=10`,
          icon: <Iconify icon="carbon:code" />,
          children: [],
        },
      ],
    },
    {
      title: "Użytkownicy",
      path: paths.account.admin.users.list,
      icon: <Iconify icon="carbon:user-multiple" />,
      children: [
        {
          title: "Spis użytkowników",
          path: `${paths.account.admin.users.list}/?sort_by=email&page_size=10`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Historia danych finansowych",
          path: `${paths.account.admin.users.financeHistory}/?sort_by=-created_at&page_size=10`,
          icon: <Iconify icon="carbon:finance" />,
          children: [],
        },
      ],
    },
    {
      title: "Kupony",
      path: paths.account.admin.users.list,
      icon: <Iconify icon="carbon:cut-out" />,
      children: [
        {
          title: "Spis kuponów",
          path: `${paths.account.admin.coupons.list}/?sort_by=-expiration_date&page_size=10`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Wykorzystanie kuponów",
          path: `${paths.account.admin.coupons.usage}/?sort_by=-created_at&page_size=10`,
          icon: <Iconify icon="carbon:user-activity" />,
          children: [],
        },
      ],
    },
    {
      title: "Zarobki",
      path: `${paths.account.admin.earnings.company}/?page_size=12`,
      icon: <Iconify icon="carbon:currency-dollar" />,
      children: [
        {
          title: "Zarobki firmy",
          path: `${paths.account.admin.earnings.company}/?total=True&page_size=12`,
          icon: <Iconify icon="carbon:building" />,
          children: [],
        },
        {
          title: "Zarobki instruktorów",
          path: `${paths.account.admin.earnings.teachers}/?total=False&page_size=12`,
          icon: <Iconify icon="carbon:education" />,
          children: [],
        },
      ],
    },
    {
      title: "Newsletter",
      path: `${paths.account.admin.newsletter}/?sort_by=-created_at&page_size=10`,
      icon: <Iconify icon="carbon:email-new" />,
      children: [],
    },
  ],
];
