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

import { useTopics, useTopicsPagesCount } from "src/api/topics/topics";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";
import DownloadCSVButton from "src/components/download-csv";

import AccountTopicsTableRow from "src/sections/account/admin/account-topics-table-row";

import { ITopicProps } from "src/types/topic";
import { IQueryParamValue } from "src/types/query-params";

import TopicNewForm from "./topic-new-form";
import TopicEditForm from "./topic-edit-form";
import TopicDeleteForm from "./topic-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "name", label: "Nazwa tematu", minWidth: 200 },
  { id: "created_at", label: "Data utworzenia", width: 200 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountCoursesTopicsView() {
  const newTopicFormOpen = useBoolean();
  const editTopicFormOpen = useBoolean();
  const deleteTopicFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useTopicsPagesCount(filters);
  const { data: topics, count: recordsCount } = useTopics(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

  const [editedTopic, setEditedTopic] = useState<ITopicProps>();
  const [deletedTopic, setDeletedTopic] = useState<ITopicProps>();

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

  const handleEditTopic = useCallback(
    (topic: ITopicProps) => {
      setEditedTopic(topic);
      editTopicFormOpen.onToggle();
    },
    [editTopicFormOpen],
  );

  const handleDeleteTopic = useCallback(
    (topic: ITopicProps) => {
      setDeletedTopic(topic);
      deleteTopicFormOpen.onToggle();
    },
    [deleteTopicFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Tematy
        </Typography>
        <Stack direction="row" spacing={1}>
          <DownloadCSVButton queryHook={useTopics} disabled={(recordsCount ?? 0) === 0} />
          <LoadingButton
            component="label"
            variant="contained"
            size="small"
            color="success"
            loading={false}
            onClick={newTopicFormOpen.onToggle}
          >
            <Iconify icon="carbon:add" />
          </LoadingButton>
        </Stack>
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.name ?? ""}
          onChangeSearch={(value) => handleChange("name", value)}
          placeholder="Nazwa tematu..."
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

            {topics && (
              <TableBody>
                {topics.map((row) => (
                  <AccountTopicsTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditTopic}
                    onDelete={handleDeleteTopic}
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

      <TopicNewForm open={newTopicFormOpen.value} onClose={newTopicFormOpen.onFalse} />
      {editedTopic && (
        <TopicEditForm
          topic={editedTopic}
          open={editTopicFormOpen.value}
          onClose={editTopicFormOpen.onFalse}
        />
      )}
      {deletedTopic && (
        <TopicDeleteForm
          topic={deletedTopic}
          open={deleteTopicFormOpen.value}
          onClose={deleteTopicFormOpen.onFalse}
        />
      )}
    </>
  );
}
