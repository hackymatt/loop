"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

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

import { UserType } from "src/consts/user-type";
import { useUserDetails } from "src/api/auth/details";
import { adminNavigation, studentNavigation, teacherNavigation } from "src/consts/navigations";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import TextMaxLine from "src/components/text-max-line";
import { useToastContext } from "src/components/toast";

import AccountImage from "src/sections/account/account-image";

// ----------------------------------------------------------------------

type Props = {
  open: boolean;
  onClose: VoidFunction;
};

export default function Nav({ open, onClose }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const mdUp = useResponsive("up", "md");

  const { logoutUser, userType, isLoggedIn } = useUserContext();

  const { data: userDetails } = useUserDetails(isLoggedIn);

  const navigations = useMemo(
    () =>
      ({
        [UserType.Admin]: adminNavigation,
        [UserType.Teacher]: teacherNavigation,
        [UserType.Student]: studentNavigation,
      })[userType],
    [userType],
  );

  const handleLogout = async () => {
    try {
      await logoutUser({});
      push(paths.login);
      enqueueSnackbar("Wylogowano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

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
              {`${userDetails.firstName} ${userDetails.lastName}`}
            </TextMaxLine>
            <TextMaxLine variant="body2" line={1} sx={{ color: "text.secondary" }}>
              {userDetails.email}
            </TextMaxLine>
          </Stack>
        )}
      </Stack>

      <Divider sx={{ borderStyle: "dashed" }} />

      <Stack sx={{ my: 1, px: 2 }}>
        {navigations?.map((navigation) => (
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

export function NavItem({ title, path, icon, children, isChild }: NavItemProps) {
  const active = useActiveLink(path);

  const [open, setOpen] = useState(active);

  const handleClick = () => {
    setOpen(!open);
  };

  const itemWithChildren = children.length > 0;

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
        {icon && (
          <ListItemIcon
            sx={{
              ...(active && {
                color: (theme) => theme.palette.primary.main,
              }),
            }}
          >
            {icon}
          </ListItemIcon>
        )}
        <ListItemText
          primary={title}
          primaryTypographyProps={{
            typography: "body2",
            ...(active && {
              color: (theme) => theme.palette.primary.main,
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
