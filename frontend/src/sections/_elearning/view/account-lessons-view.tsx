"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import InputAdornment from "@mui/material/InputAdornment";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import TablePagination from "@mui/material/TablePagination";

import { useQueryParams } from "src/hooks/use-query-params";

import { usePurchase, usePurchasePageCount } from "src/api/purchase/purchase";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";

import { LessonStatus } from "src/types/purchase";
import { IQueryParamValue } from "src/types/query-params";

import AccountLessonsTableRow from "../account/account-lessons-table-row";
import AccountLessonsTableHead from "../account/account-lessons-table-head";
import FilterTeachers from "../filters/filter-teachers";
import FilterTeacher from "src/sections/review/elearning/review-filter-teacher";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie lekcje" },
  { id: LessonStatus.Nowa, label: "Nowe" },
  { id: LessonStatus.Zaplanowana, label: "Zaplanowane" },
  { id: LessonStatus.Zakończona, label: "Zakończone" },
];

const TABLE_HEAD = [
  { id: "course_title", label: "Nazwa kursu" },
  { id: "lesson_title", label: "Nazwa lekcji" },
  { id: "status", label: "Status" },
  { id: "lecturer_full_name", label: "Instruktor" },
  { id: "created_at", label: "Data zakupu" },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [1, 5, 10, 25];

// ----------------------------------------------------------------------

export default function AccountLessonsPage() {
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePurchasePageCount(filters);
  const { data: lessons } = usePurchase(filters);

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
      console.log(newValue);
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
        Lekcje
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
        <TextField
          fullWidth
          hiddenLabel
          placeholder="Nazwa kursu..."
          size="small"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Iconify icon="carbon:search" width={24} sx={{ color: "text.disabled" }} />
              </InputAdornment>
            ),
          }}
        />
        <TextField
          fullWidth
          hiddenLabel
          placeholder="Nazwa lekcji..."
          size="small"
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Iconify icon="carbon:search" width={24} sx={{ color: "text.disabled" }} />
              </InputAdornment>
            ),
          }}
        />
        <DatePicker
          label="Data zakupu"
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{ textField: { size: "small", hiddenLabel: true } }}
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
            <AccountLessonsTableHead
              order={order}
              orderBy={orderBy}
              onSort={handleSort}
              headCells={TABLE_HEAD}
            />

            {lessons && (
              <TableBody>
                {lessons.map((row) => (
                  <AccountLessonsTableRow key={row.id} row={row} />
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
