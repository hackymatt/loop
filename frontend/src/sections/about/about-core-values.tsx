import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

const CORE_VALUES = [
  {
    title: "Innowacyjność",
    description:
      "Stale dostosowujemy nasze kursy do najnowszych technologii i trendów, abyś zawsze był o krok przed wymaganiami rynku pracy.",
    icon: "streamline:ai-technology-spark",
  },
  {
    title: "Otwartość",
    description:
      "Oferujemy przystępne cenowo kursy, aby każdy miał szansę na rozwój i zdobycie nowych umiejętności bez dużych wydatków.",
    icon: "nimbus:money",
  },
  {
    title: "Elastyczność",
    description:
      "Dopasuj naukę do swojego harmonogramu – ucz się wtedy, kiedy masz czas i energię, bez zbędnych ograniczeń.",
    icon: "cil:calendar",
  },
  {
    title: "Dostępność",
    description:
      "Nasze kursy są dostępne online z każdego miejsca na świecie, co pozwala na naukę w pełni na Twoich warunkach.",
    icon: "wpf:worldwide-location",
  },
];

// ----------------------------------------------------------------------

export default function AboutCoreValues() {
  return (
    <Box
      sx={{
        overflow: "hidden",
        bgcolor: "background.neutral",
        py: { xs: 8, md: 15 },
      }}
    >
      <Container>
        <Stack
          spacing={3}
          direction={{ xs: "column", md: "row" }}
          justifyContent={{ md: "space-between" }}
          alignItems="center"
          sx={{
            mb: { xs: 8, md: 15 },
            textAlign: { xs: "center", md: "left" },
          }}
        >
          <Typography variant="h2">Główne wartości</Typography>

          <Typography sx={{ color: "text.secondary", maxWidth: { md: 540 } }}>
            W naszej szkole kierujemy się czterema kluczowymi wartościami, które definiują naszą
            misję i stanowią fundament naszych działań.
          </Typography>
        </Stack>

        <Grid container spacing={8}>
          {CORE_VALUES.map((value) => (
            <Grid
              key={value.title}
              xs={12}
              sm={6}
              md={3}
              sx={{
                textAlign: { xs: "center", md: "left" },
              }}
            >
              <Iconify icon={value.icon} width={48} sx={{ color: "primary.main" }} />

              <Typography variant="h5" sx={{ mt: 5, mb: 2 }}>
                {value.title}
              </Typography>

              <Typography sx={{ color: "text.secondary" }}> {value.description} </Typography>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
}
