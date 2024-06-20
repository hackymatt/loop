import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import { useTheme } from "@mui/material/styles";

import { useOffSetTop } from "src/hooks/use-off-set-top";

import { bgBlur } from "src/theme/css";
import { ENV } from "src/config-global";

import Logo from "src/components/logo";
import Label from "src/components/label";

import { HEADER } from "../config-layout";
import HeaderShadow from "./header-shadow";

// ----------------------------------------------------------------------

export default function HeaderSimple() {
  const theme = useTheme();

  const offset = useOffSetTop(HEADER.H_DESKTOP);

  return (
    <AppBar>
      <Toolbar
        sx={{
          height: {
            xs: HEADER.H_MOBILE,
            md: HEADER.H_DESKTOP,
          },
          transition: theme.transitions.create(["height"], {
            easing: theme.transitions.easing.easeInOut,
            duration: theme.transitions.duration.shorter,
          }),
          ...(offset && {
            ...bgBlur({
              color: theme.palette.background.default,
            }),
            height: {
              md: HEADER.H_DESKTOP_OFFSET,
            },
          }),
        }}
      >
        <Logo />
        {ENV === "PROD" ? null : (
          <Label
            color="info"
            sx={{
              ml: 0.5,
              px: 0.5,
              top: 14,
              left: 85,
              height: 20,
              fontSize: 11,
              cursor: "pointer",
              position: "absolute",
            }}
          >
            {ENV}
          </Label>
        )}
      </Toolbar>

      {offset && <HeaderShadow />}
    </AppBar>
  );
}
