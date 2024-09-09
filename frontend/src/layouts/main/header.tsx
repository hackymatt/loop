import { useMemo, useEffect } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import { useTheme } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";
import {
  Badge,
  Divider,
  Popover,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  buttonBaseClasses,
} from "@mui/material";

import { paths } from "src/routes/paths";
import { usePathname } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { usePopover } from "src/hooks/use-popover";
import { useOffSetTop } from "src/hooks/use-off-set-top";
import { useResponsive } from "src/hooks/use-responsive";

import { bgBlur } from "src/theme/css";
import { useCartsRecordsCount } from "src/api/carts/carts";
import { useWishlistsRecordsCount } from "src/api/wishlists/wishlists";
import { adminNavigations, studentNavigations, teacherNavigations } from "src/consts/navigations";

import Logo from "src/components/logo";
import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

import { UserType } from "src/types/user";

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

  const { enqueueSnackbar } = useToastContext();

  const openMenu = usePopover();

  const offset = useOffSetTop();

  const pathname = usePathname();

  const mdUp = useResponsive("up", "md");

  const { logoutUser, isLoggedIn, userType } = useUserContext();

  const navigations = useMemo(
    () =>
      ({
        [UserType.Admin]: adminNavigations,
        [UserType.Wykładowca]: teacherNavigations,
        [UserType.Student]: studentNavigations,
      })[userType],
    [userType],
  );

  const { data: wishlistRecords } = useWishlistsRecordsCount({ page_size: -1 }, isLoggedIn);
  const { data: cartRecords } = useCartsRecordsCount({ page_size: -1 }, isLoggedIn);

  const wishlistItems = useMemo(
    () => (isLoggedIn ? wishlistRecords : 0),
    [isLoggedIn, wishlistRecords],
  );
  const cartItems = useMemo(() => (isLoggedIn ? cartRecords : 0), [isLoggedIn, cartRecords]);

  const handleLogout = async () => {
    try {
      await logoutUser({});
      enqueueSnackbar("Wylogowano pomyślnie", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
    openMenu.onClose();
  };

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
          <Box sx={{ lineHeight: 0, position: "relative" }}>
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
          <Box sx={{ lineHeight: 0, alignContent: "center" }}>
            <Logo />
          </Box>
        </>
      )}

      <Stack spacing={3} direction="row" alignItems="center" justifyContent="flex-end">
        <Badge badgeContent={wishlistItems} color="primary">
          <IconButton
            component={RouterLink}
            href={isLoggedIn ? paths.wishlist : paths.login}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
            disabled={userType !== UserType.Student}
          >
            <Iconify icon="carbon:favorite" width={24} />
          </IconButton>
        </Badge>

        <Badge badgeContent={cartItems} color="primary">
          <IconButton
            component={RouterLink}
            href={isLoggedIn ? paths.cart : paths.login}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
            disabled={userType !== UserType.Student}
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
        </Box>

        <Divider sx={{ my: 0.5, borderStyle: "dashed" }} />

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
      </Popover>
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
