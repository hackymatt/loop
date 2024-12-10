"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { LoadingButton } from "@mui/lab";
import { Tab, Tabs } from "@mui/material";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { usePosts, usePostsPagesCount } from "src/api/posts/posts";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import AccountPostsTableRow from "src/sections/account/admin/account-posts-table-row";

import { IPostProps } from "src/types/blog";
import { IQueryParamValue } from "src/types/query-params";

import PostNewForm from "./post-new-form";
import PostEditForm from "./post-edit-form";
import PostDeleteForm from "./post-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";
// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie artykuły" },
  { id: "True", label: "Aktywne" },
  { id: "False", label: "Nieaktywne" },
];

const TABLE_HEAD = [
  { id: "title", label: "Nazwa artykułu", minWidth: 200 },
  { id: "active", label: "Status", width: 100 },
  { id: "created_at", label: "Data utworzenia", width: 200 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountPostsView() {
  const newPostFormOpen = useBoolean();
  const editPostFormOpen = useBoolean();
  const deletePostFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePostsPagesCount(filters);
  const { data: posts, count: recordsCount } = usePosts(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";
  const tab = filters?.active ? filters.active : "";

  const [editedPost, setEditedPost] = useState<IPostProps>();
  const [deletedPost, setDeletedPost] = useState<IPostProps>();

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

  const handleEditPost = useCallback(
    (post: IPostProps) => {
      setEditedPost(post);
      editPostFormOpen.onToggle();
    },
    [editPostFormOpen],
  );

  const handleDeletePost = useCallback(
    (post: IPostProps) => {
      setDeletedPost(post);
      deletePostFormOpen.onToggle();
    },
    [deletePostFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Spis artykułów
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={usePosts} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newPostFormOpen.onToggle}
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
        <FilterSearch
          value={filters?.title ?? ""}
          onChangeSearch={(value) => handleChange("title", value)}
          placeholder="Nazwa artykułu..."
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
            textField: { size: "small", hiddenLabel: true, placeholder: "Data utworzenia" },
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

            {posts && (
              <TableBody>
                {posts.map((row) => (
                  <AccountPostsTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditPost}
                    onDelete={handleDeletePost}
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

      <PostNewForm open={newPostFormOpen.value} onClose={newPostFormOpen.onFalse} />
      {editedPost && (
        <PostEditForm
          post={editedPost}
          open={editPostFormOpen.value}
          onClose={editPostFormOpen.onFalse}
        />
      )}
      {deletedPost && (
        <PostDeleteForm
          post={deletedPost}
          open={deletePostFormOpen.value}
          onClose={deletePostFormOpen.onFalse}
        />
      )}
    </>
  );
}
