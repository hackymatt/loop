import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import {
  Carousel,
  useCarousel,
  CarouselDotButtons,
  CarouselArrowBasicButtons,
} from "src/components/carousel";

import { ICourseProps } from "src/types/course";

import CourseItem from "../list/course-item";

// ----------------------------------------------------------------------

type Props = {
  courses: ICourseProps[];
};

export default function LandingFeaturedCourses({ courses }: Props) {
  const carousel = useCarousel({
    slideSpacing: "32px",
    slidesToShow: { xs: 1, md: 2, lg: 3 },
  });

  return (
    <Container
      sx={{
        pt: { xs: 5, md: 10 },
      }}
    >
      <Stack
        direction={{ xs: "column", md: "row" }}
        alignItems={{ md: "flex-end" }}
        sx={{
          textAlign: { xs: "center", md: "unset" },
        }}
      >
        <Stack spacing={3} flexGrow={1}>
          <Typography variant="h2">Polecane kursy</Typography>
          <Typography sx={{ color: "text.secondary" }}>
            Sprawdź poniższe kursy, które są najbardziej doceniane przez studentów.
          </Typography>
        </Stack>

        <CarouselArrowBasicButtons
          {...carousel.arrows}
          options={carousel.options}
          sx={{ gap: 1, display: { xs: "none", md: "inline-flex" } }}
        />
      </Stack>

      <Box
        sx={{
          position: "relative",
          ml: { md: -2 },
          width: { md: "calc(100% + 32px)" },
        }}
      >
        <Carousel
          carousel={carousel}
          sx={{
            px: 0.5,
            py: { xs: 5, md: 10 },
          }}
        >
          {courses.map((course) => (
            <Box
              key={course.id}
              sx={{
                px: 2,
              }}
            >
              <CourseItem course={course} vertical />
            </Box>
          ))}
        </Carousel>

        <CarouselDotButtons
          scrollSnaps={carousel.dots.scrollSnaps}
          selectedIndex={carousel.dots.selectedIndex}
          onClickDot={carousel.dots.onClickDot}
          sx={{
            color: "primary.main",
            justifyContent: "center",
            display: { xs: "flex", md: "none" },
          }}
        />
      </Box>
    </Container>
  );
}
