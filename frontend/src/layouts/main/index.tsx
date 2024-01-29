import Box, { BoxProps } from "@mui/material/Box";

import Footer from "./footer";
import Header from "./header";
import { HEADER } from "../config-layout";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  children: React.ReactNode;
  headerOnDark?: boolean;
  disabledSpacing?: boolean;
  disabledHeader?: boolean;
  disabledFooter?: boolean;
};

export default function MainLayout({
  children,
  headerOnDark = false,
  disabledSpacing = false,
  disabledHeader = false,
  disabledFooter = false,
  sx,
  ...other
}: Props) {
  return (
    <Box
      sx={{
        height: 1,
        display: "flex",
        flexDirection: "column",
        ...sx,
      }}
      {...other}
    >
      {!disabledHeader && <Header headerOnDark={headerOnDark} />}

      <Box component="main" sx={{ flexGrow: 1 }}>
        {!(disabledSpacing || headerOnDark) && (
          <Box
            sx={{
              height: { xs: HEADER.H_MOBILE, md: HEADER.H_DESKTOP },
            }}
          />
        )}

        {children}
      </Box>

      {!disabledFooter && <Footer />}
    </Box>
  );
}
