"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { LoadingButton } from "@mui/lab";
import { Tab, Tabs } from "@mui/material";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";

import { useQueryParams } from "src/hooks/use-query-params";

import { useLessons, useLessonsPagesCount } from "src/api/lessons/lessons";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";

import { ICourseLessonProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

import FilterPrice from "../../../filters/filter-price";
import FilterSearch from "../../../filters/filter-search";
import FilterDuration from "../../../filters/filter-duration";
import AccountTableHead from "../../../account/account-table-head";
import AccountLessonsTableRow from "../../../account/admin/account-lessons-table-row";

// ----------------------------------------------------------------------

const DURATION_OPTIONS = [
  { value: "(duration_to=30)", label: "0 - 30 minut" },
  { value: "(duration_from=30)&(duration_to=60)", label: "30 - 60 minut" },
  { value: "(duration_from=60)&(duration_to=90)", label: "60 - 90 minut" },
  { value: "(duration_from=90)&(duration_to=120)", label: "90 - 120 minut" },
  { value: "(duration_from=120)", label: "120+ minut" },
];

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie lekcje" },
  { id: "True", label: "Aktywne" },
  { id: "False", label: "Nieaktywne" },
];

const TABLE_HEAD = [
  { id: "title", label: "Nazwa lekcji", minWidth: 200 },
  { id: "duration", label: "Czas", width: 100 },
  { id: "active", label: "Status", width: 100 },
  { id: "price", label: "Cena", width: 50 },
  { id: "github_url", label: "Repozytorium", width: 100 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25];

// ----------------------------------------------------------------------

export default function AccountLessonsView() {
  const router = useRouter();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  if (Object.keys(filters).length === 0) {
    setQueryParam("sort_by", "title");
  }

  const { data: pagesCount } = useLessonsPagesCount(filters);
  const { data: lessons } = useLessons(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";
  const tab = filters?.active ? filters.active : "";

  const handleChange = useCallback(
    (name: string, value: IQueryParamValue) => {
      if (value) {
        setQueryParam(name, value);
      } else {
        removeQueryParam(name);
      }
    },
    [removeQueryParam, setQueryParam],
  );

  const handleChangeTab = useCallback(
    (event: React.SyntheticEvent, newValue: string) => {
      handleChange("active", newValue);
    },
    [handleChange],
  );

  const handleSort = useCallback(
    (id: string) => {
      const isAsc = orderBy === id && order === "asc";
      handleChange("sort_by", isAsc ? `-${id}` : id);
    },
    [handleChange, order, orderBy],
  );

  const handleChangePage = useCallback(
    (event: unknown, newPage: number) => {
      handleChange("page", newPage + 1);
    },
    [handleChange],
  );

  const handleChangeRowsPerPage = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      handleChange("page_size", parseInt(event.target.value, 10));
      handleChange("page", 1);
    },
    [handleChange],
  );

  const handlePriceHistoryView = useCallback(
    (lesson: ICourseLessonProp) => {
      router.push(`${paths.account.admin.lessonsPriceHistory}/?lesson_name=${lesson.title}`);
    },
    [router],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Lekcje
        </Typography>
        <LoadingButton
          component="label"
          variant="contained"
          size="small"
          color="success"
          loading={false}
          onClick={() => {}}
        >
          <Iconify icon="carbon:add" />
        </LoadingButton>
      </Stack>

      <Tabs
        value={TABS.find((t) => t.id === tab)?.id ?? ""}
        scrollButtons="auto"
        variant="scrollable"
        allowScrollButtonsMobile
        onChange={handleChangeTab}
      >
        {TABS.map((category) => (
          <Tab key={category.id} value={category.id} label={category.label} />
        ))}
      </Tabs>

      <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.title ?? ""}
          onChangeSearch={(value) => handleChange("title", value)}
          placeholder="Nazwa lekcji..."
        />

        <FilterDuration
          value={filters?.filters ?? ""}
          options={DURATION_OPTIONS}
          onChangeDuration={(value) => handleChange("filters", value)}
        />

        <FilterPrice
          valuePriceFrom={filters?.price_from ?? ""}
          valuePriceTo={filters?.price_to ?? ""}
          onChangeStartPrice={(value) => handleChange("price_from", value)}
          onChangeEndPrice={(value) => handleChange("price_to", value)}
        />

        <FilterSearch
          value={filters?.github_url ?? ""}
          onChangeSearch={(value) => handleChange("github_url", value)}
          placeholder="Repozytorium..."
        />
      </Stack>

      <TableContainer
        sx={{
          overflow: "unset",
          [`& .${tableCellClasses.head}`]: {
            color: "text.primary",
          },
          [`& .${tableCellClasses.root}`]: {
            bgcolor: "background.default",
            borderBottomColor: (theme) => theme.palette.divider,
          },
        }}
      >
        <Scrollbar>
          <Table
            sx={{
              minWidth: 720,
            }}
            size="small"
          >
            <AccountTableHead
              order={order}
              orderBy={orderBy}
              onSort={handleSort}
              headCells={TABLE_HEAD}
            />

            {lessons && (
              <TableBody>
                {lessons.map((row) => (
                  <AccountLessonsTableRow
                    key={row.id}
                    row={row}
                    onEdit={() => {}}
                    onPriceHistoryView={handlePriceHistoryView}
                  />
                ))}
              </TableBody>
            )}
          </Table>
        </Scrollbar>
      </TableContainer>

      <Box sx={{ position: "relative" }}>
        <TablePagination
          page={page}
          component="div"
          labelRowsPerPage="Wierszy na stronę"
          labelDisplayedRows={({ from, to, count }) => `Strona ${from} z ${count}`}
          count={pagesCount ?? 0}
          rowsPerPage={rowsPerPage}
          onPageChange={handleChangePage}
          rowsPerPageOptions={ROWS_PER_PAGE_OPTIONS}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Box>
    </>
  );
}
