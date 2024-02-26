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

import { useTechnologies, useTechnologiesPagesCount } from "src/api/technologies/technologies";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";

import AccountTechnologiesTableRow from "src/sections/_elearning/account/admin/account-technologies-table-row";

import { IQueryParamValue } from "src/types/query-params";
import { ICourseByCategoryProps } from "src/types/course";

import TechnologyNewForm from "./technology-new-form";
import TechnologyEditForm from "./technology-edit-form";
import TechnologyDeleteForm from "./technology-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "name", label: "Nazwa technologii", minWidth: 200 },
  { id: "created_at", label: "Data utworzenia", width: 200 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25];

// ----------------------------------------------------------------------

export default function AccountTechnologiesView() {
  const newTechnologyFormOpen = useBoolean();
  const editTechnologyFormOpen = useBoolean();
  const deleteTechnologyFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useTechnologiesPagesCount(filters);
  const { data: technologies } = useTechnologies(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

  const [editedTechnology, setEditedTechnology] = useState<ICourseByCategoryProps>();
  const [deletedTechnology, setDeletedTechnology] = useState<ICourseByCategoryProps>();

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

  const handleEditTechnology = useCallback(
    (technology: ICourseByCategoryProps) => {
      setEditedTechnology(technology);
      editTechnologyFormOpen.onToggle();
    },
    [editTechnologyFormOpen],
  );

  const handleDeleteTechnology = useCallback(
    (technology: ICourseByCategoryProps) => {
      setDeletedTechnology(technology);
      deleteTechnologyFormOpen.onToggle();
    },
    [deleteTechnologyFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Technologie
        </Typography>
        <LoadingButton
          component="label"
          variant="contained"
          size="small"
          color="success"
          loading={false}
          onClick={newTechnologyFormOpen.onToggle}
        >
          <Iconify icon="carbon:add" />
        </LoadingButton>
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

            {technologies && (
              <TableBody>
                {technologies.map((row) => (
                  <AccountTechnologiesTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditTechnology}
                    onDelete={handleDeleteTechnology}
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

      <TechnologyNewForm
        open={newTechnologyFormOpen.value}
        onClose={newTechnologyFormOpen.onFalse}
      />
      {editedTechnology && (
        <TechnologyEditForm
          technology={editedTechnology}
          open={editTechnologyFormOpen.value}
          onClose={editTechnologyFormOpen.onFalse}
        />
      )}
      {deletedTechnology && (
        <TechnologyDeleteForm
          technology={deletedTechnology}
          open={deleteTechnologyFormOpen.value}
          onClose={deleteTechnologyFormOpen.onFalse}
        />
      )}
    </>
  );
}
