import { memo } from "react";

import Link from "@mui/material/Link";
import { Stack } from "@mui/material";
import Box, { BoxProps } from "@mui/material/Box";

import { RouterLink } from "src/routes/components";

import { ENV } from "src/config-global";

import Image from "src/components/image";

import Label from "../label";
// ----------------------------------------------------------------------

interface LogoProps extends BoxProps {
  single?: boolean;
}

function Logo({ single = false, sx }: LogoProps) {
  const singleLogo = <Image alt="logo-mark" src="/logo/logo-mark.svg" />;

  const fullLogo = <Image alt="logo" src="/logo/logo.svg" />;

  return (
    <Link
      component={RouterLink}
      href="/"
      color="inherit"
      aria-label="go to homepage"
      sx={{ lineHeight: 0 }}
    >
      <Stack
        alignItems="center"
        justifyContent="center"
        sx={{
          width: single ? 64 : 80,
          lineHeight: 0,
          cursor: "pointer",
          display: "inline-flex",
        }}
      >
        <Box
          sx={{
            width: single ? 64 : 80,
            lineHeight: 0,
            cursor: "pointer",
            display: "inline-flex",
            ...sx,
          }}
        >
          {single ? singleLogo : fullLogo}
        </Box>
        {ENV === "PROD" ? null : <Label color="info">{ENV}</Label>}
      </Stack>
    </Link>
  );
}

export default memo(Logo);
