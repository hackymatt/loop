"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useLecturers } from "src/api/lecturers/lecturers";
import { useFinanceHistory, useFinanceHistoryPagesCount } from "src/api/finance/finance-history";

import Scrollbar from "src/components/scrollbar";

import FilterTeacher from "src/sections/filters/filter-teacher";

import { IQueryParamValue } from "src/types/query-params";

import FilterPrice from "../../../../filters/filter-price";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";
import AccountFinanceHistoryTableRow from "../../../../account/admin/account-finance-table-history-row";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "lecturer_uuid", label: "Wykładowca", minWidth: 200 },
  { id: "account", label: "Konto" },
  { id: "rate", label: "Stawka h" },
  { id: "commission", label: "Prowizja" },
  { id: "created_at", label: "Data zmiany", width: 150 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AdminFinanceHistoryView() {
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useFinanceHistoryPagesCount(filters);
  const { data: financeHistories } = useFinanceHistory(filters);
  const { data: teachers } = useLecturers({ sort_by: "full_name", page_size: -1 });

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "lecturer";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

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
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Historia danych finansowych
        </Typography>
      </Stack>

      <Stack direction={{ xs: "column", md: "column" }} spacing={1} sx={{ mt: 2, mb: 3 }}>
        <FilterTeacher
          value={filters?.lecturer_id ?? ""}
          options={teachers ?? []}
          onChange={(value) => handleChange("lecturer_id", value)}
        />

        <FilterSearch
          value={filters?.account ?? ""}
          onChangeSearch={(value) => handleChange("account", value)}
          placeholder="Numer konta..."
        />
        <Stack direction={{ xs: "column", md: "row" }} spacing={1}>
          <FilterPrice
            valuePriceFrom={filters?.rate_from ?? ""}
            valuePriceTo={filters?.rate_to ?? ""}
            onChangeStartPrice={(value) => handleChange("rate_from", value)}
            onChangeEndPrice={(value) => handleChange("rate_to", value)}
          />

          <FilterPrice
            valuePriceFrom={filters?.commission_from ?? ""}
            valuePriceTo={filters?.commission_to ?? ""}
            onChangeStartPrice={(value) => handleChange("commission_from", value)}
            onChangeEndPrice={(value) => handleChange("commission_to", value)}
          />

          <DatePicker
            value={filters?.created_at ? new Date(filters.created_at) : null}
            onChange={(value: Date | null) =>
              handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
            }
            sx={{ width: 1, minWidth: 180 }}
            slotProps={{
              textField: { size: "small", hiddenLabel: true, placeholder: "Data zmiany" },
            }}
          />
        </Stack>
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

            {financeHistories && (
              <TableBody>
                {financeHistories.map((row) => (
                  <AccountFinanceHistoryTableRow key={row.id} row={row} />
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
