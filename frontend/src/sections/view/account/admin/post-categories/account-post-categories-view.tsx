"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
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

import {
  usePostCategories,
  usePostCategoriesPagesCount,
} from "src/api/post-categories/post-categories";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import AccountCategoriesTableRow from "src/sections/account/admin/account-post-categories-table-row";

import { IPostCategoryProps } from "src/types/blog";
import { IQueryParamValue } from "src/types/query-params";

import CategoryNewForm from "./category-new-form";
import CategoryEditForm from "./category-edit-form";
import CategoryDeleteForm from "./category-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "name", label: "Nazwa kategorii", minWidth: 200 },
  { id: "created_at", label: "Data utworzenia", width: 200 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountPostCategoriesView() {
  const newCategoryFormOpen = useBoolean();
  const editCategoryFormOpen = useBoolean();
  const deleteCategoryFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePostCategoriesPagesCount(filters);
  const { data: categories, count: recordsCount } = usePostCategories(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

  const [editedCategory, setEditedCategory] = useState<IPostCategoryProps>();
  const [deletedCategory, setDeletedCategory] = useState<IPostCategoryProps>();

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

  const handleEditCategory = useCallback(
    (category: IPostCategoryProps) => {
      setEditedCategory(category);
      editCategoryFormOpen.onToggle();
    },
    [editCategoryFormOpen],
  );

  const handleDeleteCategory = useCallback(
    (category: IPostCategoryProps) => {
      setDeletedCategory(category);
      deleteCategoryFormOpen.onToggle();
    },
    [deleteCategoryFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Kategorie
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={usePostCategories} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newCategoryFormOpen.onToggle}
          >
            <Iconify icon="carbon:add" />
          </LoadingButton>
        </Stack>
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.name ?? ""}
          onChangeSearch={(value) => handleChange("name", value)}
          placeholder="Nazwa technologii..."
        />

        <DatePicker
          value={filters?.created_at ? new Date(filters.created_at) : null}
          onChange={(value: Date | null) =>
            handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
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

            {categories && (
              <TableBody>
                {categories.map((row) => (
                  <AccountCategoriesTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditCategory}
                    onDelete={handleDeleteCategory}
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

      <CategoryNewForm open={newCategoryFormOpen.value} onClose={newCategoryFormOpen.onFalse} />
      {editedCategory && (
        <CategoryEditForm
          category={editedCategory}
          open={editCategoryFormOpen.value}
          onClose={editCategoryFormOpen.onFalse}
        />
      )}
      {deletedCategory && (
        <CategoryDeleteForm
          category={deletedCategory}
          open={deleteCategoryFormOpen.value}
          onClose={deleteCategoryFormOpen.onFalse}
        />
      )}
    </>
  );
}
