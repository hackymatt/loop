import { memo } from "react";

import Link from "@mui/material/Link";
import Box, { BoxProps } from "@mui/material/Box";

import { RouterLink } from "src/routes/components";

import Image from "src/components/image";
// ----------------------------------------------------------------------

interface LogoProps extends BoxProps {
  single?: boolean;
}

function Logo({ single = false, sx }: LogoProps) {
  const singleLogo = (
    <Image alt="logo-mark" src="/favicon/logo-mark.svg" sx={{ height: "50px", width: "auto" }} />
  );

  const fullLogo = <Image alt="logo" src="/favicon/logo.svg" />;

  return (
    <Link
      component={RouterLink}
      href="/"
      color="inherit"
      aria-label="go to homepage"
      sx={{ lineHeight: 0 }}
    >
      <Box
        sx={{
          width: single ? 64 : 75,
          lineHeight: 0,
          cursor: "pointer",
          display: "inline-flex",
          ...sx,
        }}
      >
        {single ? singleLogo : fullLogo}
      </Box>
    </Link>
  );
}

export default memo(Logo);
