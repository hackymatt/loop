"use client";

import { useMemo } from "react";

import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { paths } from "src/routes/paths";

import { useResponsive } from "src/hooks/use-responsive";

import { decodeUrl } from "src/utils/url-utils";

import { useCourse } from "src/api/courses/course";
import { useCourses } from "src/api/courses/courses";
import { useBestCourses } from "src/api/courses/best-courses";

import { SplashScreen } from "src/components/loading-screen";

import Review from "src/sections/review/review";
import NotFoundView from "src/sections/error/not-found-view";

import { ICourseProps, ICourseModuleProps, ICourseTechnologyProps } from "src/types/course";

import Advertisement from "../advertisement";
import Newsletter from "../newsletter/newsletter";
import CourseListSimilar from "../list/course-list-similar";
import CourseDetailsHero from "../details/course/course-details-hero";
import CourseDetailsInfo from "../details/course/course-details-info";
import CourseDetailsSummary from "../details/course/course-details-summary";
import CourseDetailsTeachersInfo from "../details/course/course-details-teachers-info";

// ----------------------------------------------------------------------

export default function CourseView({ id }: { id: string }) {
  const mdUp = useResponsive("up", "md");

  const decodedId = decodeUrl(id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { data: course, isLoading } = useCourse(recordId);
  const { data: bestCourses } = useBestCourses();

  const technologies = useMemo(
    () =>
      (course?.technologies ?? [])
        .map((technology: ICourseTechnologyProps) => technology.name)
        .join(","),
    [course?.technologies],
  );
  const query = { page_size: 3 };

  const { data: courses } = useCourses(
    technologies ? { ...query, technology_in: technologies } : query,
  );

  const similarCourses = useMemo(
    () =>
      [...(courses ?? []), ...(bestCourses ?? [])]
        .slice(0, 3)
        ?.filter((c: ICourseProps) => c.id !== course?.id),
    [bestCourses, course?.id, courses],
  );

  const allLessons = useMemo(
    () => (course?.modules ?? []).map((module: ICourseModuleProps) => module.lessons).flat(),
    [course?.modules],
  );

  if (!course || isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(course ?? {}).length === 0) {
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

            <CourseDetailsTeachersInfo teachers={course.teachers} />
          </Grid>

          <Grid xs={12} md={5} lg={4}>
            <Stack spacing={5}>
              {mdUp && <CourseDetailsInfo course={course} />}

              <Advertisement
                advertisement={{
                  title: "Wejdź do IT",
                  description: "Sprawdź nasze kursy przygotowujące do pracy programisty",
                  imageUrl: "/assets/images/general/course-8.webp",
                  path: paths.courses,
                }}
              />
            </Stack>
          </Grid>
        </Grid>
      </Container>

      {mdUp && <Divider />}

      <Review
        courseId={course.id}
        teacherId=""
        ratingNumber={course.ratingNumber ?? 0}
        reviewNumber={course.totalReviews}
        lessons={allLessons ?? []}
        teachers={course.teachers ?? []}
      />

      {similarCourses.length === 3 && <CourseListSimilar courses={similarCourses} />}

      <Newsletter />
    </>
  );
}
