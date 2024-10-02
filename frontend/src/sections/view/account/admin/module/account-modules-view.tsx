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
import TablePagination from "@mui/material/TablePagination";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { useModules, useModulesPagesCount } from "src/api/modules/modules";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import AccountModulesTableRow from "src/sections/account/admin/account-modules-table-row";

import { ICourseModuleProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

import ModuleNewForm from "./module-new-form";
import ModuleEditForm from "./module-edit-form";
import ModuleDeleteForm from "./module-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "title", label: "Nazwa modułu", minWidth: 500 },
  { id: "lessons_count", label: "Liczba lekcji" },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountModulesView() {
  const newModuleFormOpen = useBoolean();
  const editModuleFormOpen = useBoolean();
  const deleteModuleFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useModulesPagesCount(filters);
  const { data: modules, count: recordsCount } = useModules(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

  const [editedModule, setEditedModule] = useState<ICourseModuleProp>();
  const [deletedModule, setDeletedModule] = useState<ICourseModuleProp>();

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

  const handleEditModule = useCallback(
    (module: ICourseModuleProp) => {
      setEditedModule(module);
      editModuleFormOpen.onToggle();
    },
    [editModuleFormOpen],
  );

  const handleDeleteModule = useCallback(
    (module: ICourseModuleProp) => {
      setDeletedModule(module);
      deleteModuleFormOpen.onToggle();
    },
    [deleteModuleFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Spis modułów
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={useModules} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newModuleFormOpen.onToggle}
          >
            <Iconify icon="carbon:add" />
          </LoadingButton>
        </Stack>
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.title ?? ""}
          onChangeSearch={(value) => handleChange("title", value)}
          placeholder="Nazwa modułu..."
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

            {modules && (
              <TableBody>
                {modules.map((row) => (
                  <AccountModulesTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditModule}
                    onDelete={handleDeleteModule}
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

      <ModuleNewForm open={newModuleFormOpen.value} onClose={newModuleFormOpen.onFalse} />
      {editedModule && (
        <ModuleEditForm
          module={editedModule}
          open={editModuleFormOpen.value}
          onClose={editModuleFormOpen.onFalse}
        />
      )}
      {deletedModule && (
        <ModuleDeleteForm
          module={deletedModule}
          open={deleteModuleFormOpen.value}
          onClose={deleteModuleFormOpen.onFalse}
        />
      )}
    </>
  );
}
