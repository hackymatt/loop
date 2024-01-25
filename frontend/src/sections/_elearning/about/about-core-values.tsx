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
      "Nasza szkoła kładzie nacisk na stałe dostosowywanie programów nauczania do najnowszych trendów i technologii, umożliwiając studentom naukę zgodną z aktualnymi wymaganiami rynku pracy.",
    icon: "streamline:ai-technology-spark",
  },
  {
    title: "Otwartość",
    description:
      "Nasza szkoła kładzie nacisk na zapewnienie przystępności cenowej kursów, aby umożliwić szerokiemu gronu uczniów korzystanie z wysokiej jakości edukacji bez dużego obciążenia finansowego.",
    icon: "nimbus:money",
  },
  {
    title: "Elastyczność",
    description:
      "Zdajemy sobie sprawę, że nasi studenci mają różnorodne zobowiązania, dlatego oferujemy elastyczność w harmonogramie kursów, aby umożliwić dostosowanie nauki do indywidualnych potrzeb i czasu każdego uczestnika.",
    icon: "cil:calendar",
  },
  {
    title: "Dostępność",
    description:
      "Zapewniamy dostęp do wysokiej jakości edukacji programowania z dowolnego miejsca na świecie, umożliwiając elastyczność i swobodę nauki online.",
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
