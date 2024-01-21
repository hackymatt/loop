"use client";

import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { useResponsive } from "src/hooks/use-responsive";

import { _mock, _courses } from "src/_mock";
import { useCourse } from "src/api/course/course";
import { useBestCourses } from "src/api/courses/best-courses";

import { SplashScreen } from "src/components/loading-screen";

import Review from "src/sections/review/elearning/review";
import NotFoundView from "src/sections/error/not-found-view";

import Newsletter from "../newsletter";
import Advertisement from "../../advertisement";
import CourseListSimilar from "../list/course-list-similar";
import CourseDetailsHero from "../details/course-details-hero";
import CourseDetailsInfo from "../details/course-details-info";
import CourseDetailsSummary from "../details/course-details-summary";
import CourseDetailsTeachersInfo from "../details/course-details-teachers-info";

// ----------------------------------------------------------------------

const _mockCourse = _courses[0];

export default function CourseView({ id }: { id: string }) {
  const mdUp = useResponsive("up", "md");

  const { data: course, isLoading } = useCourse(id);
  const { data: bestCourses } = useBestCourses();

  const courseSimilar = _courses.slice(-3);

  if (isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(course).length === 0) {
    return <NotFoundView />;
  }

  return (
    <>
      <CourseDetailsHero course={course} />

      <Container
        sx={{
          overflow: "hidden",
          pt: { xs: 5, md: 10 },
          pb: { xs: 15, md: 10 },
        }}
      >
        <Grid container spacing={{ xs: 5, md: 8 }}>
          {!mdUp && (
            <Grid xs={12}>
              <CourseDetailsInfo course={_mockCourse} />
            </Grid>
          )}

          <Grid xs={12} md={7} lg={8}>
            <CourseDetailsSummary course={_mockCourse} />

            <Divider sx={{ my: 5 }} />

            <CourseDetailsTeachersInfo teachers={_mockCourse.teachers} />
          </Grid>

          <Grid xs={12} md={5} lg={4}>
            <Stack spacing={5}>
              {mdUp && <CourseDetailsInfo course={_mockCourse} />}

              <Advertisement
                advertisement={{
                  title: "Wejdź do IT",
                  description: "Sprawdź nasze kursy przygotowujące do pracy programisty",
                  imageUrl: _mock.image.course(7),
                  path: "/assets/images/course/course_8.jpg",
                }}
              />
            </Stack>
          </Grid>
        </Grid>
      </Container>

      {mdUp && <Divider />}

      <Review />

      {bestCourses?.length >= 1 && <CourseListSimilar courses={bestCourses} />}

      <Newsletter />
    </>
  );
}
