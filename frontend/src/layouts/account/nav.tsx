"use client";

import { useMemo, useEffect } from "react";
import { useRouter } from "next/navigation";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Drawer from "@mui/material/Drawer";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemButton from "@mui/material/ListItemButton";

import { paths } from "src/routes/paths";
import { useActiveLink } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { useResponsive } from "src/hooks/use-responsive";

import { useUserDetails } from "src/api/auth/details";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import TextMaxLine from "src/components/text-max-line";
import { useToastContext } from "src/components/toast";

import AccountImage from "src/sections/_elearning/account/account-image";

import { UserType } from "src/types/user";
import { ReviewStatus } from "src/types/purchase";

// ----------------------------------------------------------------------

const userNavigations = [
  {
    title: "Dane osobowe",
    path: paths.account.personal,
    icon: <Iconify icon="carbon:user" />,
  },
  {
    title: "Zarządzaj hasłem",
    path: paths.account.password,
    icon: <Iconify icon="carbon:user" />,
  },
];

const studentNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Lekcje",
      path: paths.account.lessons,
      icon: <Iconify icon="carbon:book" />,
    },
    {
      title: "Recenzje",
      path: `${paths.account.reviews}?review_status_exclude=${ReviewStatus.brak}`,
      icon: <Iconify icon="carbon:review" />,
    },
  ],
];

const teacherNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Lekcje",
      path: `${paths.account.teacher.lessons}?sort_by=title`,
      icon: <Iconify icon="carbon:notebook" />,
    },
    {
      title: "Terminarz",
      path: paths.account.teacher.calendar,
      icon: <Iconify icon="carbon:calendar" />,
    },
    {
      title: "Recenzje",
      path: paths.account.teacher.reviews,
      icon: <Iconify icon="carbon:review" />,
    },
    {
      title: "Zarobki",
      path: paths.account.teacher.earnings,
      icon: <Iconify icon="carbon:currency-dollar" />,
    },
  ],
];

const adminNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Lekcje",
      path: `${paths.account.admin.lessons}?sort_by=title`,
      icon: <Iconify icon="carbon:notebook" />,
    },
    {
      title: "Kursy",
      path: paths.account.admin.courses,
      icon: <Iconify icon="carbon:book" />,
    },
    {
      title: "Użytkownicy",
      path: paths.account.admin.users,
      icon: <Iconify icon="carbon:user-multiple" />,
    },
    {
      title: "Zakupy",
      path: paths.account.admin.purchases,
      icon: <Iconify icon="carbon:purchase" />,
    },
    {
      title: "Recenzje",
      path: paths.account.admin.reviews,
      icon: <Iconify icon="carbon:review" />,
    },
    {
      title: "Zarobki",
      path: paths.account.admin.earnings,
      icon: <Iconify icon="carbon:currency-dollar" />,
    },
  ],
];

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
};

export default function Nav({ open, onClose }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const mdUp = useResponsive("up", "md");

  const { logoutUser, isLoggedIn } = useUserContext();

  const { data: userDetails } = useUserDetails();

  const userType = useMemo(
    () => (userDetails?.user_type ? userDetails.user_type : UserType.Student),
    [userDetails],
  );

  const navigations = useMemo(
    () =>
      ({
        [UserType.Admin]: adminNavigations,
        [UserType.Wykładowca]: teacherNavigations,
        [UserType.Student]: studentNavigations,
      })[userType],
    [userType],
  );

  const handleLogout = async () => {
    try {
      await logoutUser({});
      enqueueSnackbar("Wylogowano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

  useEffect(() => {
    if (!isLoggedIn) {
      push(paths.login);
    }
  }, [isLoggedIn, push]);

  const renderContent = (
    <Stack
      sx={{
        flexShrink: 0,
        borderRadius: 2,
        width: 1,
        ...(mdUp && {
          width: 280,
          border: (theme) => `solid 1px ${alpha(theme.palette.grey[500], 0.24)}`,
        }),
      }}
    >
      <Stack spacing={2} sx={{ p: 3, pb: 2 }}>
        <AccountImage />

        {userDetails && (
          <Stack spacing={0.5}>
            <TextMaxLine variant="subtitle1" line={1}>
              {`${userDetails.first_name} ${userDetails.last_name}`}
            </TextMaxLine>
            <TextMaxLine variant="body2" line={1} sx={{ color: "text.secondary" }}>
              {userDetails.email}
            </TextMaxLine>
          </Stack>
        )}
      </Stack>

      <Divider sx={{ borderStyle: "dashed" }} />

      <Stack sx={{ my: 1, px: 2 }}>
        {navigations.map((item) => (
          <NavItem key={item.title} item={item} />
        ))}
      </Stack>

      <Divider sx={{ borderStyle: "dashed" }} />

      <Stack sx={{ my: 1, px: 2 }}>
        <ListItemButton
          sx={{
            px: 1,
            height: 44,
            borderRadius: 1,
          }}
          onClick={handleLogout}
        >
          <ListItemIcon>
            <Iconify icon="carbon:logout" />
          </ListItemIcon>
          <ListItemText
            primary="Wyloguj"
            primaryTypographyProps={{
              typography: "body2",
            }}
          />
        </ListItemButton>
      </Stack>
    </Stack>
  );

  return (
    <>
      {mdUp ? (
        renderContent
      ) : (
        <Drawer
          open={open}
          onClose={onClose}
          PaperProps={{
            sx: {
              width: 280,
            },
          }}
        >
          {renderContent}
        </Drawer>
      )}
    </>
  );
}

// ----------------------------------------------------------------------

type NavItemProps = {
  item: {
    title: string;
    path: string;
    icon: React.ReactNode;
  };
};

function NavItem({ item }: NavItemProps) {
  const active = useActiveLink(item.path);

  return (
    <Link
      component={RouterLink}
      key={item.title}
      href={item.path}
      color={active ? "primary" : "inherit"}
      underline="none"
    >
      <ListItemButton
        sx={{
          px: 1,
          height: 44,
          borderRadius: 1,
        }}
      >
        <ListItemIcon>{item.icon}</ListItemIcon>
        <ListItemText
          primary={item.title}
          primaryTypographyProps={{
            typography: "body2",
            ...(active && {
              typography: "subtitle2",
            }),
          }}
        />
      </ListItemButton>
    </Link>
  );
}
