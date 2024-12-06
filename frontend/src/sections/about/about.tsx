import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { fShortenNumber } from "src/utils/format-number";

import { useStatistics } from "src/api/statistics/statistics";

import Image from "src/components/image";
import CountUp from "src/components/count-up";

// ----------------------------------------------------------------------

export default function About() {
  const { data: stats } = useStatistics();

  const statsSummary = [
    {
      number: Math.floor(stats?.students_count),
      name: "Studentów",
      description:
        "Studenci naszej szkoły to dynamiczna społeczność entuzjastów technologii, zdeterminowanych rozwijać swoje umiejętności programistyczne i tworzyć innowacyjne rozwiązania.",
    },
    {
      number: Math.floor(stats?.course_count),
      name: "Kursów",
      description:
        "Kursy oferowane przez naszą szkołę to solidna droga do zdobycia praktycznych umiejętności w dynamicznie rozwijającej się dziedzinie, prowadzone przez doświadczonych instruktorów.",
    },
    {
      number: Math.floor(stats?.lecturers_count),
      name: "Instruktorów",
      description:
        "Instruktorzy w naszej szkole to pasjonaci z obszaru technologii, oferujący wszechstronną wiedzę oraz inspirujące podejście, które umożliwiają studentom pełne zaangażowanie w proces nauki.",
    },
  ] as const;

  return (
    <Container
      sx={{
        overflow: "hidden",
        py: 10,
      }}
    >
      <Grid
        container
        spacing={{ xs: 2, md: 8 }}
        sx={{
          textAlign: { xs: "center", md: "left" },
        }}
      >
        <Grid xs={12} md={6}>
          <Typography variant="overline" sx={{ color: "primary.main" }}>
            Rozwijamy talenty, nie liczby.
          </Typography>

          <Typography variant="h3" sx={{ mb: 3 }}>
            Tworzymy przyszłość kodowania - gdzie dostępność spotyka jakość, a liczby świadczą o
            naszym sukcesie!
          </Typography>
        </Grid>

        <Grid xs={12} md={6} display="flex" alignItems="center">
          <Typography sx={{ color: "text.secondary" }}>
            Nasze statystyki to nie tylko liczby zadowolonych studentów, ale pasjonaci technologii,
            którzy odkrywają świat programowania z wsparciem doświadczonych instruktorów. Nasze
            kursy są nie tylko lekcjami, lecz też pełnym doświadczeniem, które kształtuje
            umiejętności i inspiruje do tworzenia innowacyjnych rozwiązań.
          </Typography>
        </Grid>
      </Grid>

      <Grid
        container
        spacing={8}
        direction={{ md: "row-reverse" }}
        justifyContent={{ md: "space-between" }}
      >
        <Grid xs={12} md={6} lg={6}>
          <Image
            alt="o-nas"
            src="/assets/images/general/about-summary.webp"
            ratio="3/4"
            sx={{ borderRadius: 2 }}
          />
        </Grid>

        <Grid
          xs={12}
          md={6}
          lg={5}
          sx={{
            textAlign: { xs: "center", md: "left" },
          }}
        >
          <Stack spacing={{ xs: 2, md: 2 }}>
            {statsSummary.map(
              (value) =>
                value.number > 0 && (
                  <Box key={value.name}>
                    <Typography variant="h4" sx={{ color: "text.disabled", opacity: 0.48 }}>
                      {value.name}
                    </Typography>

                    <Typography variant="h2" sx={{ mt: 1, mb: 2 }}>
                      <CountUp
                        start={value.number / 2}
                        end={value.number}
                        formattingFn={(newValue: number) => fShortenNumber(newValue)}
                      />
                      +
                    </Typography>

                    <Typography sx={{ color: "text.secondary" }}>{value.description}</Typography>
                  </Box>
                ),
            )}
          </Stack>
        </Grid>
      </Grid>
    </Container>
  );
}
