"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
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

import { useUsers, useUsersPagesCount } from "src/api/users/users";

import Scrollbar from "src/components/scrollbar";

import AccountUsersTableRow from "src/sections/_elearning/account/admin/account-users-table-row";

import { IQueryParamValue } from "src/types/query-params";
import { UserType, IUserDetailsProps } from "src/types/user";

import UserEditForm from "./user-edit-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszyscy użytkownicy" },
  { id: UserType.Admin.slice(0, 1), label: "Admini" },
  { id: UserType.Wykładowca.slice(0, 1), label: "Wykładowcy" },
  { id: UserType.Student.slice(0, 1), label: "Studenci" },
];

const TABLE_HEAD = [
  { id: "first_name", label: "Imię" },
  { id: "last_name", label: "Nazwisko" },
  { id: "email", label: "Email", minWidth: 200 },
  { id: "gender", label: "Płeć", maxWidth: 100 },
  { id: "user_type", label: "Typ" },
  { id: "created_at", label: "Data", minWidth: 110 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountUsersView() {
  const router = useRouter();
  const editFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useUsersPagesCount(filters);
  const { data: users } = useUsers(filters);

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
      router.push(
        `${paths.account.admin.users.financeHistory}/?lecturer_id=${user.uuid}&sort_by=-created_at`,
      );
    },
    [router],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Spis użytkowników
        </Typography>
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
          value={filters?.first_name ?? ""}
          onChangeSearch={(value) => handleChange("first_name", value)}
          placeholder="Imię..."
        />

        <FilterSearch
          value={filters?.last_name ?? ""}
          onChangeSearch={(value) => handleChange("last_name", value)}
          placeholder="Nazwisko..."
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
          slotProps={{
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
          labelDisplayedRows={({ from, to, count }) => `Strona ${from} z ${count}`}
          count={pagesCount ?? 0}
          rowsPerPage={rowsPerPage}
          onPageChange={handleChangePage}
          rowsPerPageOptions={ROWS_PER_PAGE_OPTIONS}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Box>

      {editedUser && (
        <UserEditForm user={editedUser} open={editFormOpen.value} onClose={editFormOpen.onFalse} />
      )}
    </>
  );
}
