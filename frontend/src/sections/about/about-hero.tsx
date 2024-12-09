import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import { alpha, useTheme } from "@mui/material";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

import { bgGradient } from "src/theme/css";

import Image from "src/components/image";

// ----------------------------------------------------------------------

export default function AboutHero() {
  const theme = useTheme();
  return (
    <Box
      component="section"
      sx={{
        ...bgGradient({
          color: `to bottom, ${alpha(theme.palette.background.default, 0.9)}, ${alpha(theme.palette.background.default, 0.9)}`,
          imgUrl: "/assets/background/overlay-1.webp",
        }),
        overflow: "hidden",
        position: "relative",
        py: { xs: 10, md: 20 },
      }}
    >
      <Box
        component="img"
        alt="Texture"
        src="/assets/background/texture-1.webp"
        sx={{
          top: 0,
          right: 0,
          zIndex: 8,
          opacity: 0.24,
          position: "absolute",
          height: `calc(100% + 80px)`,
        }}
      />
      <Container>
        <Grid container spacing={{ xs: 8, md: 3 }} justifyContent="space-between">
          <Grid
            xs={12}
            md={6}
            lg={5}
            sx={{
              color: "grey.800",
              textAlign: { xs: "center", md: "left" },
            }}
          >
            <Typography variant="h1">Kursy online</Typography>

            <Typography sx={{ mt: 3, mb: 6 }}>
              Nasza szkoła oferuje wysokiej jakości kursy programowania, które są dostosowane do
              różnych poziomów umiejętności - od początkujących po zaawansowanych programistów. Nasi
              doświadczeni instruktorzy zapewniają praktyczną wiedzę z obszaru programowania,
              umożliwiając studentom zdobycie niezbędnych umiejętności do skutecznego rozwoju w
              dziedzinie technologii. Dodatkowo, nasze kursy są elastyczne i dostępne w trybie
              online, aby sprostać potrzebom każdego zainteresowanego nauką programowania.
            </Typography>

            <Button variant="contained" size="large" color="primary" href={paths.courses}>
              Przeglądaj kursy
            </Button>
          </Grid>

          <Grid xs={12} md={6} lg={6}>
            <Image
              alt="kurs-programowania-online"
              src="/assets/illustrations/illustration_courses_hero.svg"
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
