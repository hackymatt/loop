"use client";

import { useMemo } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { SelectChangeEvent } from "@mui/material";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { useCourses, useCoursesPagesCount } from "src/api/courses/courses";

import Iconify from "src/components/iconify";

import NotFoundView from "src/sections/error/not-found-view";

import Newsletter from "../newsletter";
import Filters from "../filters/filters";
import Sorting from "../sorting/sorting";
import CourseList from "../list/course-list";

// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: "-students_count", label: "Popularność: największa" },
  { value: "-rating", label: "Ocena: najlepsza" },
  { value: "price", label: "Cena: od najniższej" },
  { value: "-price", label: "Cena: od najwyższej" },
];

export default function CoursesView() {
  const mobileOpen = useBoolean();
  const { setQueryParam, getQueryParams } = useQueryParams();

  const query = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useCoursesPagesCount(query);
  const { data: courses, isLoading } = useCourses(query);

  const handleChange = (name: string, value?: string | number) => {
    setQueryParam(name, value);
  };

  if (pagesCount === 0) {
    return <NotFoundView />;
  }

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
            {courses?.length > 0 && (
              <Stack direction="row" alignItems="center" justifyContent="right" sx={{ mb: 5 }}>
                <Sorting
                  value={query.sort_by ?? "-students_count"}
                  options={SORT_OPTIONS}
                  onChange={(event: SelectChangeEvent) =>
                    handleChange("sort_by", event.target.value)
                  }
                />
              </Stack>
            )}

            <CourseList
              courses={courses}
              loading={isLoading}
              pagesCount={pagesCount}
              page={parseInt(query.page ?? "1", 10) ?? 1}
              onPageChange={(selectedPage: number) => handleChange("page", selectedPage)}
            />
          </Box>
        </Stack>
      </Container>

      <Newsletter />
    </>
  );
}
