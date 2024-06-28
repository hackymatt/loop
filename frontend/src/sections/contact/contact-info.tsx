import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import { IconButton } from "@mui/material";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { useResponsive } from "src/hooks/use-responsive";

import { socials } from "src/consts/socials";

import Image from "src/components/image";
import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

export default function ContactInfo() {
  const mdUp = useResponsive("up", "md");

  return (
    <Container
      sx={{
        pt: { xs: 5, md: 5 },
        pb: { xs: 10, md: 15 },
      }}
    >
      <Grid container spacing={2} justifyContent={{ md: "space-between" }}>
        <Grid xs={12} md={6} lg={4}>
          <Typography
            variant="h2"
            sx={{
              mb: 5,
              textAlign: { xs: "center", md: "left" },
            }}
          >
            Bądź w kontakcie
          </Typography>

          <Stack spacing={3} alignItems={{ xs: "center", md: "flex-start" }}>
            <Stack spacing={1}>
              <Stack direction="row" alignItems="center" sx={{ typography: "subtitle2" }}>
                <Iconify icon="carbon:email" width={24} sx={{ mr: 1 }} /> Email
              </Stack>

              <Link color="inherit" variant="body2" href="mailto:kontakt@loop.edu.pl">
                kontakt@loop.edu.pl
              </Link>
            </Stack>

            <Stack spacing={1} sx={{ mr: 2 }}>
              <Stack direction="row" alignItems="center" sx={{ typography: "subtitle2" }}>
                <Iconify icon="carbon:mobile" width={24} sx={{ mr: 1 }} /> Telefon
              </Stack>

              <Link color="inherit" variant="body2" href="tel:+48881455596">
                +48 881 455 596
              </Link>
            </Stack>

            <Divider sx={{ borderStyle: "dashed", width: 1 }} />

            <Stack spacing={1} alignItems={{ xs: "center", md: "flex-start" }}>
              <Typography variant="overline">Obserwuj nas</Typography>
              <Stack direction="row">
                {socials.map((social) => (
                  <IconButton key={social.value}>
                    <Iconify icon={social.icon} color={social.color} />
                  </IconButton>
                ))}
              </Stack>
            </Stack>
          </Stack>
        </Grid>

        {mdUp && (
          <Grid xs={12} md={6} lg={7}>
            <Image alt="contact" src="/assets/illustrations/illustration_contact.svg" />
          </Grid>
        )}
      </Grid>
    </Container>
  );
}
