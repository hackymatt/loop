import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import { Badge } from "@mui/material";
import Stack from "@mui/material/Stack";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Container from "@mui/material/Container";
import { useTheme } from "@mui/material/styles";
import IconButton from "@mui/material/IconButton";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useUser } from "src/hooks/use-user";
import { useOffSetTop } from "src/hooks/use-off-set-top";
import { useResponsive } from "src/hooks/use-responsive";

import { bgBlur } from "src/theme/css";

import Logo from "src/components/logo";
import Label from "src/components/label";
import Iconify from "src/components/iconify";

import NavMobile from "./nav/mobile";
import NavDesktop from "./nav/desktop";
import { HEADER } from "../config-layout";
import { navConfig } from "./config-navigation";
import HeaderShadow from "../common/header-shadow";

// ----------------------------------------------------------------------

type Props = {
  headerOnDark: boolean;
};

export default function Header({ headerOnDark }: Props) {
  const theme = useTheme();

  const offset = useOffSetTop();

  const mdUp = useResponsive("up", "md");

  const { isLoggedIn } = useUser();

  const renderContent = (
    <>
      <Box sx={{ lineHeight: 0, position: "relative" }}>
        <Logo />

        <Link href="https://zone-docs.vercel.app/changelog" target="_blank" rel="noopener">
          <Label
            color="info"
            sx={{
              ml: 0.5,
              px: 0.5,
              top: -14,
              left: 60,
              height: 20,
              fontSize: 11,
              cursor: "pointer",
              position: "absolute",
            }}
          >
            v2.4.0
          </Label>
        </Link>
      </Box>

      <>
        <Stack
          flexGrow={1}
          alignItems="center"
          sx={{
            height: 1,
            display: { xs: "none", md: "flex" },
          }}
        >
          <NavDesktop data={navConfig} />
        </Stack>

        <Box sx={{ flexGrow: { xs: 1, md: "unset" } }} />
      </>

      {!mdUp && <NavMobile data={navConfig} />}

      <Stack spacing={3} direction="row" alignItems="center" flexGrow={1} justifyContent="flex-end">
        <Badge badgeContent={2} color="primary">
          <IconButton
            component={RouterLink}
            href={paths.wishlist}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
          >
            <Iconify icon="carbon:favorite" width={24} />
          </IconButton>
        </Badge>

        <Badge badgeContent={4} color="primary">
          <IconButton
            component={RouterLink}
            href={paths.cart}
            size="small"
            color="inherit"
            sx={{ p: 0 }}
          >
            <Iconify icon="carbon:shopping-cart" width={24} />
          </IconButton>
        </Badge>

        <IconButton
          component={RouterLink}
          href={isLoggedIn ? paths.account.personal : paths.login}
          size="small"
          color="inherit"
          sx={{ p: 0 }}
        >
          <Iconify icon="carbon:user" width={24} />
        </IconButton>
      </Stack>
    </>
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
