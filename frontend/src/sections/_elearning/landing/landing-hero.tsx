import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import { alpha, useTheme } from "@mui/material/styles";

import { paths } from "src/routes/paths";

import { useResponsive } from "src/hooks/use-responsive";

import { fShortenNumber } from "src/utils/format-number";

import { bgGradient } from "src/theme/css";
import { useStatistics } from "src/api/statistics/statistics";
import HeroIllustration from "src/assets/illustrations/hero-illustration";

import Iconify from "src/components/iconify";

export default function LandingHero() {
  const theme = useTheme();

  const mdUp = useResponsive("up", "md");

  const { data: stats } = useStatistics();

  const statsSummary = [
    { value: stats?.students_count, label: "Studentów", color: "warning" },
    { value: stats?.course_count, label: "Kursów", color: "error" },
    { value: stats?.lecturers_count, label: "Wykładowców", color: "success" },
  ] as const;

  const showStats = statsSummary.every((item) => item.value > 0);

  return (
    <Box
      sx={{
        ...bgGradient({
          color: alpha(theme.palette.background.default, 0.9),
          imgUrl: "/assets/background/overlay_1.jpg",
        }),
        overflow: "hidden",
      }}
    >
      <Container
        sx={{
          py: 15,
          display: { md: "flex" },
          alignItems: { md: "center" },
          height: { md: `100vh` },
        }}
      >
        <Grid container spacing={3}>
          <Grid xs={12} md={6} lg={5}>
            <Stack
              sx={{
                textAlign: { xs: "center", md: "unset" },
              }}
            >
              <Typography variant="h1">
                Zostań
                <Box component="span" sx={{ color: "text.disabled" }}>
                  {` lepszym`}
                </Box>{" "}
                <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
                  {` programistą`}
                </Box>{" "}
                już dziś!
              </Typography>

              <Typography sx={{ color: "text.secondary", mt: 3, mb: 5 }}>
                Zdalne zajęcia programowania prowadzone przez praktyków.
              </Typography>

              <Stack spacing={3} alignItems="center" direction={{ xs: "column", md: "row" }}>
                <Button
                  color="inherit"
                  size="large"
                  variant="contained"
                  href={paths.eLearning.courses}
                  endIcon={<Iconify icon="carbon:chevron-right" />}
                  sx={{ textTransform: "none" }}
                >
                  Rozpocznij naukę
                </Button>
              </Stack>

              <Divider sx={{ borderStyle: "dashed", mt: 2, mb: 6 }} />

              <Stack
                direction="row"
                spacing={{ xs: 3, sm: 10 }}
                justifyContent={{ xs: "center", md: "unset" }}
              >
                {showStats &&
                  statsSummary.map((item) => (
                    <Stack key={item.label} spacing={0.5} sx={{ position: "relative" }}>
                      <Box
                        sx={{
                          top: 8,
                          left: -4,
                          width: 24,
                          height: 24,
                          opacity: 0.24,
                          borderRadius: "50%",
                          position: "absolute",
                          bgcolor: `${item.color}.main`,
                        }}
                      />
                      <Typography variant="h3">{fShortenNumber(item.value)}+</Typography>
                      <Typography variant="body2" sx={{ color: "text.secondary" }}>
                        {item.label}
                      </Typography>
                    </Stack>
                  ))}
              </Stack>
            </Stack>
          </Grid>

          {mdUp && (
            <Grid xs={12} md={6} lg={7}>
              <HeroIllustration />
            </Grid>
          )}
        </Grid>
      </Container>
    </Box>
  );
}
