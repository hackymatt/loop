import { Masonry } from "@mui/lab";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import { IconButton } from "@mui/material";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { socials } from "src/consts/socials";
import { useTechnologies } from "src/api/technologies/technologies";

import Logo from "src/components/logo";
import Iconify from "src/components/iconify";

import { NewsletterEmail } from "src/sections/newsletter/newsletter";

// ----------------------------------------------------------------------

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const { data: technologies } = useTechnologies({
    courses_count_from: 1,
    sort_by: "name",
    page_size: -1,
  });

  const mainFooter = (
    <>
      <Divider />

      <Container
        sx={{
          overflow: "hidden",
          py: { xs: 8, md: 10 },
        }}
      >
        <Grid container spacing={3} justifyContent={{ md: "space-between" }}>
          <Grid xs={12} md={4}>
            <Stack spacing={{ xs: 3, md: 5 }}>
              <Stack alignItems="flex-start" spacing={3}>
                <Logo />
              </Stack>

              <Stack spacing={1} alignItems="flex-start">
                <Link
                  component={RouterLink}
                  href={paths.courses}
                  variant="body2"
                  sx={{ color: "text.primary" }}
                >
                  Kursy
                </Link>

                <Link
                  component={RouterLink}
                  href={paths.about}
                  variant="body2"
                  sx={{ color: "text.primary" }}
                >
                  O nas
                </Link>

                <Link
                  component={RouterLink}
                  href={paths.contact}
                  variant="body2"
                  sx={{ color: "text.primary" }}
                >
                  Kontakt
                </Link>

                <Link
                  component={RouterLink}
                  href={paths.support}
                  variant="body2"
                  sx={{ color: "text.primary" }}
                >
                  FAQ
                </Link>
              </Stack>

              <Stack spacing={2}>
                <Stack spacing={1}>
                  <Typography variant="h6">Bądź na bieżąco</Typography>
                  <Typography variant="caption" sx={{ color: "text.secondary" }}>
                    Zapisz się do naszego newslettera.
                  </Typography>
                </Stack>

                <NewsletterEmail buttonLabel="Zapisz" />
              </Stack>

              <Stack spacing={2}>
                <Typography variant="h6">Media społecznościowe</Typography>
                <Stack direction="row">
                  {socials.map((social) => (
                    <IconButton key={social.value} href={social.url} target="_blank">
                      <Iconify icon={social.icon} color={social.color} />
                    </IconButton>
                  ))}
                </Stack>
              </Stack>
            </Stack>
          </Grid>

          {technologies && technologies.length > 0 && (
            <Grid xs={12} md={6}>
              <Masonry columns={3} spacing={2} defaultColumns={3} defaultSpacing={2}>
                {technologies?.map((technology) => (
                  <Link
                    component={RouterLink}
                    key={technology.id}
                    href={`${paths.courses}?technology_in=${technology.name}`}
                    variant="caption"
                    sx={{
                      color: "text.secondary",
                      "&:hover": {
                        color: "text.primary",
                      },
                    }}
                  >
                    <Typography
                      variant="subtitle2"
                      sx={{
                        cursor: "pointer",
                        display: "inline-flex",
                        alignItems: "center",
                      }}
                    >
                      {`Kursy ${technology.name}`}
                      <Iconify width={16} icon="carbon:chevron-right" sx={{ ml: 0.5 }} />
                    </Typography>
                  </Link>
                ))}
              </Masonry>
            </Grid>
          )}
        </Grid>
      </Container>

      <Divider />

      <Container>
        <Stack
          spacing={2.5}
          direction={{ xs: "column", md: "row" }}
          justifyContent="space-between"
          sx={{ py: 3, textAlign: "center" }}
        >
          <Typography variant="caption" sx={{ color: "text.secondary" }}>
            {`© ${currentYear}. Wszelkie prawa zastrzeżone`}
          </Typography>

          <Stack direction="row" spacing={3} justifyContent="center">
            <Link
              component={RouterLink}
              href={paths.privacyPolicy}
              variant="caption"
              sx={{ color: "text.secondary" }}
            >
              Polityka prywatności
            </Link>

            <Link
              component={RouterLink}
              href={paths.termsAndConditions}
              variant="caption"
              sx={{ color: "text.secondary" }}
            >
              Regulamin
            </Link>
          </Stack>
        </Stack>
      </Container>
    </>
  );

  return <footer>{mainFooter}</footer>;
}
