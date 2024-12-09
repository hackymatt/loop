import { useEffect } from "react";

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import { alpha, useTheme } from "@mui/material";
import Typography from "@mui/material/Typography";

import { bgGradient } from "src/theme/css";
import { useUnregisterNewsletter } from "src/api/newsletter/unregister";

import Image from "src/components/image";

// ----------------------------------------------------------------------

export default function NewsletterUnsubscribe({ id }: { id: string }) {
  const theme = useTheme();

  const { mutateAsync: unregister } = useUnregisterNewsletter();

  useEffect(() => {
    unregister({ uuid: id });
  }, [id, unregister]);

  return (
    <Box
      component="section"
      sx={{
        ...bgGradient({
          color: `to bottom, ${alpha(theme.palette.background.default, 0.9)}, ${alpha(theme.palette.background.default, 0.9)}`,
          imgUrl: "/assets/background/overlay-1.webp",
        }),
        overflow: "hidden",
        position: "relative",
        py: { xs: 10, md: 20 },
      }}
    >
      <Box
        component="img"
        alt="Texture"
        src="/assets/background/texture-1.webp"
        sx={{
          top: 0,
          right: 0,
          zIndex: 8,
          opacity: 0.24,
          position: "absolute",
          height: `calc(100% + 80px)`,
        }}
      />
      <Container>
        <Grid
          container
          spacing={{ xs: 5, md: 3 }}
          alignItems={{ md: "center" }}
          justifyContent={{ md: "space-between" }}
          direction={{ xs: "column-reverse", md: "row" }}
        >
          <Grid xs={12} md={5} sx={{ textAlign: "center", color: "grey.800" }}>
            <Typography variant="h3">Wyrejestrowano z subskrypcji newslettera</Typography>
          </Grid>

          <Grid xs={12} md={5}>
            <Image
              alt="newsletter"
              src="/assets/illustrations/illustration_newsletter.svg"
              sx={{ maxWidth: 366, mx: "auto" }}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
