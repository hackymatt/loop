import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

import Iconify from "src/components/iconify";
import TextMaxLine from "src/components/text-max-line";

import { ICourseByTechnologyProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  technologies: ICourseByTechnologyProps[];
};

export default function LandingTechnologies({ technologies }: Props) {
  const TECHNOLOGIES_SLOTS: number = 9 as const;
  return (
    <Box
      sx={{
        overflow: "hidden",
        bgcolor: "background.neutral",
        py: { xs: 10, md: 15 },
      }}
    >
      <Container>
        <Grid container spacing={{ xs: 8, lg: 3 }} justifyContent={{ lg: "space-between" }}>
          <Grid
            xs={12}
            lg={4}
            sx={{
              textAlign: { xs: "center", lg: "unset" },
            }}
          >
            <Typography variant="h2">Polecane technologie</Typography>

            <Typography sx={{ color: "text.secondary", mt: 2, mb: 5 }}>
              Sprawdź technologie dostępne w naszych kursach
            </Typography>

            {technologies.length > TECHNOLOGIES_SLOTS && (
              <Button
                variant="contained"
                size="large"
                color="inherit"
                href={paths.courses}
                endIcon={<Iconify icon="carbon:chevron-right" />}
              >
                Zobacz więcej
              </Button>
            )}
          </Grid>

          <Grid xs={12} lg={7}>
            <Box
              sx={{
                gap: 3,
                display: "grid",
                gridTemplateColumns: {
                  xs: "repeat(2, 1fr)",
                  md: "repeat(3, 1fr)",
                },
              }}
            >
              {technologies
                .slice(0, TECHNOLOGIES_SLOTS)
                .map((technology: ICourseByTechnologyProps) => (
                  <Button
                    key={technology.id}
                    href={`${paths.courses}?technology_in=${technology.name}`}
                    sx={{ borderRadius: 1.5, padding: 0 }}
                  >
                    <TechnologyItem key={technology.id} technology={technology} />
                  </Button>
                ))}
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

// ----------------------------------------------------------------------

type TechnologyItemProps = {
  technology: ICourseByTechnologyProps;
};

function TechnologyItem({ technology }: TechnologyItemProps) {
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 3,
        width: "100%",
        borderRadius: 1.5,
        cursor: "pointer",
        bgcolor: "transparent",
        transition: (theme) =>
          theme.transitions.create("all", {
            duration: theme.transitions.duration.enteringScreen,
          }),
        "&:hover": {
          bgcolor: "background.paper",
          boxShadow: (theme) => theme.customShadows.z24,
          h6: {
            color: "primary.main",
          },
        },
      }}
    >
      <TextMaxLine variant="h6" line={1}>
        {technology.name}
      </TextMaxLine>

      {technology.totalStudents && (
        <Typography variant="body2" sx={{ mt: 1, color: "text.disabled" }}>
          {technology.totalStudents}{" "}
          {polishPlurals("kurs", "kursy", "kursów", technology.totalStudents)}
        </Typography>
      )}
    </Paper>
  );
}
