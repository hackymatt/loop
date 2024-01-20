"use client";

import { m } from "framer-motion";

import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { RouterLink } from "src/routes/components";

import CompactLayout from "src/layouts/compact";

import Image from "src/components/image";
import { varBounce, MotionContainer } from "src/components/animate";

// ----------------------------------------------------------------------

export default function Error500View() {
  return (
    <CompactLayout>
      <MotionContainer>
        <m.div variants={varBounce().in}>
          <Typography variant="h3" paragraph>
            500 Błąd serwera
          </Typography>
        </m.div>

        <m.div variants={varBounce().in}>
          <Typography sx={{ color: "text.secondary" }}>
            Wystąpił błąd. Spróbuj ponownie później.
          </Typography>
        </m.div>

        <m.div variants={varBounce().in}>
          <Image
            alt="500"
            src="/assets/illustrations/illustration_500.svg"
            sx={{
              mx: "auto",
              maxWidth: 320,
              my: { xs: 5, sm: 8 },
            }}
          />
        </m.div>

        <Button
          component={RouterLink}
          href="/"
          size="large"
          color="inherit"
          variant="contained"
          sx={{ textTransform: "none" }}
        >
          Wróć do strony głownej
        </Button>
      </MotionContainer>
    </CompactLayout>
  );
}
