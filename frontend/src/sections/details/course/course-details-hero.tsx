import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Fab from "@mui/material/Fab";
import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { alpha, useTheme } from "@mui/material/styles";

import { paths } from "src/routes/paths";

import { useBoolean } from "src/hooks/use-boolean";

import { fShortenNumber } from "src/utils/format-number";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import { PlayerDialog } from "src/components/player";
import CustomBreadcrumbs from "src/components/custom-breadcrumbs";

import { ILevel, ICourseProps, ICourseLessonProp, ICourseModuleProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
};

export default function CourseDetailsHero({ course }: Props) {
  const {
    slug,
    level,
    modules,
    category: categories,
    coverUrl,
    video,
    totalHours,
    description,
    ratingNumber,
    totalReviews,
    totalStudents,
    teachers = [],
  } = course;

  const theme = useTheme();

  const videoOpen = useBoolean();

  const genderAvatarUrl =
    teachers?.[0]?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = teachers?.[0]?.avatarUrl || genderAvatarUrl;

  const allLessons = useMemo(
    () =>
      course?.modules
        ?.map((module: ICourseModuleProp) => module.lessons)
        .flat() as ICourseLessonProp[],
    [course?.modules],
  );

  return (
    <>
      <Box
        sx={{
          bgcolor: "background.neutral",
          pb: { xs: 5, md: 10 },
        }}
      >
        <Container sx={{ overflow: "hidden" }}>
          <CustomBreadcrumbs
            links={[
              { name: "Strona główna", href: "/" },
              { name: "Kursy", href: paths.courses },
              { name: course.slug || "" },
            ]}
            sx={{
              pt: 5,
              mb: { xs: 5, md: 10 },
            }}
          />

          <Grid container spacing={{ xs: 5, md: 10 }} direction="row-reverse">
            <Grid xs={12} md={5}>
              <Stack
                alignItems="center"
                justifyContent="center"
                sx={{
                  position: "relative",
                  borderRadius: 2,
                  overflow: "hidden",
                }}
              >
                {video && (
                  <Fab
                    color="primary"
                    onClick={videoOpen.onTrue}
                    sx={{
                      zIndex: 9,
                      position: "absolute",
                    }}
                  >
                    <Iconify icon="carbon:play" width={24} />
                  </Fab>
                )}

                <Image
                  alt="hero"
                  src={coverUrl}
                  overlay={`linear-gradient(to bottom, ${alpha(
                    theme.palette.common.black,
                    0,
                  )} 0%, ${theme.palette.common.black} 100%)`}
                />
              </Stack>
            </Grid>

            <Grid xs={12} md={7}>
              <Stack spacing={3}>
                <Stack spacing={2} alignItems="flex-start">
                  {categories && (
                    <Stack
                      spacing={0.5}
                      direction="row"
                      alignItems="center"
                      flexWrap="wrap"
                      divider={
                        <Box
                          sx={{
                            width: 4,
                            height: 4,
                            bgcolor: "text.disabled",
                            borderRadius: "50%",
                          }}
                        />
                      }
                    >
                      {categories.map((category: string) => (
                        <Typography
                          key={category}
                          variant="overline"
                          sx={{ color: "primary.main" }}
                        >
                          {category}
                        </Typography>
                      ))}
                    </Stack>
                  )}

                  <Typography variant="h3" component="h1">
                    {slug}
                  </Typography>

                  <Typography sx={{ color: "text.secondary", textAlign: "justify" }}>
                    {description}
                  </Typography>
                </Stack>

                <Stack
                  spacing={1.5}
                  direction="row"
                  alignItems="center"
                  divider={<Divider orientation="vertical" sx={{ height: 20 }} />}
                >
                  {totalReviews > 0 && (
                    <Stack spacing={0.5} direction="row" alignItems="center">
                      <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                      <Box sx={{ typography: "h6" }}>
                        {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
                      </Box>

                      {totalReviews && (
                        <Typography variant="body2" sx={{ color: "text.secondary" }}>
                          ({fShortenNumber(totalReviews)}{" "}
                          {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
                        </Typography>
                      )}
                    </Stack>
                  )}

                  {totalStudents > 0 && (
                    <Stack direction="row" sx={{ typography: "subtitle2" }}>
                      {fShortenNumber(totalStudents)}
                      <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                        {polishPlurals("student", "studentów", "studentów", totalStudents)}
                      </Box>
                    </Stack>
                  )}
                </Stack>

                {teachers?.length > 0 && (
                  <Stack direction="row" alignItems="center">
                    <Avatar src={avatarUrl} />
                    <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                      {teachers[0]?.name}
                    </Typography>
                    {teachers?.length > 1 && (
                      <Link underline="always" color="text.secondary" variant="body2">
                        + {teachers.length - 1}{" "}
                        {polishPlurals(
                          "nauczyciel",
                          "nauczycieli",
                          "nauczycieli",
                          teachers.length - 1,
                        )}
                      </Link>
                    )}
                  </Stack>
                )}

                <Divider sx={{ borderStyle: "dashed" }} />

                <Stack spacing={2}>
                  <Stack
                    direction="row"
                    flexWrap="wrap"
                    sx={{
                      "& > *": { my: 0.5, mr: 3 },
                    }}
                  >
                    <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                      <Iconify icon="carbon:time" sx={{ mr: 1 }} />{" "}
                      {totalHours < 1 ? totalHours : fShortenNumber(Math.floor(totalHours), 0)}+{" "}
                      {polishPlurals("godzina", "godziny", "godzin", totalHours)}
                    </Stack>

                    {modules && (
                      <>
                        <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                          <Iconify icon="carbon:document-multiple-01" sx={{ mr: 1 }} />
                          {`${modules.length} ${polishPlurals(
                            "moduł",
                            "moduły",
                            "modułów",
                            modules.length,
                          )}`}
                        </Stack>

                        <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                          <Iconify icon="carbon:document" sx={{ mr: 1 }} />
                          {`${allLessons.length} ${polishPlurals(
                            "lekcja",
                            "lekcje",
                            "lekcji",
                            allLessons.length,
                          )}`}
                        </Stack>
                      </>
                    )}

                    <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                      <Iconify
                        icon={
                          (level === ("Podstawowy" as ILevel) && "carbon:skill-level") ||
                          (level === ("Średniozaawansowany" as ILevel) &&
                            "carbon:skill-level-basic") ||
                          (level === ("Zaawansowany" as ILevel) &&
                            "carbon:skill-level-intermediate") ||
                          "carbon:skill-level-advanced"
                        }
                        sx={{ mr: 1 }}
                      />
                      {level}
                    </Stack>
                  </Stack>
                </Stack>
              </Stack>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {video && (
        <PlayerDialog open={videoOpen.value} onClose={videoOpen.onFalse} videoPath={video} />
      )}
    </>
  );
}
