import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { useBoolean } from "src/hooks/use-boolean";
import { useResponsive } from "src/hooks/use-responsive";

import Nav from "./nav";

// ----------------------------------------------------------------------

type Props = {
  children: React.ReactNode;
};

export default function AccountLayout({ children }: Props) {
  const mdUp = useResponsive("up", "md");

  const menuOpen = useBoolean();

  return (
    <>
      {mdUp ? (
        <Container sx={{ my: 5 }}>
          <Typography variant="h3">Konto</Typography>
        </Container>
      ) : (
        <Box
          sx={{
            mb: 3,
          }}
        />
      )}

      <Container>
        <Stack
          direction={{
            md: "row",
          }}
          alignItems={{
            md: "flex-start",
          }}
          sx={{
            mb: {
              xs: 8,
              md: 10,
            },
          }}
        >
          <Nav open={menuOpen.value} onClose={menuOpen.onFalse} />

          <Box
            sx={{
              flexGrow: 1,
              pl: { md: 4 },
              width: { md: `calc(100% - ${280}px)` },
            }}
          >
            {children}
          </Box>
        </Stack>
      </Container>
    </>
  );
}
