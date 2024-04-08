"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import { useTheme } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import { LineChart } from "@mui/x-charts/LineChart";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import { useEarnings, useEarningsPagesCount } from "src/api/earnings/earnings";

import Scrollbar from "src/components/scrollbar";

import AccountTableHead from "src/sections/_elearning/account/account-table-head";
import AccountEarningsTableRow from "src/sections/_elearning/account/teacher/account-earnings-table-row";

import { IEarningProp } from "src/types/finance";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "year", label: "Rok" },
  { id: "month", label: "Miesiąc" },
  { id: "earnings", label: "Zarobki" },
];

const ROWS_PER_PAGE_OPTIONS = [3, 6, 12, 24, 36, 60, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountEarningsView() {
  const { palette } = useTheme();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useEarningsPagesCount(filters);
  const { data: earnings } = useEarnings(filters);

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

  const monthYear = useMemo(
    () =>
      earnings
        ? earnings
            .map(
              (earning: IEarningProp) =>
                `${fDate(new Date(2000, earning.month, 1), "LLL")} ${earning.year}`,
            )
            .reverse()
        : [],
    [earnings],
  );

  const forecastEarnings = useMemo(
    () => (earnings ? earnings.filter((earning: IEarningProp) => !earning.actual) : []),
    [earnings],
  );

  const actualEarnings = useMemo(
    () => (earnings ? earnings.filter((earning: IEarningProp) => earning.actual) : []),
    [earnings],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Zarobki
        </Typography>
      </Stack>

      <Stack direction="row" display="flex" justifyContent="center">
        <LineChart
          xAxis={[
            {
              data: monthYear,
              scaleType: "band",
              dataKey: "month",
            },
          ]}
          yAxis={[
            {
              valueFormatter: (value) => fCurrency(value),
            },
          ]}
          series={[
            {
              data: [
                ...actualEarnings.map((earning: IEarningProp) => earning.earnings ?? 0).reverse(),
                ...Array(forecastEarnings.length).fill(null),
              ],
              color: palette.success.main,
              valueFormatter: (value) => (value === null ? "0,00 zł" : fCurrency(value)),
              label: "wartość rzeczywista",
            },
            {
              data: [
                ...Array(actualEarnings.length).fill(null),
                ...forecastEarnings.map((earning: IEarningProp) => earning.earnings ?? 0).reverse(),
              ],
              color: palette.success.light,
              valueFormatter: (value) => (value === null ? "0,00 zł" : fCurrency(value)),
              label: "wartość szacunkowa",
            },
          ]}
          width={500}
          height={300}
          slotProps={{
            legend: {
              itemMarkWidth: 20,
              itemMarkHeight: 2,
              markGap: 5,
              itemGap: 10,
              labelStyle: { fontSize: 12 },
            },
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
            <AccountTableHead headCells={TABLE_HEAD} />

            {earnings && (
              <TableBody>
                {earnings.map((row) => (
                  <AccountEarningsTableRow key={`${row.year}${row.month}`} row={row} />
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
