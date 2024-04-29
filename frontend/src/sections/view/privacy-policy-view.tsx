"use client";

import { Stack } from "@mui/material";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

// ----------------------------------------------------------------------

export default function PrivacyPolicyView() {
  return (
    <Container sx={{ mb: 10 }}>
      <Stack
        direction="row"
        alignItems="center"
        justifyContent="space-between"
        sx={{
          py: 5,
        }}
      >
        <Typography variant="h2">Polityka prywatności</Typography>
      </Stack>
    </Container>
  );
}
