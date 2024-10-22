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

import { useUsers } from "src/api/users/users";
import { useCouponUsage, useCouponUsagePagesCount } from "src/api/coupons/coupon-usage";

import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import FilterUser from "src/sections/filters/filter-user";
import AccountCouponUsageTableRow from "src/sections/account/admin/account-finance-table-usage-row";

import { UserType } from "src/types/user";
import { IQueryParamValue } from "src/types/query-params";

import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "user_email", label: "Email użytkownika", minWidth: 200 },
  { id: "coupon_code", label: "Kupon" },
  { id: "created_at", label: "Data wykorzystania" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AdminCouponUsageView() {
  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useCouponUsagePagesCount(filters);
  const { data: couponUsages, count: recordsCount } = useCouponUsage(filters);
  const { data: users } = useUsers({
    user_type: UserType.STUDENT[0],
    sort_by: "email",
    page_size: -1,
  });

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "-created_at";
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
          Wykorzystanie kuponów
        </Typography>
        <DownloadCSVButton queryHook={useCouponUsage} disabled={(recordsCount ?? 0) === 0} />
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 2, mb: 3 }}>
        <FilterUser
          value={filters?.user_id ?? ""}
          options={users ?? []}
          onChange={(value) => handleChange("user_id", value)}
        />

        <FilterSearch
          value={filters?.coupon_code ?? ""}
          onChangeSearch={(value) => handleChange("coupon_code", value)}
          placeholder="Kupon..."
        />

        <DatePicker
          value={filters?.created_at ? new Date(filters.created_at) : null}
          onChange={(value: Date | null) =>
            handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Data wykorzystania" },
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

            {couponUsages && (
              <TableBody>
                {couponUsages.map((row) => (
                  <AccountCouponUsageTableRow key={row.id} row={row} />
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
