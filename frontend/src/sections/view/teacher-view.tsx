"use client";

import { useMemo } from "react";

import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { paths } from "src/routes/paths";

import { useResponsive } from "src/hooks/use-responsive";

import { decodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";

import { useLecturer } from "src/api/lecturers/lecturer";

import { SplashScreen } from "src/components/loading-screen";

import NotFoundView from "src/sections/error/not-found-view";

import Review from "../review/review";
import Advertisement from "../advertisement";
import Newsletter from "../newsletter/newsletter";
import TeacherDetailsHero from "../details/teacher/teacher-details-hero";
import TeacherDetailsInfo from "../details/teacher/teacher-details-info";
import TeacherDetailsSummary from "../details/teacher/teacher-details-summary";

// ----------------------------------------------------------------------

export default function TeacherView({ id }: { id: string }) {
  const mdUp = useResponsive("up", "md");

  const decodedId = decodeUrl(id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { data: teacher, isLoading } = useLecturer(recordId);

  const metadata = useMemo(
    () =>
      createMetadata(
        `Instruktor ${teacher?.name} - sprawdź oferowane lekcje`,
        `Poznaj ${teacher?.name} — doświadczonego instruktora w loop. ${teacher?.description} Sprawdź jego profil, lekcje, które prowadzi, oraz opinie studentów. Rozpocznij naukę programowania pod okiem profesjonalisty!`,
        [
          "profil instruktora",
          "instruktor programowania",
          "loop instruktor",
          "nauczyciel programowania",
          "opinie o instruktorze",
          "kursy prowadzone przez instruktora",
          "doświadczenie instruktora",
          "specjalizacje instruktora",
          "mentor programistyczny",
          "szkoła programowania",
        ],
      ),
    [teacher?.description, teacher?.name],
  );

  if (isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(teacher).length === 0) {
    return <NotFoundView />;
  }

  return (
    <>
      <title>{metadata.title}</title>
      <meta name="description" content={metadata.description} />
      <meta name="keywords" content={metadata.keywords} />

      <TeacherDetailsHero teacher={teacher} />

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
              <TeacherDetailsInfo teacher={teacher} />
            </Grid>
          )}

          <Grid xs={12} md={7} lg={8}>
            <TeacherDetailsSummary teacher={teacher} />
          </Grid>

          <Grid xs={12} md={5} lg={4}>
            <Stack spacing={5}>
              {mdUp && <TeacherDetailsInfo teacher={teacher} />}

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
        courseId=""
        teacherId={teacher.id}
        ratingNumber={teacher.ratingNumber ?? 0}
        reviewNumber={teacher.totalReviews ?? 0}
        lessons={teacher.lessons ?? []}
        teachers={[]}
      />

      <Newsletter />
    </>
  );
}
