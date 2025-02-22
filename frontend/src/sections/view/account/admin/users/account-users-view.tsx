"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { LoadingButton } from "@mui/lab";
import { Tab, Tabs } from "@mui/material";
import TableBody from "@mui/material/TableBody";
import { DatePicker } from "@mui/x-date-pickers";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks/use-router";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { UserType } from "src/consts/user-type";
import { useUsers, useUsersPagesCount } from "src/api/users/users";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv/download-csv";

import FilterBoolean from "src/sections/filters/filter-boolean";
import AccountUsersTableRow from "src/sections/account/admin/account-users-table-row";

import { IUserDetailsProps } from "src/types/user";
import { IQueryParamValue } from "src/types/query-params";

import UserNewForm from "./user-new-form";
import UserEditForm from "./user-edit-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszyscy użytkownicy" },
  { id: UserType.Admin.slice(0, 1), label: "Admini" },
  { id: UserType.Teacher.slice(0, 1), label: "Wykładowcy" },
  { id: UserType.Student.slice(0, 1), label: "Studenci" },
  { id: UserType.Other.slice(0, 1), label: "Inni" },
];

const TABLE_HEAD = [
  { id: "active", label: "Aktywny" },
  { id: "email", label: "Email", minWidth: 250 },
  { id: "user_type", label: "Typ" },
  { id: "created_at", label: "Data", minWidth: 150 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountUsersView() {
  const { push } = useRouter();
  const newFormOpen = useBoolean();
  const editFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useUsersPagesCount(filters);
  const { data: users, count: recordsCount } = useUsers(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";
  const tab = filters?.user_type ? filters.user_type : "";

  const [editedUser, setEditedUser] = useState<IUserDetailsProps>();

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
      handleChange("user_type", newValue);
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

  const handleEditUser = useCallback(
    (user: IUserDetailsProps) => {
      setEditedUser(user);
      editFormOpen.onToggle();
    },
    [editFormOpen],
  );

  const handleFinanceHistoryView = useCallback(
    (user: IUserDetailsProps) => {
      push(
        `${paths.account.admin.users.financeHistory}/?lecturer_id=${user.id}&sort_by=-created_at`,
      );
    },
    [push],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Spis użytkowników
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={useUsers} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newFormOpen.onToggle}
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

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterBoolean
          leftLabel="Nieaktywny"
          rightLabel="Aktywny"
          value={(filters?.active ?? "true") === "true"}
          onChange={(value: boolean) => handleChange("active", value.toString())}
        />

        <FilterSearch
          value={filters?.email ?? ""}
          onChangeSearch={(value) => handleChange("email", value)}
          placeholder="Email..."
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
            textField: { size: "small", hiddenLabel: true, placeholder: "Data" },
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

            {users && (
              <TableBody>
                {users.map((row) => (
                  <AccountUsersTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditUser}
                    onFinanceHistoryView={handleFinanceHistoryView}
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

      <UserNewForm open={newFormOpen.value} onClose={newFormOpen.onFalse} />

      {editedUser && (
        <UserEditForm
          user={editedUser}
          open={editFormOpen.value}
          onClose={() => {
            setEditedUser(undefined);
            editFormOpen.onFalse();
          }}
        />
      )}
    </>
  );
}
