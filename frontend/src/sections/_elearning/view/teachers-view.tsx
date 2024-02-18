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

import { useLecturers, useLecturersPagesCount } from "src/api/lecturers/lecturers";

import Iconify from "src/components/iconify";
import { SplashScreen } from "src/components/loading-screen";

import NotFoundView from "src/sections/error/not-found-view";

import Newsletter from "../newsletter/newsletter";
import Sorting from "../sorting/sorting";
import TeacherList from "../list/teacher-list";
import Filters from "../filters/teacher-filters";

// ----------------------------------------------------------------------

const SORT_OPTIONS = [
  { value: "-rating", label: "Ocena: najlepsza" },
  { value: "user_title", label: "Rola: od A do Z" },
  { value: "-user_title", label: "Rola: od Z do A" },
  { value: "full_name", label: "Imię i Nazwisko: od A do Z" },
  { value: "-full_name", label: "Imię i Nazwisko: od Z do A" },
];

export default function TeachersView() {
  const mobileOpen = useBoolean();
  const { setQueryParam, getQueryParams } = useQueryParams();

  const query = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount, isLoading: isLoadingLecturersPagesCount } =
    useLecturersPagesCount(query);
  const { data: lecturers, isLoading: isLoadingLecturers } = useLecturers(query);

  const handleChange = (name: string, value?: string | number) => {
    setQueryParam(name, value);
  };

  const isLoading = isLoadingLecturers || isLoadingLecturersPagesCount;

  if (isLoading) {
    return <SplashScreen />;
  }

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
          <Typography variant="h2">Instruktorzy</Typography>

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
            {lecturers?.length > 0 && (
              <Stack direction="row" alignItems="center" justifyContent="right" sx={{ mb: 5 }}>
                <Sorting
                  value={query.sort_by ?? "-rating"}
                  options={SORT_OPTIONS}
                  onChange={(event: SelectChangeEvent) =>
                    handleChange("sort_by", event.target.value)
                  }
                />
              </Stack>
            )}

            <TeacherList
              teachers={lecturers}
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
