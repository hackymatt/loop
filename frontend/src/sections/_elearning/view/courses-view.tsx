"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { useBoolean } from "src/hooks/use-boolean";

import { useCourses, useCoursesPagesCount } from "src/api/courses/courses";

import Iconify from "src/components/iconify";

import Newsletter from "../newsletter";
import Filters from "../filters/filters";
import CourseList from "../list/course-list";

// ----------------------------------------------------------------------

export default function CoursesView() {
  const mobileOpen = useBoolean();
  const searchParams = useSearchParams();

  const { data: pagesCount } = useCoursesPagesCount();

  const params = new URLSearchParams(searchParams);
  const pageParam = parseInt(params.get("page") ?? "1", 10);
  const urlPage = Number.isNaN(pageParam) ? 1 : pageParam;

  const [page, setPage] = useState<number>(Math.min(urlPage, pagesCount));

  const { data: courses, isLoading } = useCourses(page);

  return (
    <>
      <Container sx={{ mb: 10 }}>
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="space-between"
          sx={{
            py: 5,
          }}
        >
          <Typography variant="h2">Kursy</Typography>

          <Button
            color="inherit"
            variant="contained"
            startIcon={<Iconify icon="carbon:filter" width={18} />}
            onClick={mobileOpen.onTrue}
            sx={{
              display: { md: "none" },
            }}
          >
            Filtry
          </Button>
        </Stack>

        <Stack direction={{ xs: "column", md: "row" }}>
          <Filters open={mobileOpen.value} onClose={mobileOpen.onFalse} />

          <Box
            sx={{
              flexGrow: 1,
              pl: { md: 8 },
              width: { md: `calc(100% - ${280}px)` },
            }}
          >
            <CourseList
              courses={courses}
              loading={isLoading}
              pagesCount={pagesCount}
              onPageChange={(selectedPage: number) => setPage(selectedPage)}
            />
          </Box>
        </Stack>
      </Container>

      <Newsletter />
    </>
  );
}
