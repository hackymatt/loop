"use client";

import { m } from "framer-motion";

import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { RouterLink } from "src/routes/components";

import MainLayout from "src/layouts/main";
import CompactLayout from "src/layouts/compact";

import Image from "src/components/image";
import { varBounce, MotionContainer } from "src/components/animate";

// ----------------------------------------------------------------------

export default function NotFoundView() {
  return (
    <MainLayout disabledHeader disabledFooter>
      <CompactLayout>
        <MotionContainer>
          <m.div variants={varBounce().in}>
            <Typography variant="h3" paragraph>
              Strona nie istnieje!
            </Typography>
          </m.div>

          <m.div variants={varBounce().in}>
            <Typography sx={{ color: "text.secondary" }}>
              Przepraszamy, nie znaleźliśmy strony, której szukasz. Być może błędnie wpisałeś adres
              URL? Pamiętaj, aby sprawdzić pisownię.
            </Typography>
          </m.div>

          <m.div variants={varBounce().in}>
            <Image
              alt="404"
              src="/assets/illustrations/illustration_404.svg"
              sx={{
                mx: "auto",
                maxWidth: 320,
                my: { xs: 5, sm: 8 },
              }}
            />
          </m.div>

          <Button component={RouterLink} href="/" size="large" color="inherit" variant="contained">
            Wróć do strony głownej
          </Button>
        </MotionContainer>
      </CompactLayout>
    </MainLayout>
  );
}
