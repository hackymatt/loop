/* eslint-disable import/no-duplicates */
import { pl } from "date-fns/locale";
import { formatDistance } from "date-fns";
import { useMemo, useEffect } from "react";
import { formatInTimeZone } from "date-fns-tz";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import { useTheme } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";
import {
  List,
  Link,
  Badge,
  Avatar,
  Divider,
  Popover,
  ListItem,
  Typography,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  ListItemAvatar,
  buttonBaseClasses,
} from "@mui/material";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";
import { useRouter, usePathname } from "src/routes/hooks";

import { useOffSetTop } from "src/hooks/use-off-set-top";
import { useResponsive } from "src/hooks/use-responsive";
import { usePopover, UsePopoverReturn } from "src/hooks/use-popover";

import { getTimezone } from "src/utils/get-timezone";

import { bgBlur } from "src/theme/css";
import { useCartsRecordsCount } from "src/api/carts/carts";
import { useWishlistsRecordsCount } from "src/api/wishlists/wishlists";
import { useNotifications } from "src/api/notifications/notifications";
import { useEditNotification } from "src/api/notifications/notification";
import { adminNavigation, studentNavigation, teacherNavigation } from "src/consts/navigations";

import Logo from "src/components/logo";
import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import TextMaxLine from "src/components/text-max-line";

import { UserType } from "src/types/user";
import { INotificationProp, NotificationStatus } from "src/types/notification";

import NavMobile from "./nav/mobile";
import NavDesktop from "./nav/desktop";
import { NavItem } from "../account/nav";
import { HEADER } from "../config-layout";
import { navConfig } from "./config-navigation";
import HeaderShadow from "../common/header-shadow";

// ----------------------------------------------------------------------

type Props = {
  headerOnDark: boolean;
};

