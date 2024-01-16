import { useEffect } from "react";

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { useUnregisterNewsletter } from "src/api/newsletter/unregister";

import Image from "src/components/image";

// ----------------------------------------------------------------------

export default function NewsletterUnsubscribe({ id }: { id: string }) {
  const { mutateAsync: unregister } = useUnregisterNewsletter();

  useEffect(() => {
    unregister({ uuid: id });
  }, [id, unregister]);

  return (
    <Box
      sx={{
        py: { xs: 10, md: 15 },
        overflow: "hidden",
        bgcolor: "primary.lighter",
      }}
    >
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
