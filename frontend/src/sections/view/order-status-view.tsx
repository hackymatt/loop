"use client";

import { m } from "framer-motion";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import { CircularProgress } from "@mui/material";
import Typography from "@mui/material/Typography";

import { varBounce, MotionContainer } from "src/components/animate";

// ----------------------------------------------------------------------

export default function OrderStatusView() {
  const isLoading = true;
  return (
    <Container
      component={MotionContainer}
      sx={{
        textAlign: "center",
        pt: { xs: 5, md: 10 },
        pb: { xs: 10, md: 20 },
      }}
    >
      <m.div variants={varBounce().in}>
        {isLoading && (
          <Box sx={{ fontSize: 128 }}>
            <CircularProgress size={50} />
          </Box>
        )}
      </m.div>

      <Stack spacing={1} sx={{ my: 5 }}>
        <Typography variant="h3">Oczekiwanie na płatność...</Typography>
      </Stack>
    </Container>
  );
}
