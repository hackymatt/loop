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
import TablePagination from "@mui/material/TablePagination";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";

import { fDate } from "src/utils/format-time";

import { useLecturers } from "src/api/lecturers/lecturers";
import { usePurchase, usePurchasePageCount } from "src/api/purchase/purchase";

import Scrollbar from "src/components/scrollbar";

import { IQueryParamValue } from "src/types/query-params";
import { ReviewStatus, IPurchaseItemProp } from "src/types/purchase";

import ReviewNewForm from "./review-new-form";
import ReviewEditForm from "./review-edit-form";
import ReviewDeleteForm from "./review-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import FilterTeacher from "../../../../filters/filter-teacher";
import AccountTableHead from "../../../../account/account-table-head";
import AccountReviewsTableRow from "../../../../account/student/account-reviews-table-row";

// ----------------------------------------------------------------------

const TABS = [
  { id: ReviewStatus.brak, label: "Wszystkie recenzje" },
  { id: ReviewStatus.oczekujące, label: "Oczekujące" },
  { id: ReviewStatus.ukończone, label: "Ukończone" },
];

const TABLE_HEAD = [
  { id: "lesson_title", label: "Nazwa lekcji", minWidth: 230 },
  { id: "lesson_status", label: "Status" },
  { id: "reservation_date", label: "Termin", minWidth: 150 },
  { id: "lecturer_id", label: "Instruktor", minWidth: 100 },
  { id: "created_at", label: "Data zakupu", minWidth: 150 },
  { id: "" },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25, { label: "Wszystkie", value: -1 }];

// ----------------------------------------------------------------------

export default function AccountReviewsView() {
  const addReviewFormOpen = useBoolean();
  const editReviewFormOpen = useBoolean();
  const deleteReviewFormOpen = useBoolean();

  const [addedPurchase, setAddedPurchase] = useState<IPurchaseItemProp>();
  const [editedPurchase, setEditedPurchase] = useState<IPurchaseItemProp>();
  const [deletedPurchase, setDeletedPurchase] = useState<IPurchaseItemProp>();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = usePurchasePageCount(filters);
  const { data: reviews, count: recordsCount } = usePurchase(filters);

  const { data: teachers } = useLecturers({ sort_by: "full_name", page_size: -1 });

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "created_at";
  const order = filters?.sort_by && !filters.sort_by.startsWith("-") ? "asc" : "desc";
  const tab = filters?.review_status ? filters.review_status : ReviewStatus.brak;

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

  const manageTab = useCallback(
    (tabName: string) => {
      if (tabName === ReviewStatus.brak) {
        handleChange("review_status", "");
        handleChange("review_status_exclude", tabName);
      } else {
        handleChange("review_status", tabName);
        handleChange("review_status_exclude", "");
      }
    },
    [handleChange],
  );

  const handleChangeTab = useCallback(
    (event: React.SyntheticEvent, newValue: string) => {
      manageTab(newValue);
    },
    [manageTab],
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

  const handleAddReview = useCallback(
    (purchase: IPurchaseItemProp) => {
      setAddedPurchase(purchase);
      addReviewFormOpen.onToggle();
    },
    [addReviewFormOpen],
  );

  const handleEditReview = useCallback(
    (purchase: IPurchaseItemProp) => {
      setEditedPurchase(purchase);
      editReviewFormOpen.onToggle();
    },
    [editReviewFormOpen],
  );

  const handleDeleteReview = useCallback(
    (purchase: IPurchaseItemProp) => {
      setDeletedPurchase(purchase);
      deleteReviewFormOpen.onToggle();
    },
    [deleteReviewFormOpen],
  );

  return (
    <>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Recenzje
      </Typography>

      <Tabs
        value={TABS.find((t) => t.id === tab)?.id ?? ReviewStatus.brak}
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
          value={filters?.lesson_title ?? ""}
          onChangeSearch={(value) => handleChange("lesson_title", value)}
          placeholder="Nazwa lekcji..."
        />

        {teachers && (
          <FilterTeacher
            value={filters?.lecturer_id ?? ""}
            options={teachers ?? []}
            onChange={(value) => handleChange("lecturer_id", value)}
          />
        )}

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
              headCells={TABLE_HEAD}
            />

            {reviews && (
              <TableBody>
                {reviews.map((row) => (
                  <AccountReviewsTableRow
                    key={row.id}
                    row={row}
                    onAdd={handleAddReview}
                    onEdit={handleEditReview}
                    onDelete={handleDeleteReview}
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

      {addedPurchase && (
        <ReviewNewForm
          purchase={addedPurchase}
          open={addReviewFormOpen.value}
          onClose={addReviewFormOpen.onFalse}
        />
      )}

      {editedPurchase && (
        <ReviewEditForm
          purchase={editedPurchase}
          open={editReviewFormOpen.value}
          onClose={editReviewFormOpen.onFalse}
        />
      )}

      {deletedPurchase && (
        <ReviewDeleteForm
          purchase={deletedPurchase}
          open={deleteReviewFormOpen.value}
          onClose={deleteReviewFormOpen.onFalse}
        />
      )}
    </>
  );
}