export default function Header({ headerOnDark }: Props) {
  const theme = useTheme();

  const openNotifications = usePopover();
  const openMenu = usePopover();

  const offset = useOffSetTop();

  const pathname = usePathname();

  const mdUp = useResponsive("up", "md");

  const { isLoggedIn, userType } = useUserContext();

  const { data: wishlistRecords } = useWishlistsRecordsCount(
    { page_size: -1 },
    isLoggedIn && userType === UserType.STUDENT,
  );
  const { data: cartRecords } = useCartsRecordsCount(
    { page_size: -1 },
    isLoggedIn && userType === UserType.STUDENT,
  );

  const { data: notifications, refetch: refreshNotifications } = useNotifications(
    { sort_by: "-created_at", page_size: -1 },
    isLoggedIn && userType !== UserType.ADMIN,
    60000,
  );

  const notificationItems = useMemo(
    () =>
      isLoggedIn
        ? notifications?.filter(
            (notification: INotificationProp) => notification.status === NotificationStatus.NEW,
          )?.length ?? 0
        : 0,
    [isLoggedIn, notifications],
  );
  const wishlistItems = useMemo(
    () => (isLoggedIn ? wishlistRecords : 0),
    [isLoggedIn, wishlistRecords],
  );
  const cartItems = useMemo(() => (isLoggedIn ? cartRecords : 0), [isLoggedIn, cartRecords]);

  useEffect(() => {
    if (openMenu.open) {
      openMenu.onClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  const renderContent = (
    <Stack direction="row" justifyContent="space-between" alignItems="center" width={1}>
      {mdUp && (
        <>
          <Box sx={{ lineHeight: 0, position: "relative", mt: 0.5 }}>
            <Logo />
          </Box>
          <>
            <Stack
              flexGrow={1}
              alignItems="center"
              sx={{
                height: 1,
              }}
            >
              <NavDesktop data={navConfig} />
            </Stack>

            <Box sx={{ flexGrow: { xs: 1, md: "unset" } }} />
          </>
        </>
      )}

      {!mdUp && (
        <>
          <NavMobile data={navConfig} />
          <Box sx={{ lineHeight: 0, alignContent: "center", mt: 0.5 }}>
            <Logo />
          </Box>
        </>
      )}

      <Stack spacing={3} direction="row" alignItems="center" flexGrow={1} justifyContent="flex-end">
        {isLoggedIn ? (
          <Badge
            badgeContent={userType !== UserType.ADMIN ? notificationItems : 0}
            max={99}
            color="primary"
          >
            <IconButton
              size="small"
              color="inherit"
              sx={{ p: 0 }}
              onClick={(event) => {
                refreshNotifications();
                openNotifications.onOpen(event);
              }}
              disabled={userType === UserType.ADMIN}
            >
              <Iconify icon="carbon:notification" width={24} />
            </IconButton>
          </Badge>
        ) : (
          <IconButton
            component={RouterLink}
            href={paths.login}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
          >
            <Iconify icon="carbon:notification" width={24} />
          </IconButton>
        )}

        <Badge
          badgeContent={userType === UserType.STUDENT ? wishlistItems : 0}
          max={99}
          color="primary"
        >
          <IconButton
            component={RouterLink}
            href={isLoggedIn ? paths.wishlist : `${paths.login}?redirect=${paths.wishlist}`}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
            disabled={userType !== UserType.STUDENT}
          >
            <Iconify icon="carbon:favorite" width={24} />
          </IconButton>
        </Badge>

        <Badge
          badgeContent={userType === UserType.STUDENT ? cartItems : 0}
          max={99}
          color="primary"
        >
          <IconButton
            component={RouterLink}
            href={isLoggedIn ? paths.cart : `${paths.login}?redirect=${paths.cart}`}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
            disabled={userType !== UserType.STUDENT}
          >
            <Iconify icon="carbon:shopping-cart" width={24} />
          </IconButton>
        </Badge>

        {isLoggedIn ? (
          <IconButton size="small" color="inherit" sx={{ p: 0 }} onClick={openMenu.onOpen}>
            <Iconify icon="carbon:user" width={24} />
          </IconButton>
        ) : (
          <IconButton
            component={RouterLink}
            href={paths.login}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
          >
            <Iconify icon="carbon:user" width={24} />
          </IconButton>
        )}
      </Stack>

      <NotificationsPopover
        openNotifications={openNotifications}
        notifications={notifications ?? []}
      />

      <AccountPopover openMenu={openMenu} />
    </Stack>
  );

  return (
    <AppBar>
      <Toolbar
        disableGutters
        sx={{
          height: {
            xs: HEADER.H_MOBILE,
            md: HEADER.H_DESKTOP,
          },
          transition: theme.transitions.create(["height", "background-color"], {
            easing: theme.transitions.easing.easeInOut,
            duration: theme.transitions.duration.shorter,
          }),
          ...(headerOnDark && {
            color: "common.white",
          }),
          ...(offset && {
            ...bgBlur({ color: theme.palette.background.default }),
            color: "text.primary",
            height: {
              md: HEADER.H_DESKTOP - 16,
            },
          }),
        }}
      >
        <Container
          sx={{
            height: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          {renderContent}
        </Container>
      </Toolbar>

      {offset && <HeaderShadow />}
    </AppBar>
  );
}

function NotificationItem({
  notification,
  onClick,
}: {
  notification: INotificationProp;
  onClick?: (notification: INotificationProp) => void;
}) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: editNotification } = useEditNotification(notification.id);

  const handleEditNotification = async () => {
    try {
      await editNotification({ ...notification, status: NotificationStatus.READ });
    } catch {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  };

  return (
    <ListItem disablePadding>
      <ListItemButton
        sx={{
          px: 1,
          height: 44,
          borderRadius: 1,
          pl: 2,
        }}
        onClick={async () => {
          if (notification.status === NotificationStatus.NEW) {
            await handleEditNotification();
          }
          if (onClick) {
            onClick(notification);
          }
        }}
      >
        <ListItemAvatar>
          <Avatar
            color={notification.status === "NEW" ? "primary" : "inherit"}
            sx={{ width: 28, height: 28 }}
          >
            <Iconify icon={notification.icon} />
          </Avatar>
        </ListItemAvatar>
        <ListItemText
          primary={notification.title}
          secondary={
            <>
              <Typography
                component="span"
                variant="body2"
                sx={{ color: "text.primary", display: "inline" }}
              >
                {notification.subtitle}
              </Typography>
              <TextMaxLine variant="body2" line={3}>
                {notification.description}
              </TextMaxLine>
              <Typography component="span" variant="caption" sx={{ display: "inline" }}>
                {formatDistance(
                  new Date(
                    formatInTimeZone(notification.createdAt, getTimezone(), "yyyy-MM-dd HH:mm:ss"),
                  ),
                  new Date(),
                  {
                    addSuffix: true,
                    locale: pl,
                  },
                )}
              </Typography>
            </>
          }
        />
      </ListItemButton>
    </ListItem>
  );
}

function NotificationsPopover({
  openNotifications,
  notifications,
}: {
  openNotifications: UsePopoverReturn;
  notifications: INotificationProp[];
}) {
  const { enqueueSnackbar } = useToastContext();

  function handleCopy(text: string) {
    navigator.clipboard.writeText(text);
    enqueueSnackbar("Skopiowano do schowka", { variant: "success" });
  }

  return (
    <Popover
      open={openNotifications.open}
      anchorEl={openNotifications.anchorEl}
      onClose={openNotifications.onClose}
      anchorOrigin={{ vertical: "bottom", horizontal: "left" }}
      transformOrigin={{ vertical: "top", horizontal: "left" }}
      slotProps={{
        paper: {
          sx: {
            width: 360,
            mt: 1,
            maxHeight: "calc(100% / 4 * 3)",
            [`& .${buttonBaseClasses.root}`]: {
              px: 1.5,
              py: 0.75,
              height: "auto",
            },
          },
        },
      }}
    >
      <Box component="nav">
        <List sx={{ width: "100%", maxWidth: 360 }}>
          {notifications.length > 0 ? (
            notifications.map((notification: INotificationProp) =>
              notification.path ? (
                <Link
                  key={notification.id}
                  component={RouterLink}
                  href={notification.path}
                  underline="none"
                  color={notification.status === NotificationStatus.NEW ? "primary" : "inherit"}
                >
                  <NotificationItem notification={notification} />
                </Link>
              ) : (
                <Link
                  key={notification.id}
                  underline="none"
                  color={notification.status === NotificationStatus.NEW ? "primary" : "inherit"}
                >
                  <NotificationItem
                    notification={notification}
                    onClick={(n: INotificationProp) => handleCopy(n.subtitle ?? "")}
                  />
                </Link>
              ),
            )
          ) : (
            <ListItem>
              <ListItemText primary="Brak powiadomień" />
            </ListItem>
          )}
        </List>
      </Box>
    </Popover>
  );
}

function AccountPopover({ openMenu }: { openMenu: UsePopoverReturn }) {
  const { enqueueSnackbar } = useToastContext();
  const pathname = usePathname();
  const { push } = useRouter();

  const { logoutUser, userType } = useUserContext();

  const navigations = useMemo(
    () =>
      ({
        [UserType.ADMIN]: adminNavigation,
        [UserType.TEACHER]: teacherNavigation,
        [UserType.STUDENT]: studentNavigation,
      })[userType],
    [userType],
  );

  const handleLogout = async () => {
    try {
      await logoutUser({});
      if (pathname.includes(paths.account.root)) {
        push(paths.login);
      }
      enqueueSnackbar("Wylogowano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
    openMenu.onClose();
  };

  return (
    <Popover
      open={openMenu.open}
      anchorEl={openMenu.anchorEl}
      onClose={openMenu.onClose}
      anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
      transformOrigin={{ vertical: "top", horizontal: "right" }}
      slotProps={{
        paper: {
          sx: {
            width: 220,
            mt: 1,
            [`& .${buttonBaseClasses.root}`]: {
              px: 1.5,
              py: 0.75,
              height: "auto",
            },
          },
        },
      }}
    >
      <Box component="nav">
        <List sx={{ width: "100%", maxWidth: 360 }}>
          {navigations?.map((navigation) => (
            <NavItem
              key={navigation.title}
              title={navigation.title}
              path={navigation.path}
              icon={navigation.icon}
              children={navigation.children}
            />
          ))}
        </List>
      </Box>

      <Divider sx={{ my: 0.5, borderStyle: "dashed" }} />

      <List sx={{ width: "100%", maxWidth: 360 }}>
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
      </List>
    </Popover>
  );
}
