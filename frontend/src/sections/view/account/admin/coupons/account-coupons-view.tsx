"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { Tab, Tabs } from "@mui/material";
import TableBody from "@mui/material/TableBody";
import { DatePicker } from "@mui/x-date-pickers";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks/use-router";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useCoupons, useCouponsPagesCount } from "src/api/coupons/coupons";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import FilterValue from "src/sections/filters/filter-value";
import AccountCouponsTableRow from "src/sections/account/admin/account-coupons-table-row";

import { ICouponProps } from "src/types/coupon";
import { IQueryParamValue } from "src/types/query-params";

import CouponNewForm from "./coupon-new-form";
import CouponEditForm from "./coupon-edit-form";
import CouponDeleteForm from "./coupon-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie kupony" },
  { id: "true", label: "Aktywne" },
  { id: "false", label: "Nieaktywne" },
];

const TABLE_HEAD = [
  { id: "code", label: "Kupon", minWidth: 200 },
  { id: "discount", label: "Zniżka", maxWidth: 100 },
  { id: "active", label: "Status" },
  { id: "expiration_date", label: "Data ważności", minWidth: 150 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountCouponsView() {
  const { push } = useRouter();

  const newCouponFormOpen = useBoolean();
  const editCouponFormOpen = useBoolean();
  const deleteCouponFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useCouponsPagesCount(filters);
  const { data: coupons, count: recordsCount } = useCoupons(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "-expiration_date";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";
  const tab = filters?.active ? filters.active : "";

  const [editedCoupon, setEditedCoupon] = useState<ICouponProps>();
  const [deletedCoupon, setDeletedCoupon] = useState<ICouponProps>();

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

  const handleEdit = useCallback(
    (coupon: ICouponProps) => {
      setEditedCoupon(coupon);
      editCouponFormOpen.onToggle();
    },
    [editCouponFormOpen],
  );

  const handleDelete = useCallback(
    (coupon: ICouponProps) => {
      setDeletedCoupon(coupon);
      deleteCouponFormOpen.onToggle();
    },
    [deleteCouponFormOpen],
  );

  const handleViewUsage = useCallback(
    (coupon: ICouponProps) => {
      push(`${paths.account.admin.coupons.usage}/?coupon_code=${coupon.code}&sort_by=-created_at`);
    },
    [push],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Spis kuponów
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={useCoupons} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newCouponFormOpen.onToggle}
          >
            <Iconify icon="carbon:add" />
          </LoadingButton>
        </Stack>
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

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.code ?? ""}
          onChangeSearch={(value) => handleChange("code", value)}
          placeholder="Kupon..."
        />

        <FilterValue
          valueFrom={filters?.discount_from ?? ""}
          valueTo={filters?.discount_to ?? ""}
          onChangeStart={(value) => handleChange("discount_from", value)}
          onChangeEnd={(value) => handleChange("discount_to", value)}
        />

        <DatePicker
          value={filters?.expiration_date_to ? new Date(filters.expiration_date_to) : null}
          onChange={(value: Date | null) =>
            handleChange("expiration_date_to", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Ważny do" },
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

            {coupons && (
              <TableBody>
                {coupons.map((row) => (
                  <AccountCouponsTableRow
                    key={row.id}
                    row={row}
                    onViewUsage={handleViewUsage}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
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

      <CouponNewForm open={newCouponFormOpen.value} onClose={newCouponFormOpen.onFalse} />

      {editedCoupon && (
        <CouponEditForm
          coupon={editedCoupon}
          open={editCouponFormOpen.value}
          onClose={editCouponFormOpen.onFalse}
        />
      )}

      {deletedCoupon && (
        <CouponDeleteForm
          coupon={deletedCoupon}
          open={deleteCouponFormOpen.value}
          onClose={deleteCouponFormOpen.onFalse}
        />
      )}
    </>
  );
}
