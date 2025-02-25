"use client";

import { useMemo, useEffect, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import {
  List,
  Popover,
  ListItem,
  IconButton,
  ListItemText,
  ListItemButton,
  SelectChangeEvent,
  buttonBaseClasses,
} from "@mui/material";

import { usePathname } from "src/routes/hooks";

import { useBoolean } from "src/hooks/use-boolean";
import { usePopover } from "src/hooks/use-popover";
import { useQueryParams } from "src/hooks/use-query-params";

import { useCourses, useCoursesPagesCount } from "src/api/courses/courses";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { SplashScreen } from "src/components/loading-screen";

import NotFoundView from "src/sections/error/not-found-view";

import Sorting from "../sorting/sorting";
import CourseList from "../list/course-list";
import Filters from "../filters/course-filters";
import Newsletter from "../newsletter/newsletter";

// ----------------------------------------------------------------------

const MAIN_SORT_OPTIONS = [
  { value: "-students_count", label: "Popularność: największa" },
  { value: "-rating", label: "Ocena: najlepsza" },
  { value: "price", label: "Cena: od najniższej" },
  { value: "-price", label: "Cena: od najwyższej" },
];

const USER_SORT_OPTIONS = [{ value: "-progress", label: "Postęp: największy" }];

export default function CoursesView() {
  const openSorting = usePopover();
  const mobileOpen = useBoolean();
  const pathname = usePathname();

  const { isLoggedIn } = useUserContext();

  const { setQueryParam, getQueryParams } = useQueryParams();

  const query = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount, isLoading: isLoadingCoursesPagesCount } = useCoursesPagesCount(query);
  const { data: courses, isLoading: isLoadingCourses } = useCourses(query);

  const handleChange = useCallback(
    (name: string, value?: string | number) => {
      setQueryParam(name, value);
    },
    [setQueryParam],
  );

  const isLoading = isLoadingCourses || isLoadingCoursesPagesCount;

  useEffect(() => {
    if (openSorting.open) {
      openSorting.onClose();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pathname]);

  useEffect(() => {
    if (!isLoggedIn) {
      if (query.sort_by === "-progress") {
        handleChange("sort_by", "-students_count");
      }
    }
  }, [handleChange, isLoggedIn, query.sort_by]);

  const sortOptions = useMemo(
    () => (isLoggedIn ? [...USER_SORT_OPTIONS, ...MAIN_SORT_OPTIONS] : MAIN_SORT_OPTIONS),
    [isLoggedIn],
  );
  const defaultSort = useMemo(() => (isLoggedIn ? "-progress" : "-students_count"), [isLoggedIn]);

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
          <Typography variant="h2">Kursy</Typography>

          <Stack direction="row">
            <IconButton
              onClick={openSorting.onOpen}
              sx={{
                display: { md: "none" },
              }}
            >
              <Iconify
                icon={
                  (query.sort_by ?? defaultSort).slice(0, 1) === "-"
                    ? "carbon:sort-descending"
                    : "carbon:sort-ascending"
                }
                width={18}
              />
            </IconButton>

            <IconButton
              onClick={mobileOpen.onTrue}
              sx={{
                display: { md: "none" },
              }}
            >
              <Iconify icon="carbon:filter" width={18} />
            </IconButton>
          </Stack>
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
            <Stack
              direction="row"
              alignItems="center"
              justifyContent="right"
              sx={{ mb: 5, display: { xs: "none", md: "flex" } }}
            >
              <Sorting
                value={query.sort_by ?? defaultSort}
                options={sortOptions}
                onChange={(event: SelectChangeEvent) => handleChange("sort_by", event.target.value)}
              />
            </Stack>

            <Popover
              open={openSorting.open}
              anchorEl={openSorting.anchorEl}
              onClose={openSorting.onClose}
              anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
              transformOrigin={{ vertical: "top", horizontal: "right" }}
              slotProps={{
                paper: {
                  sx: {
                    width: 220,
                    [`& .${buttonBaseClasses.root}`]: {
                      px: 1.5,
                      py: 0.75,
                      height: "auto",
                    },
                  },
                },
              }}
            >
              <List>
                {sortOptions.map((option) => (
                  <ListItem key={option.value} disablePadding>
                    <ListItemButton
                      key={option.value}
                      selected={(query.sort_by ?? defaultSort) === option.value}
                      onClick={() => {
                        openSorting.onClose();
                        handleChange("sort_by", option.value);
                      }}
                    >
                      <ListItemText primary={option.label} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Popover>

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
