import CountUp from "react-countup";
import Fade from "embla-carousel-fade";
import Autoplay from "embla-carousel-autoplay";

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

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import {
  Carousel,
  useCarousel,
  CarouselDotButtons,
  CarouselArrowBasicButtons,
} from "src/components/carousel";

export default function LandingHero() {
  const theme = useTheme();

  const carousel = useCarousel(
    {
      loop: true,
      duration: 100,
    },
    [Autoplay({ delay: 5000 }), Fade()],
  );

  const landingPages = [
    <LandingMain />,
    <LandingUserTest />,
    <LandingAbout />,
    <LandingSuggestions />,
    <LandingNewTeacher />,
  ];

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
          display: "flex",
          flexDirection: "column",
          minHeight: { md: "100vh" },
          pl: 2,
        }}
      >
        <Carousel carousel={carousel}>
          {landingPages.map((landingPage: JSX.Element, index: number) => (
            <Box key={index} sx={{ opacity: carousel.dots.selectedIndex === index ? 1 : 0 }}>
              {landingPage}
            </Box>
          ))}
        </Carousel>

        <Box display="flex" alignItems="center" justifyContent="space-between">
          <CarouselDotButtons
            variant="rounded"
            scrollSnaps={carousel.dots.scrollSnaps}
            selectedIndex={carousel.dots.selectedIndex}
            onClickDot={carousel.dots.onClickDot}
            sx={{ color: "primary.main", p: 0 }}
          />

          <CarouselArrowBasicButtons
            {...carousel.arrows}
            options={carousel.options}
            slotProps={{
              prevBtn: {
                svgIcon: (
                  <path
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="m15 5l-6 7l6 7"
                  />
                ),
              },
              nextBtn: {
                svgIcon: (
                  <path
                    fill="none"
                    stroke="currentColor"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="m9 5l6 7l-6 7"
                  />
                ),
              },
            }}
            sx={{ gap: 1, color: "primary.main", p: 0 }}
          />
        </Box>
      </Container>
    </Box>
  );
}

function LandingMain() {
  const mdUp = useResponsive("up", "md");

  const { data: stats } = useStatistics();

  const statsSummary = [
    {
      value: Math.floor(stats?.students_count),
      label: "Studentów",
      color: "warning",
    },
    {
      value: Math.floor(stats?.course_count),
      label: "Kursów",
      color: "error",
    },
    {
      value: Math.floor(stats?.lecturers_count),
      label: "Instruktorów",
      color: "success",
    },
  ] as const;

  const showStats = statsSummary.every((item) => item.value > 0);

  return (
    <Grid container spacing={3} display="flex" flexDirection={{ xs: "column", md: "row" }}>
      <Grid xs={12} md={6} lg={5}>
        <Stack
          sx={{
            textAlign: { xs: "center", md: "unset" },
          }}
        >
          <Typography variant="h1">
            Zostań{" "}
            <Box component="span" sx={{ color: "text.disabled" }}>
              lepszym
            </Box>{" "}
            <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
              programistą
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
              href={paths.courses}
              endIcon={<Iconify icon="carbon:chevron-right" />}
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
                  <Typography variant="h3">
                    <CountUp
                      start={item.value / 2}
                      end={item.value}
                      formattingFn={(newValue: number) => fShortenNumber(newValue)}
                    />
                    +
                  </Typography>
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
  );
}

function LandingAbout() {
  const mdUp = useResponsive("up", "md");

  return (
    <Grid container spacing={3} display="flex" flexDirection={{ xs: "column", md: "row" }}>
      <Grid xs={12} md={6} lg={5}>
        <Stack
          sx={{
            textAlign: { xs: "center", md: "unset" },
          }}
        >
          <Typography variant="h1">
            Zobacz co{" "}
            <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
              nas
            </Box>{" "}
            wyróżnia?
          </Typography>

          <Typography sx={{ color: "text.secondary", mt: 3, mb: 5 }}>
            Tworzymy przyszłość kodowania - gdzie dostępność spotyka jakość, a liczby świadczą o
            naszym sukcesie!
          </Typography>

          <Stack spacing={3} alignItems="center" direction={{ xs: "column", md: "row" }}>
            <Button
              color="inherit"
              size="large"
              variant="contained"
              href={paths.about}
              endIcon={<Iconify icon="carbon:chevron-right" />}
            >
              Sprawdź informacje
            </Button>
          </Stack>
        </Stack>
      </Grid>

      {mdUp && (
        <Grid xs={12} md={6} lg={7}>
          <Image
            alt="about"
            src="/assets/images/general/course-7.webp"
            sx={{ borderRadius: 2, height: 670 }}
          />
        </Grid>
      )}
    </Grid>
  );
}

