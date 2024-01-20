"use client";

import { useEffect } from "react";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { useBoolean } from "src/hooks/use-boolean";
import { useResponsive } from "src/hooks/use-responsive";

import { _mock, _socials, _courses } from "src/_mock";

import Iconify from "src/components/iconify";
import { SplashScreen } from "src/components/loading-screen";

import ReviewElearning from "src/sections/review/elearning/review-elearning";

import Advertisement from "../../advertisement";
import ElearningNewsletter from "../newsletter";
import CourseListSimilar from "../list/course-list-similar";
import CourseDetailsHero from "../details/course-details-hero";
import CourseDetailsInfo from "../details/course-details-info";
import CourseDetailsSummary from "../details/course-details-summary";
import CourseDetailsTeachersInfo from "../details/course-details-teachers-info";

// ----------------------------------------------------------------------

const _mockCourse = _courses[0];

export default function CourseView({ id }: { id: string }) {
  const mdUp = useResponsive("up", "md");

  const loading = useBoolean(false);

  const courseSimilar = _courses.slice(-3);

  if (loading.value) {
    return <SplashScreen />;
  }

  return (
    <>
      <CourseDetailsHero course={_mockCourse} />

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

            <Stack direction="row" flexWrap="wrap" sx={{ mt: 5 }}>
              <Typography variant="subtitle2" sx={{ mt: 0.75, mr: 1.5 }}>
                Share:
              </Typography>

              <Stack direction="row" alignItems="center" flexWrap="wrap">
                {_socials.map((social) => (
                  <Button
                    key={social.value}
                    size="small"
                    variant="outlined"
                    startIcon={<Iconify icon={social.icon} />}
                    sx={{
                      m: 0.5,
                      flexShrink: 0,
                      color: social.color,
                      borderColor: social.color,
                      "&:hover": {
                        borderColor: social.color,
                        bgcolor: alpha(social.color, 0.08),
                      },
                    }}
                  >
                    {social.label}
                  </Button>
                ))}
              </Stack>
            </Stack>

            <Divider sx={{ my: 5 }} />

            <CourseDetailsTeachersInfo teachers={_mockCourse.teachers} />
          </Grid>

          <Grid xs={12} md={5} lg={4}>
            <Stack spacing={5}>
              {mdUp && <CourseDetailsInfo course={_mockCourse} />}

              <Advertisement
                advertisement={{
                  title: "Advertisement",
                  description: "Duis leo. Donec orci lectus, aliquam ut, faucibus non",
                  imageUrl: _mock.image.course(7),
                  path: "",
                }}
              />
            </Stack>
          </Grid>
        </Grid>
      </Container>

      {mdUp && <Divider />}

      <ReviewElearning />

      <CourseListSimilar courses={courseSimilar} />

      <ElearningNewsletter />
    </>
  );
}
