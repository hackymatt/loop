"use client";

import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { useResponsive } from "src/hooks/use-responsive";

import { useCourse } from "src/api/courses/course";
import { useBestCourses } from "src/api/courses/best-courses";

import { SplashScreen } from "src/components/loading-screen";

import Review from "src/sections/review/review";
import NotFoundView from "src/sections/error/not-found-view";

import { ICourseProps } from "src/types/course";

import Advertisement from "../advertisement";
import Newsletter from "../newsletter/newsletter";
import CourseListSimilar from "../list/course-list-similar";
import CourseDetailsHero from "../details/course-details-hero";
import CourseDetailsInfo from "../details/course-details-info";
import CourseDetailsSummary from "../details/course-details-summary";
import CourseDetailsTeachersInfo from "../details/course-details-teachers-info";

// ----------------------------------------------------------------------

export default function CourseView({ id }: { id: string }) {
  const mdUp = useResponsive("up", "md");

  const { data: course, isLoading: isLoadingCourse } = useCourse(id);
  const { data: bestCourses, isLoading: isLoadingBestCourse } = useBestCourses();

  const similarCourses = bestCourses?.filter(
    (bestCourse: ICourseProps) => bestCourse.id !== course?.id,
  );

  const isLoading = isLoadingCourse || isLoadingBestCourse;

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
              <CourseDetailsInfo course={course} />
            </Grid>
          )}

          <Grid xs={12} md={7} lg={8}>
            <CourseDetailsSummary course={course} />

            <Divider sx={{ my: 5 }} />

            {course && <CourseDetailsTeachersInfo teachers={course.teachers} />}
          </Grid>

          <Grid xs={12} md={5} lg={4}>
            <Stack spacing={5}>
              {mdUp && <CourseDetailsInfo course={course} />}

              <Advertisement
                advertisement={{
                  title: "Wejdź do IT",
                  description: "Sprawdź nasze kursy przygotowujące do pracy programisty",
                  imageUrl: "/assets/images/course/course_8.jpg",
                  path: "/assets/images/course/course_8.jpg",
                }}
              />
            </Stack>
          </Grid>
        </Grid>
      </Container>

      {mdUp && <Divider />}

      <Review
        courseId={id}
        ratingNumber={course.ratingNumber}
        reviewNumber={course.totalReviews}
        lessons={course.lessons ?? []}
        teachers={course.teachers ?? []}
      />

      {similarCourses?.length >= 3 && <CourseListSimilar courses={similarCourses} />}

      <Newsletter />
    </>
  );
}
