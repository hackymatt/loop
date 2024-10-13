"use client";

import { useMemo, useState, useCallback } from "react";

import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import Tabs from "@mui/material/Tabs";
import Stack from "@mui/material/Stack";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import Typography from "@mui/material/Typography";
import TableContainer from "@mui/material/TableContainer";
import { tableCellClasses } from "@mui/material/TableCell";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import TablePagination from "@mui/material/TablePagination";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useMessages, useMessagesPagesCount } from "src/api/message/messages";

import Scrollbar from "src/components/scrollbar";

import AccountMessagesTableRow from "src/sections/account/account-messages-table-row";

import { IQueryParamValue } from "src/types/query-params";
import { MessageType, IMessageProp } from "src/types/message";

import MessageReadForm from "./message-read-form";
import MessageReplyForm from "./message-reply-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABS = [
  { id: MessageType.INBOX, label: "Otrzymane" },
  { id: MessageType.SENT, label: "Wysłane" },
];

const INBOX_TABLE_HEAD = [
  { id: "sender", label: "Od", minWidth: 200 },
  { id: "subject", label: "Tytuł", minWidth: 150 },
  { id: "body", label: "Treść", minWidth: 160, maxWidth: 180 },
  { id: "status", label: "Status" },
  { id: "created_at", label: "Data otrzymania", minWidth: 150 },
  { id: "" },
];

const SENT_TABLE_HEAD = [
  { id: "recipient", label: "Do", minWidth: 200 },
  { id: "subject", label: "Tytuł", minWidth: 150 },
  { id: "body", label: "Treść", minWidth: 160, maxWidth: 180 },
  { id: "status", label: "Status" },
  { id: "created_at", label: "Data wysłania", minWidth: 150 },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountMessagesView() {
  const newMessageFormOpen = useBoolean();
  const readMessageFormOpen = useBoolean();

  const [newMessage, setNewMessage] = useState<IMessageProp>();
  const [readMessage, setReadMessage] = useState<IMessageProp>();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useMessagesPagesCount(filters);
  const { data: messages, count: recordsCount } = useMessages(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "created_at";
  const order = filters?.sort_by && !filters.sort_by.startsWith("-") ? "asc" : "desc";
  const tab = filters?.type ? filters.type : "";

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
      handleChange("type", newValue);
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

  const handleAdd = useCallback(
    (message: IMessageProp) => {
      setNewMessage(message);
      newMessageFormOpen.onToggle();
    },
    [newMessageFormOpen],
  );

  const handleRead = useCallback(
    (message: IMessageProp) => {
      setReadMessage(message);
      readMessageFormOpen.onToggle();
    },
    [readMessageFormOpen],
  );

  return (
    <>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Wiadomości
      </Typography>

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

      <Stack direction={{ xs: "column", md: "row" }} spacing={2} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.search ?? ""}
          onChangeSearch={(value) => handleChange("search", value)}
          placeholder="Szukaj..."
        />

        <DatePicker
          value={filters?.created_at ? new Date(filters.created_at) : null}
          onChange={(value: Date | null) =>
            handleChange("created_at", value ? fDate(value, "yyyy-MM-dd") : "")
          }
          sx={{ width: 1, minWidth: 180 }}
          slotProps={{
            textField: { size: "small", hiddenLabel: true, placeholder: "Data zakupu" },
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
              headCells={tab === MessageType.INBOX ? INBOX_TABLE_HEAD : SENT_TABLE_HEAD}
            />

            {messages && (
              <TableBody>
                {messages.map((row) => (
                  <AccountMessagesTableRow
                    key={row.id}
                    row={row}
                    type={tab as MessageType}
                    onAdd={handleAdd}
                    onRead={handleRead}
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

      {newMessage && (
        <MessageReplyForm
          message={newMessage}
          open={newMessageFormOpen.value}
          onClose={newMessageFormOpen.onFalse}
        />
      )}

      {readMessage && (
        <MessageReadForm
          message={readMessage}
          type={tab as MessageType}
          open={readMessageFormOpen.value}
          onClose={readMessageFormOpen.onFalse}
        />
      )}
    </>
  );
}
