"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { LoadingButton } from "@mui/lab";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import TablePagination from "@mui/material/TablePagination";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { usePayments, usePaymentsPageCount } from "src/api/purchases/admin/services/payments";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import FilterPrice from "src/sections/filters/filter-price";
import AccountServicesPaymentsTableRow from "src/sections/account/admin/account-services-payments-table-row";

import { IQueryParamValue } from "src/types/query-params";
import { IPaymentProp, PaymentStatus } from "src/types/payment";

import PaymentNewForm from "./payment-new-form";
import PaymentEditForm from "./payment-edit-form";
import PaymentDeleteForm from "./payment-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie statusy" },
  { id: PaymentStatus.PENDING.slice(0, 1), label: "Oczekujące" },
  { id: PaymentStatus.SUCCESS.slice(0, 1), label: "Zapłacone" },
  { id: PaymentStatus.FAILURE.slice(0, 1), label: "Niezapłacone" },
];

const TABLE_HEAD = [
  { id: "session_id", label: "Id", minWidth: 230 },
  { id: "amount", label: "Kwota" },
  { id: "status", label: "Status", minWidth: 150 },
  { id: "created_at", label: "Data płatności", minWidth: 150 },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountServicePaymentView() {
  const newPaymentFormOpen = useBoolean();
  const editPaymentFormOpen = useBoolean();
  const deletePaymentFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePaymentsPageCount(filters);
  const { data: lessons, count: recordsCount } = usePayments(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "created_at";
  const order = filters?.sort_by && !filters.sort_by.startsWith("-") ? "asc" : "desc";
  const tab = filters?.status ? filters.status : "";

  const [editedPayment, setEditedPayment] = useState<IPaymentProp>();
  const [deletedPayment, setDeletedPayment] = useState<IPaymentProp>();

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
      handleChange("status", newValue);
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

  const handleEditPayment = useCallback(
    (payment: IPaymentProp) => {
      setEditedPayment(payment);
      editPaymentFormOpen.onToggle();
    },
    [editPaymentFormOpen],
  );

  const handleDeletePayment = useCallback(
    (payment: IPaymentProp) => {
      setDeletedPayment(payment);
      deletePaymentFormOpen.onToggle();
    },
    [deletePaymentFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Płatności
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={usePayments} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newPaymentFormOpen.onToggle}
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
        {TABS.map((t) => (
          <Tab key={t.id} value={t.id} label={t.label} />
        ))}
      </Tabs>

      <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.session_id ?? ""}
          onChangeSearch={(value) => handleChange("session_id", value)}
          placeholder="Id..."
        />

        <FilterPrice
          valuePriceFrom={filters?.amount_from ?? ""}
          valuePriceTo={filters?.amount_to ?? ""}
          onChangeStartPrice={(value) => handleChange("amount_from", value)}
          onChangeEndPrice={(value) => handleChange("amount_to", value)}
          currency=""
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
            textField: { size: "small", hiddenLabel: true, placeholder: "Data płatności" },
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
                  <AccountServicesPaymentsTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditPayment}
                    onDelete={handleDeletePayment}
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

      <PaymentNewForm open={newPaymentFormOpen.value} onClose={newPaymentFormOpen.onFalse} />
      {editedPayment && (
        <PaymentEditForm
          payment={editedPayment}
          open={editPaymentFormOpen.value}
          onClose={editPaymentFormOpen.onFalse}
        />
      )}
      {deletedPayment && (
        <PaymentDeleteForm
          payment={deletedPayment}
          open={deletePaymentFormOpen.value}
          onClose={deletePaymentFormOpen.onFalse}
        />
      )}
    </>
  );
}
