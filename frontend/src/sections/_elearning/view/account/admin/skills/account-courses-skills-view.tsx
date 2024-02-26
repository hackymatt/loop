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

import { useSkills, useSkillsPagesCount } from "src/api/skills/skills";

import Iconify from "src/components/iconify";
import Scrollbar from "src/components/scrollbar";

import AccountSkillsTableRow from "src/sections/_elearning/account/admin/account-skills-table-row";

import { ICourseBySkillProps } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

import SkillNewForm from "./skill-new-form";
import SkillEditForm from "./skill-edit-form";
import SkillDeleteForm from "./skill-delete-form";
import FilterSearch from "../../../../filters/filter-search";
import AccountTableHead from "../../../../account/account-table-head";

// ----------------------------------------------------------------------

const TABLE_HEAD = [
  { id: "name", label: "Nazwa tematu", minWidth: 200 },
  { id: "created_at", label: "Data utworzenia", width: 200 },
  { id: "", width: 25 },
];

const ROWS_PER_PAGE_OPTIONS = [5, 10, 25];

// ----------------------------------------------------------------------

export default function AccountCoursesSkillsView() {
  const newSkillFormOpen = useBoolean();
  const editSkillFormOpen = useBoolean();
  const deleteSkillFormOpen = useBoolean();

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount } = useSkillsPagesCount(filters);
  const { data: skills } = useSkills(filters);

  const page = filters?.page ? parseInt(filters?.page, 10) - 1 : 0;
  const rowsPerPage = filters?.page_size ? parseInt(filters?.page_size, 10) : 10;
  const orderBy = filters?.sort_by ? filters.sort_by.replace("-", "") : "title";
  const order = filters?.sort_by && filters.sort_by.startsWith("-") ? "desc" : "asc";

  const [editedSkill, setEditedSkill] = useState<ICourseBySkillProps>();
  const [deletedSkill, setDeletedSkill] = useState<ICourseBySkillProps>();

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

  const handleEditSkill = useCallback(
    (skill: ICourseBySkillProps) => {
      setEditedSkill(skill);
      editSkillFormOpen.onToggle();
    },
    [editSkillFormOpen],
  );

  const handleDeleteSkill = useCallback(
    (skill: ICourseBySkillProps) => {
      setDeletedSkill(skill);
      deleteSkillFormOpen.onToggle();
    },
    [deleteSkillFormOpen],
  );

  return (
    <>
      <Stack direction="row" spacing={1} display="flex" justifyContent="space-between">
        <Typography variant="h5" sx={{ mb: 3 }}>
          Umiejętności
        </Typography>
        <LoadingButton
          component="label"
          variant="contained"
          size="small"
          color="success"
          loading={false}
          onClick={newSkillFormOpen.onToggle}
        >
          <Iconify icon="carbon:add" />
        </LoadingButton>
      </Stack>

      <Stack direction={{ xs: "column", md: "row" }} spacing={1} sx={{ mt: 5, mb: 3 }}>
        <FilterSearch
          value={filters?.name ?? ""}
          onChangeSearch={(value) => handleChange("name", value)}
          placeholder="Nazwa umiejętności..."
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

            {skills && (
              <TableBody>
                {skills.map((row) => (
                  <AccountSkillsTableRow
                    key={row.id}
                    row={row}
                    onEdit={handleEditSkill}
                    onDelete={handleDeleteSkill}
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

      <SkillNewForm open={newSkillFormOpen.value} onClose={newSkillFormOpen.onFalse} />
      {editedSkill && (
        <SkillEditForm
          skill={editedSkill}
          open={editSkillFormOpen.value}
          onClose={editSkillFormOpen.onFalse}
        />
      )}
      {deletedSkill && (
        <SkillDeleteForm
          skill={deletedSkill}
          open={deleteSkillFormOpen.value}
          onClose={deleteSkillFormOpen.onFalse}
        />
      )}
    </>
  );
}
