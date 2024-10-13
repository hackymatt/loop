"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import { Tab, Tabs } from "@mui/material";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import TablePagination from "@mui/material/TablePagination";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { useTeachings, useTeachingsPagesCount } from "src/api/teaching/teachings";

import Scrollbar from "src/components/scrollbar";

import FilterPrice from "src/sections/filters/filter-price";
import FilterSearch from "src/sections/filters/filter-search";
import FilterDuration from "src/sections/filters/filter-duration";
import AccountTableHead from "src/sections/account/account-table-head";
import AccountTeachingsTableRow from "src/sections/account/teacher/account-teachings-table-row";

import { ITeachingProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

import TeachingAddForm from "./teaching-add-form";
import TeachingViewForm from "./teaching-view-form";
import TeachingDeleteForm from "./teaching-delete-form";

// ----------------------------------------------------------------------

const DURATION_OPTIONS = [
  { value: "(duration_to=30)", label: "0 - 30 minut" },
  { value: "(duration_from=30)&(duration_to=60)", label: "30 - 60 minut" },
  { value: "(duration_from=60)&(duration_to=90)", label: "60 - 90 minut" },
  { value: "(duration_from=90)&(duration_to=120)", label: "90 - 120 minut" },
  { value: "(duration_from=120)", label: "120+ minut" },
];

// ----------------------------------------------------------------------

const TABS = [
  { id: "", label: "Wszystkie lekcje" },
  { id: "True", label: "Prowadzone" },
  { id: "False", label: "Nieprowadzone" },
];

const TABLE_HEAD = [
  { id: "title", label: "Nazwa lekcji", minWidth: 200 },
  { id: "duration", label: "Czas", width: 100 },
  { id: "active", label: "Status", width: 100 },
  { id: "teaching", label: "Nauczanie", width: 100 },
  { id: "price", label: "Cena", width: 50 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountTeachingView() {
  const viewTeachingFormOpen = useBoolean();
  const addTeachingFormOpen = useBoolean();
  const deleteTeachingFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useTeachingsPagesCount(filters);
  const { data: teachings, count: recordsCount } = useTeachings(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";
  const tab = filters?.teaching ? filters.teaching : "";

  const [viewedTeaching, setViewedTeaching] = useState<ITeachingProp>();
  const [addedTeaching, setAddedTeaching] = useState<ITeachingProp>();
  const [deletedTeaching, setDeletedTeaching] = useState<ITeachingProp>();

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
      handleChange("teaching", newValue);
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

  const handleViewTeaching = useCallback(
    (teaching: ITeachingProp) => {
      setViewedTeaching(teaching);
      viewTeachingFormOpen.onToggle();
    },
    [viewTeachingFormOpen],
  );

  const handleAddTeaching = useCallback(
    (teaching: ITeachingProp) => {
      setAddedTeaching(teaching);
      addTeachingFormOpen.onToggle();
    },
    [addTeachingFormOpen],
  );

  const handleDeleteTeaching = useCallback(
    (teaching: ITeachingProp) => {
      setDeletedTeaching(teaching);
      deleteTeachingFormOpen.onToggle();
    },
    [deleteTeachingFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Nauczanie
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
          value={filters?.title ?? ""}
          onChangeSearch={(value) => handleChange("title", value)}
          placeholder="Nazwa lekcji..."
        />

        <FilterDuration
          value={filters?.filters ?? ""}
          options={DURATION_OPTIONS}
          onChangeDuration={(value) => handleChange("filters", value)}
        />

        <FilterPrice
          valuePriceFrom={filters?.price_from ?? ""}
          valuePriceTo={filters?.price_to ?? ""}
          onChangeStartPrice={(value) => handleChange("price_from", value)}
          onChangeEndPrice={(value) => handleChange("price_to", value)}
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

            {teachings && (
              <TableBody>
                {teachings.map((row) => (
                  <AccountTeachingsTableRow
                    key={row.id}
                    row={row}
                    onView={handleViewTeaching}
                    onAdd={handleAddTeaching}
                    onDelete={handleDeleteTeaching}
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
          labelDisplayedRows={() => `Strona ${page + 1} z ${pagesCount ?? 0}`}
          count={recordsCount ?? 0}
          rowsPerPage={rowsPerPage}
          onPageChange={handleChangePage}
          rowsPerPageOptions={ROWS_PER_PAGE_OPTIONS}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Box>

      {viewedTeaching && (
        <TeachingViewForm
          teaching={viewedTeaching}
          open={viewTeachingFormOpen.value}
          onClose={viewTeachingFormOpen.onFalse}
        />
      )}
      {addedTeaching && (
        <TeachingAddForm
          teaching={addedTeaching}
          open={addTeachingFormOpen.value}
          onClose={addTeachingFormOpen.onFalse}
        />
      )}
      {deletedTeaching && (
        <TeachingDeleteForm
          teaching={deletedTeaching}
          open={deleteTeachingFormOpen.value}
          onClose={deleteTeachingFormOpen.onFalse}
        />
      )}
    </>
  );
}
