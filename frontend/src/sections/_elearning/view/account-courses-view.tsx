"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import TablePagination from "@mui/material/TablePagination";

import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useLecturers } from "src/api/lecturers/lecturers";
import { usePurchase, usePurchasePageCount } from "src/api/purchase/purchase";

import Scrollbar from "src/components/scrollbar";

import { LessonStatus } from "src/types/purchase";
import { IQueryParamValue } from "src/types/query-params";

import FilterSearch from "../filters/filter-search";
import FilterTeacher from "../filters/filter-teacher";
import AccountTableHead from "../account/account-table-head";
import AccountLessonsTableRow from "../account/student/account-lessons-table-row";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie kursy" },
  { id: LessonStatus.nowa, label: "Aktywne" },
  { id: LessonStatus.zaplanowana, label: "Nieaktywne" },
];

const TABLE_HEAD = [
  { id: "course_title", label: "Nazwa kursu" },
  { id: "lesson_title", label: "Nazwa lekcji" },
  { id: "lesson_status", label: "Status" },
  { id: "lecturer_uuid", label: "Instruktor" },
  { id: "created_at", label: "Data zakupu" },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25];

// ----------------------------------------------------------------------

export default function AccountCoursesView() {
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePurchasePageCount(filters);
  const { data: lessons } = usePurchase(filters);

  const { data: teachers } = useLecturers({ sort_by: "full_name", page_size: 1000 });

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "created_at";
  const order = filters?.sort_by && !filters.sort_by.startsWith("-") ? "asc" : "desc";
  const tab = filters?.lesson_status ? filters.lesson_status : "";

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
      handleChange("lesson_status", newValue);
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

  return (
    <>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Kursy
      </Typography>

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
          value={filters?.course_title ?? ""}
          onChangeSearch={(value) => handleChange("course_title", value)}
          placeholder="Nazwa kursu..."
        />

        <FilterSearch
          value={filters?.lesson_title ?? ""}
          onChangeSearch={(value) => handleChange("lesson_title", value)}
          placeholder="Nazwa lekcji..."
        />

        {teachers && (
          <FilterTeacher
            value={filters?.lecturer_id ?? ""}
            options={teachers}
            onChange={(value) => handleChange("lecturer_id", value)}
          />
        )}

        <DatePicker
          value={filters?.created_at ? new Date(filters.created_at) : null}
          onChange={(value: Date | null) =>
            handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Data zakupu" },
          }}
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
                    onAdd={() => {}}
                    onDelete={() => {}}
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
