"use client";

import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

// ----------------------------------------------------------------------

export default function PrivacyPolicyView() {
  return (
    <Container sx={{ mb: 10 }}>
      <Typography variant="h3" sx={{ py: { xs: 3, md: 10 } }}>
        Polityka prywatności
      </Typography>
    </Container>
  );
}
