import { useEffect } from "react";

import { Box } from "@mui/material";
import List from "@mui/material/List";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";

import { usePathname } from "src/routes/hooks";

import { useBoolean } from "src/hooks/use-boolean";

import Logo from "src/components/logo";
import Iconify from "src/components/iconify";
import { Scrollbar } from "src/components/scrollbar";

import NavList from "./nav-list";
import { NavProps } from "../types";
import { NAV } from "../../../config-layout";

// ----------------------------------------------------------------------

export default function NavMobile({ data }: NavProps) {
  const pathname = usePathname();

  const mobileOpen = useBoolean();

  useEffect(() => {
    if (mobileOpen.value) {
      mobileOpen.onFalse();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  return (
    <>
      <IconButton onClick={mobileOpen.onTrue} sx={{ color: "inherit" }}>
        <Iconify icon="carbon:menu" />
      </IconButton>

      <Drawer
        open={mobileOpen.value}
        onClose={mobileOpen.onFalse}
        PaperProps={{
          sx: {
            pb: 5,
            width: NAV.W_VERTICAL,
          },
        }}
      >
        <Scrollbar fillContent>
          <Box sx={{ lineHeight: 0, position: "relative", mx: 2.5, my: 3 }}>
            <Logo />
          </Box>

          <List component="nav" disablePadding>
            {data.map((list) => (
              <NavList key={list.title} data={list} />
            ))}
          </List>
        </Scrollbar>

        <Box gap={1.5} display="flex" sx={{ px: 2.5, py: 3 }}>
          <IconButton size="small" color="inherit" sx={{ p: 0 }}>
            <Iconify icon="circle-flags:pl" width={24} />
          </IconButton>
        </Box>
      </Drawer>
    </>
  );
}
