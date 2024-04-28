"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import { DatePicker } from "@mui/x-date-pickers";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useLecturers } from "src/api/lecturers/lecturers";
import { useEarnings, useEarningsPagesCount } from "src/api/earnings/earnings";

import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import FilterTeacher from "src/sections/filters/filter-teacher";
import AccountTableHead from "src/sections/account/account-table-head";
import AccountEarningsTeachersTableRow from "src/sections/account/admin/account-earnings-table-teachers-row";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "year", label: "Rok" },
  { id: "month", label: "Miesiąc" },
  { id: "cost", label: "Wykładowca" },
  { id: "cost", label: "Nr konta", minWidth: 200 },
  { id: "balance", label: "Zarobki" },
];

const ROWS_PER_PAGE_OPTIONS = [3, 6, 12, 24, 36, 60];

// ----------------------------------------------------------------------

export default function AccountEarningsTeachersView() {
  const { data: teachers } = useLecturers({ sort_by: "full_name", page_size: -1 });

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useEarningsPagesCount(filters);
  const { data: earnings, count: recordsCount } = useEarnings(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 12;

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
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Zarobki instruktorów
        </Typography>
        <DownloadCSVButton queryHook={useEarnings} disabled={(recordsCount ?? 0) === 0} />
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 2, mb: 3 }}>
        <DatePicker
          value={filters?.year ? new Date(`${filters.year}-01-01`) : null}
          onChange={(value: Date | null) => handleChange("year", value ? fDate(value, "yyyy") : "")}
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Rok" },
          }}
          views={["year"]}
          openTo="year"
        />

        <DatePicker
          value={filters?.month ? new Date(`2000-${filters.month}-01`) : null}
          onChange={(value: Date | null) => handleChange("month", value ? fDate(value, "M") : "")}
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Miesiąc" },
          }}
          views={["month"]}
          openTo="month"
        />

        <FilterTeacher
          value={filters?.lecturer ?? ""}
          options={teachers ?? []}
          onChange={(value) => handleChange("lecturer", value)}
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
            <AccountTableHead headCells={TABLE_HEAD} />

            {earnings && (
              <TableBody>
                {earnings.map((row) => (
                  <AccountEarningsTeachersTableRow key={`${row.year}${row.month}`} row={row} />
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
          labelRowsPerPage="Ilość miesięcy"
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
