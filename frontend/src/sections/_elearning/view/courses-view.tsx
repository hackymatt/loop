"use client";

import { useState, useEffect } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";

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
  const pathname = usePathname();
  const { replace } = useRouter();
  const searchParams = useSearchParams();

  const params = new URLSearchParams(searchParams);

  const { data: pagesCount } = useCoursesPagesCount();

  const pageParam = parseInt(params.get("page") ?? "1", 10);
  const urlPage = Number.isNaN(pageParam) ? 1 : pageParam;

  const [page, setPage] = useState<number>(1);

  useEffect(() => {
    if (pagesCount) {
      setPage(Math.min(urlPage, Number.isNaN(pagesCount) ? 1 : pagesCount));
    }
  }, [pagesCount, urlPage]);

  const { data: courses, isLoading } = useCourses(page);

  const handlePageChange = (selectedPage: number) => {
    setPage(selectedPage);
    params.set("page", selectedPage.toString());
    replace(`${pathname}?${params.toString()}`);
  };

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
              page={page}
              onPageChange={(selectedPage: number) => handlePageChange(selectedPage)}
            />
          </Box>
        </Stack>
      </Container>

      <Newsletter />
    </>
  );
}
