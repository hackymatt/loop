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
              alt="o-nas"
              src="/assets/images/general/course-6.webp"
              ratio="3/4"
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
              Nazwa{" "}
              <Box component="span" sx={{ color: "primary.main" }}>
                loop
              </Box>{" "}
              odzwierciedla jedną z najważniejszych struktur w programowaniu — pętlę (ang. loop).
              Symbolizuje ciągłe doskonalenie, powtarzalność i nieustanny rozwój — wartości, które
              są kluczowe w nauce programowania. Dzięki regularnemu powtarzaniu i ulepszaniu swoich
              umiejętności można osiągnąć biegłość w kodowaniu, a to właśnie chcemy umożliwić
              każdemu, kto dołączy do naszych kursów.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              W{" "}
              <Box component="span" sx={{ color: "primary.main" }}>
                loop
              </Box>{" "}
              naszą misją jest wspieranie zarówno początkujących entuzjastów, jak i doświadczonych
              inżynierów oprogramowania w rozwijaniu ich wiedzy i umiejętności w dynamicznym świecie
              programowania. Tworzymy przyjazne, dostępne środowisko edukacyjne, gdzie ciekawość i
              współpraca są na pierwszym miejscu.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              Naszym celem jest uproszczenie złożoności programowania i uczynienie go przystępnym
              dla wszystkich. Oferujemy angażujące i wszechstronne kursy, które dostarczają solidne
              podstawy dla nowicjuszy oraz zaawansowaną wiedzę dla doświadczonych programistów,
              pomagając im nadążyć za nieustannie zmieniającym się krajobrazem technologicznym.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              Wierzymy, że każdy powinien mieć możliwość nauki i rozwoju w dziedzinie programowania.
              Dlatego zapewniamy elastyczne i wygodne opcje edukacyjne, dostosowane do różnych
              harmonogramów i preferencji. Nasi doświadczeni instruktorzy z pasją dzielą się swoją
              wiedzą, prowadząc uczestników przez praktyczne projekty i oferując wsparcie na każdym
              etapie nauki.
            </Typography>

            <Typography sx={{ color: "text.secondary" }}>
              Dołącz do nas w{" "}
              <Box component="span" sx={{ color: "primary.main" }}>
                loop
              </Box>{" "}
              gdzie nauka nie zna ograniczeń, a razem kształtujemy przyszłość programowania.
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
