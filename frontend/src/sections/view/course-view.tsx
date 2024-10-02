"use client";

import { useMemo } from "react";

import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { paths } from "src/routes/paths";

import { useResponsive } from "src/hooks/use-responsive";

import { createMetadata } from "src/utils/create-metadata";

import { useCourse } from "src/api/courses/course";
import { useCourses } from "src/api/courses/courses";
import { useBestCourses } from "src/api/courses/best-courses";

import { SplashScreen } from "src/components/loading-screen";

import Review from "src/sections/review/review";
import NotFoundView from "src/sections/error/not-found-view";

import { ICourseProps, ICourseLessonProp, ICourseModuleProp } from "src/types/course";

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

  const { data: course, isLoading: isLoadingCourse } = useCourse(id);
  const { data: bestCourses, isLoading: isLoadingBestCourses } = useBestCourses();

  const technologies = useMemo(() => course?.category.join(","), [course?.category]);
  const query = { page_size: -1 };

  const { data: courses, isLoading: isLoadingCourses } = useCourses(
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
    () =>
      course?.modules
        ?.map((module: ICourseModuleProp) => module.lessons)
        .flat() as ICourseLessonProp[],
    [course?.modules],
  );

  const technologyKeywords = useMemo(
    () =>
      course?.category
        .map((category: string) => [
          `${category} online`,
          `nauka ${category}`,
          `programowanie ${category}`,
          `${category} od podstaw`,
          `certyfikat ${category}`,
          `zajęcia z ${category}`,
        ])
        .flat(),
    [course?.category],
  );

  const metadata = useMemo(
    () =>
      createMetadata(
        `Kurs: ${course?.slug}`,
        `Zapisz się na kurs ${course?.slug} w loop i naucz się programować. Oferujemy praktyczne lekcje online z certyfikatem ukończenia oraz wsparcie doświadczonych instruktorów.`,
        [
          `kurs ${course?.slug}`,
          "kursy programowania",
          "szkoła programowania loop",
          "kurs programowania",
          ...(technologyKeywords ?? []),
        ],
      ),
    [course?.slug, technologyKeywords],
  );

  const isLoading = isLoadingCourse || isLoadingBestCourses || isLoadingCourses;

  if (isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(course).length === 0) {
    return <NotFoundView />;
  }

  return (
    <>
      <title>{metadata.title}</title>
      <meta name="description" content={metadata.description} />
      <meta name="keywords" content={metadata.keywords} />

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
        courseId={id}
        teacherId=""
        ratingNumber={course.ratingNumber}
        reviewNumber={course.totalReviews}
        lessons={allLessons ?? []}
        teachers={course.teachers ?? []}
      />

      {similarCourses?.length === 3 && <CourseListSimilar courses={similarCourses} />}

      <Newsletter />
    </>
  );
}
