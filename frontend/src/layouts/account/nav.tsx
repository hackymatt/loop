"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState, useEffect } from "react";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Drawer from "@mui/material/Drawer";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import { List, Collapse } from "@mui/material";
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
    children: [],
  },
  {
    title: "Zarządzaj hasłem",
    path: paths.account.password,
    icon: <Iconify icon="carbon:password" />,
    children: [],
  },
];

const studentNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Lekcje",
      path: paths.account.lessons,
      icon: <Iconify icon="carbon:book" />,
      children: [],
    },
    {
      title: "Recenzje",
      path: `${paths.account.reviews}?review_status_exclude=${ReviewStatus.brak}`,
      icon: <Iconify icon="carbon:review" />,
      children: [],
    },
  ],
];

const teacherNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Dane finansowe",
      path: paths.account.teacher.finance,
      icon: <Iconify icon="carbon:finance" />,
      children: [],
    },
    {
      title: "Terminarz",
      path: paths.account.teacher.calendar,
      icon: <Iconify icon="carbon:calendar" />,
      children: [],
    },
    {
      title: "Nauczanie",
      path: `${paths.account.teacher.teaching}/?sort_by=title`,
      icon: <Iconify icon="carbon:education" />,
      children: [],
    },
    {
      title: "Recenzje",
      path: paths.account.teacher.reviews,
      icon: <Iconify icon="carbon:review" />,
      children: [],
    },
    {
      title: "Zarobki",
      path: paths.account.teacher.earnings,
      icon: <Iconify icon="carbon:currency-dollar" />,
      children: [],
    },
  ],
];

const adminNavigations = [
  ...userNavigations,
  ...[
    {
      title: "Kursy",
      path: paths.account.admin.courses.list,
      icon: <Iconify icon="carbon:book" />,
      children: [
        {
          title: "Spis kursów",
          path: `${paths.account.admin.courses.list}/?sort_by=title`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Umiejętności",
          path: `${paths.account.admin.courses.skills}/?sort_by=name`,
          icon: <Iconify icon="carbon:policy" />,
          children: [],
        },
        {
          title: "Tematy",
          path: `${paths.account.admin.courses.topics}/?sort_by=name`,
          icon: <Iconify icon="carbon:query" />,
          children: [],
        },
      ],
    },
    {
      title: "Lekcje",
      path: paths.account.admin.lessons.list,
      icon: <Iconify icon="carbon:notebook" />,
      children: [
        {
          title: "Spis lekcji",
          path: `${paths.account.admin.lessons.list}/?sort_by=title`,
          icon: <Iconify icon="carbon:list" />,
          children: [],
        },
        {
          title: "Historia cen",
          path: `${paths.account.admin.lessons.priceHistory}/?sort_by=-created_at`,
          icon: <Iconify icon="carbon:chart-line" />,
          children: [],
        },
        {
          title: "Technologie",
          path: `${paths.account.admin.lessons.technologies}/?sort_by=name`,
          icon: <Iconify icon="carbon:code" />,
          children: [],
        },
      ],
    },
    {
      title: "Użytkownicy",
      path: paths.account.admin.users,
      icon: <Iconify icon="carbon:user-multiple" />,
      children: [],
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
        {navigations.map((navigation) => (
          <NavItem
            key={navigation.title}
            title={navigation.title}
            path={navigation.path}
            icon={navigation.icon}
            children={navigation.children}
          />
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
  title: string;
  path: string;
  icon?: React.ReactNode;
  children: NavItemProps[];
  isChild?: boolean;
};

function NavItem({ title, path, icon, children, isChild }: NavItemProps) {
  const active = useActiveLink(path);

  const [open, setOpen] = useState(false);

  const handleClick = () => {
    setOpen(!open);
  };

  const itemWithChildren = children.length > 0 ?? false;

  const expandIcon = open ? (
    <ListItemIcon>
      <Iconify icon="carbon:chevron-up" />
    </ListItemIcon>
  ) : (
    <ListItemIcon>
      <Iconify icon="carbon:chevron-down" />
    </ListItemIcon>
  );

  const renderContent = (
    <>
      <ListItemButton
        sx={{
          px: 1,
          height: 44,
          borderRadius: 1,
          pl: isChild ?? false ? 2 : 1,
        }}
        onClick={handleClick}
      >
        {icon && <ListItemIcon>{icon}</ListItemIcon>}
        <ListItemText
          primary={title}
          primaryTypographyProps={{
            typography: "body2",
            ...(active && {
              typography: "subtitle2",
            }),
          }}
        />
        {itemWithChildren && expandIcon}
      </ListItemButton>

      {itemWithChildren && (
        <Collapse in={open} timeout="auto" unmountOnExit>
          <List component="div" disablePadding>
            {children.map((child) => (
              <NavItem
                key={child.title}
                title={child.title}
                path={child.path}
                icon={child.icon}
                children={child.children}
                isChild
              />
            ))}
          </List>
        </Collapse>
      )}
    </>
  );

  return (
    <>
      {itemWithChildren ? (
        renderContent
      ) : (
        <Link
          component={RouterLink}
          key={title}
          href={path}
          color={active ? "primary" : "inherit"}
          underline="none"
        >
          {renderContent}
        </Link>
      )}
    </>
  );
}