function LandingSuggestions() {
  const mdUp = useResponsive("up", "md");

  return (
    <Grid container spacing={3} display="flex" flexDirection={{ xs: "column", md: "row" }}>
      <Grid xs={12} md={6} lg={5}>
        <Stack
          sx={{
            textAlign: { xs: "center", md: "unset" },
          }}
        >
          <Typography variant="h1">
            Nie znalazłeś kursu? Zróbmy to{" "}
            <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
              razem
            </Box>{" "}
            !
          </Typography>

          <Typography sx={{ color: "text.secondary", mt: 3, mb: 5 }}>
            Nie znalazłeś kursu, którego szukasz? Skontaktuj się z nami, a pomożemy stworzyć program
            dostosowany do Twoich potrzeb!
          </Typography>

          <Stack spacing={3} alignItems="center" direction={{ xs: "column", md: "row" }}>
            <Button
              color="inherit"
              size="large"
              variant="contained"
              href={paths.contact}
              endIcon={<Iconify icon="carbon:chevron-right" />}
            >
              Wyślij sugestię
            </Button>
          </Stack>
        </Stack>
      </Grid>

      {mdUp && (
        <Grid xs={12} md={6} lg={7}>
          <Image
            alt="about"
            src="/assets/images/general/course-7.webp"
            sx={{ borderRadius: 2, height: 670 }}
          />
        </Grid>
      )}
    </Grid>
  );
}

function LandingNewTeacher() {
  const mdUp = useResponsive("up", "md");

  return (
    <Grid container spacing={3} display="flex" flexDirection={{ xs: "column", md: "row" }}>
      <Grid xs={12} md={6} lg={5}>
        <Stack
          sx={{
            textAlign: { xs: "center", md: "unset" },
          }}
        >
          <Typography variant="h1">
            Dołącz do{" "}
            <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
              nas
            </Box>{" "}
            i inspiruj innych!
          </Typography>

          <Typography sx={{ color: "text.secondary", mt: 3, mb: 5 }}>
            Chcesz dołączyć do naszego zespołu instruktorów? Napisz do nas i podziel się swoją
            pasją!
          </Typography>

          <Stack spacing={3} alignItems="center" direction={{ xs: "column", md: "row" }}>
            <Button
              color="inherit"
              size="large"
              variant="contained"
              href={paths.contact}
              endIcon={<Iconify icon="carbon:chevron-right" />}
            >
              Wyślij zgłoszenie
            </Button>
          </Stack>
        </Stack>
      </Grid>

      {mdUp && (
        <Grid xs={12} md={6} lg={7}>
          <Image
            alt="about"
            src="/assets/images/general/course-7.webp"
            sx={{ borderRadius: 2, height: 670 }}
          />
        </Grid>
      )}
    </Grid>
  );
}

function LandingUserTest() {
  const mdUp = useResponsive("up", "md");

  return (
    <Grid container spacing={3} display="flex" flexDirection={{ xs: "column", md: "row" }}>
      <Grid xs={12} md={6} lg={5}>
        <Stack
          sx={{
            textAlign: { xs: "center", md: "unset" },
          }}
        >
          <Typography variant="h1">
            Czy{" "}
            <Box component="span" sx={{ color: "text.disabled" }}>
              programowanie
            </Box>
            {" jest dla "}
            <Box component="span" sx={{ color: "primary.main", textDecoration: "underline" }}>
              Ciebie
            </Box>
            ?
          </Typography>

          <Typography sx={{ color: "text.secondary", mt: 3, mb: 5 }}>
            Przeprowadź darmowy test predyspozycji już teraz! Odpowiedz na 20 pytań.
          </Typography>

          <Stack spacing={3} alignItems="center" direction={{ xs: "column", md: "row" }}>
            <Button
              color="inherit"
              size="large"
              variant="contained"
              href={paths.tests.predisposition}
              endIcon={<Iconify icon="carbon:chevron-right" />}
            >
              Rozpocznij test
            </Button>
          </Stack>
        </Stack>
      </Grid>

      {mdUp && (
        <Grid xs={12} md={6} lg={7}>
          <Image
            alt="test"
            src="/assets/images/general/course-11.webp"
            sx={{ borderRadius: 2, height: 670 }}
          />
        </Grid>
      )}
    </Grid>
  );
}
