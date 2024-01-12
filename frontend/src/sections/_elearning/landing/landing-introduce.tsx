import packageInfo from "package.json";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { useResponsive } from "src/hooks/use-responsive";

import Image from "src/components/image";

// ----------------------------------------------------------------------

export default function LandingIntroduce() {
  const mdUp = useResponsive("up", "md");

  return (
    <Container
      sx={{
        py: { xs: 8, md: 15 },
      }}
    >
      <Typography
        variant="overline"
        sx={{
          display: "block",
          color: "primary.main",
        }}
      >
        O nas
      </Typography>

      <Grid
        container
        spacing={3}
        alignItems={{ md: "center" }}
        justifyContent={{ md: "space-between" }}
      >
        {mdUp && (
          <Grid xs={12} md={6} lg={5}>
            <Image
              alt="about"
              src="/assets/images/course/course_6.jpg"
              ratio="4/6"
              sx={{ borderRadius: 2 }}
            />
          </Grid>
        )}

        <Grid xs={12} md={6} lg={6}>
          <Typography variant="h3" sx={{ mb: 3 }}>
            Szkoła programowania dla każdego
          </Typography>

          <Stack sx={{ gap: 2 }}>
            <Typography sx={{ color: "text.secondary" }}>
              W{" "}
              <Typography
                variant="overline"
                sx={{
                  fontSize: 15,
                  color: "primary.main",
                }}
              >
                {packageInfo.name}
              </Typography>{" "}
              naszą misją jest umożliwienie zarówno początkującym entuzjastom, jak i doświadczonym
              inżynierom oprogramowania rozwijania swojej wiedzy i umiejętności w dynamicznym
              świecie programowania. Zobowiązujemy się tworzyć otoczenie edukacyjne online, które
              jest dostępne i wspierające, zapewniając społeczność, w której ceni się ciekawość, a
              współpraca jest kluczowa.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              Naszym celem jest demistyfikacja złożoności programowania, uczynienie go dostępnym dla
              nowych uczestników poprzez dostarczanie angażujących i kompleksowych kursów. Dla
              początkujących oferujemy strukturyzowaną ścieżkę nauki, budującą solidne podstawy,
              podczas gdy dla doświadczonych programistów dostarczamy zaawansowanych kursów, aby
              poszerzyć ich ekspertyzę i być na bieżąco z nieustannie zmieniającym się krajobrazem
              technologicznym.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              W centrum naszej misji leży przekonanie, że każdy powinien mieć możliwość nauki i
              rozwoju w dziedzinie programowania. Dążymy do uczynienia edukacji elastyczną i
              wygodną, oferując różnorodne kursy dostosowane do różnych harmonogramów i preferencji
              uczących się. Nasi doświadczeni instruktorzy pasjonują się dzieleniem się wiedzą,
              prowadzeniem uczestników przez praktyczne projekty i zapewnianiem wsparcia podczas
              całego procesu nauki.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              Dołącz do nas w{" "}
              <Typography
                variant="overline"
                sx={{
                  fontSize: 15,
                  color: "primary.main",
                }}
              >
                {packageInfo.name}
              </Typography>
              , gdzie nauka nie zna ograniczeń, a razem kształtujemy przyszłość programowania.
            </Typography>
          </Stack>

          <Stack
            direction={{ xs: "column", md: "row" }}
            spacing={{ xs: 5, md: 10 }}
            sx={{ mt: { xs: 8, md: 6 } }}
          >
            <Stack spacing={3}>
              <Box sx={{ width: 24, height: 3, bgcolor: "primary.main" }} />
              <Typography sx={{ color: "text.secondary" }}>
                Dla osób chcących zostać programistą
              </Typography>
            </Stack>

            <Stack spacing={3}>
              <Box sx={{ width: 24, height: 3, bgcolor: "primary.main" }} />
              <Typography sx={{ color: "text.secondary" }}>
                Dla obecnych programistów chcących zwiększyć swoje umiejętności
              </Typography>
            </Stack>
          </Stack>
        </Grid>
      </Grid>
    </Container>
  );
}
