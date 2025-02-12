"use client";

import { useMemo, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import TablePagination from "@mui/material/TablePagination";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";

import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { usePurchase, usePurchasePageCount } from "src/api/purchases/lessons-purchases";

import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import FilterPrice from "src/sections/filters/filter-price";
import AccountPurchasesTableRow from "src/sections/account/admin/account-lessons-purchases-table-row";

import { IPurchaseItemProp } from "src/types/purchase";
import { IQueryParamValue } from "src/types/query-params";

import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "lesson_title", label: "Nazwa lekcji", minWidth: 230 },
  { id: "price", label: "Cena" },
  { id: "created_at", label: "Data zakupu", minWidth: 150 },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountLessonsPurchaseView() {
  const { push } = useRouter();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePurchasePageCount(filters);
  const { data: lessons, count: recordsCount } = usePurchase(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "created_at";
  const order = filters?.sort_by && !filters.sort_by.startsWith("-") ? "asc" : "desc";

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

  const handleViewPayment = useCallback(
    (purchase: IPurchaseItemProp) => {
      push(`${paths.account.admin.purchases.lessons.payments}/?session_id=${purchase.paymentId}`);
    },
    [push],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Zakupy
        </Typography>
        <DownloadCSVButton queryHook={usePurchase} disabled={(recordsCount ?? 0) === 0} />
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.lesson_title ?? ""}
          onChangeSearch={(value) => handleChange("lesson_title", value)}
          placeholder="Nazwa lekcji..."
        />

        <FilterPrice
          valuePriceFrom={filters?.price_from ?? ""}
          valuePriceTo={filters?.price_to ?? ""}
          onChangeStartPrice={(value) => handleChange("price_from", value)}
          onChangeEndPrice={(value) => handleChange("price_to", value)}
        />

        <DatePicker
          value={filters?.created_at ? new Date(filters.created_at) : null}
          onChange={(value: Date | null) =>
            handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          localeText={{
            toolbarTitle: "Wybierz datę",
            cancelButtonLabel: "Anuluj",
          }}
          slotProps={{
            field: { clearable: true, onClear: () => handleChange("created_at", "") },
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
                  <AccountPurchasesTableRow
                    key={row.id}
                    row={row}
                    onViewPayment={handleViewPayment}
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
          labelDisplayedRows={() => `Strona ${page + 1} z ${pagesCount ?? 1}`}
          count={recordsCount ?? 0}
          rowsPerPage={rowsPerPage}
          onPageChange={handleChangePage}
          rowsPerPageOptions={ROWS_PER_PAGE_OPTIONS}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Box>
    </>
  );
}
