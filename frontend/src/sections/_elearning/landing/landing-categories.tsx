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

import { ICourseByCategoryProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  categories: ICourseByCategoryProps[];
};

export default function LandingCategories({ categories }: Props) {
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

            {categories.length > 9 && (
              <Button
                variant="contained"
                size="large"
                color="inherit"
                href={paths.eLearning.courses}
                endIcon={<Iconify icon="carbon:chevron-right" />}
                sx={{ textTransform: "none" }}
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
              {categories.slice(0, 9).map((category) => (
                <CategoryItem key={category.id} category={category} />
              ))}
            </Box>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

// ----------------------------------------------------------------------

type CategoryItemProps = {
  category: ICourseByCategoryProps;
};

function CategoryItem({ category }: CategoryItemProps) {
  return (
    <Paper
      variant="outlined"
      sx={{
        p: 3,
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
        {category.name}
      </TextMaxLine>

      <Typography variant="body2" sx={{ mt: 1, color: "text.disabled" }}>
        {category.totalStudents}{" "}
        {polishPlurals("student", "studentów", "studentów", category.totalStudents)}
      </Typography>
    </Paper>
  );
}
