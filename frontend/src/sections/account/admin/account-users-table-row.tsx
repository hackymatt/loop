import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";

import { UserType } from "src/consts/user-type";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { IUserDetailsProps } from "src/types/user";

// ----------------------------------------------------------------------

type Props = {
  row: IUserDetailsProps;
  onEdit: (user: IUserDetailsProps) => void;
  onEditFinance: (user: IUserDetailsProps) => void;
  onFinanceHistoryView: (user: IUserDetailsProps) => void;
};

export default function AccountUsersTableRow({
  row,
  onEdit,
  onEditFinance,
  onFinanceHistoryView,
}: Props) {
  const openOptions = usePopover();

  const handleEditDetails = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleEditFinanceDetails = useCallback(() => {
    openOptions.onClose();
    onEditFinance(row);
  }, [openOptions, onEditFinance, row]);

  const handleViewFinanceHistory = useCallback(() => {
    openOptions.onClose();
    onFinanceHistoryView(row);
  }, [openOptions, onFinanceHistoryView, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  const isAdmin = useMemo(() => row.userType === UserType.Admin, [row.userType]);
  const isTeacher = useMemo(() => row.userType === UserType.Teacher, [row.userType]);
  const isStudent = useMemo(() => row.userType === UserType.Student, [row.userType]);

  return (
    <>
      <TableRow hover>
        <TableCell
          align="center"
          sx={{
            px: 1,
            color: isActive ? "success.main" : "error.main",
          }}
        >
          <Iconify icon={isActive ? "carbon:checkmark-filled" : "carbon:close-filled"} />
        </TableCell>

        <TableCell>
          <InputBase value={row.email} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={
              (isAdmin && "error") ||
              (isTeacher && "warning") ||
              (isStudent && "success") ||
              "default"
            }
          >
            {row.userType}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fDate(row.createdAt)} sx={{ width: 1 }} />
        </TableCell>

        <TableCell align="right" padding="none">
          <IconButton onClick={openOptions.onOpen}>
            <Iconify icon="carbon:overflow-menu-vertical" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
        open={openOptions.open}
        anchorEl={openOptions.anchorEl}
        onClose={openOptions.onClose}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        slotProps={{
          paper: {
            sx: { width: "fit-content" },
          },
        }}
      >
        <MenuItem onClick={handleEditDetails} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj dane</Typography>
        </MenuItem>

        {isTeacher && (
          <>
            <MenuItem onClick={handleEditFinanceDetails} sx={{ mr: 1, width: "100%" }}>
              <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Edytuj dane finansowe</Typography>
            </MenuItem>

            <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

            <MenuItem onClick={handleViewFinanceHistory} sx={{ mr: 1, width: "100%" }}>
              <Iconify icon="carbon:finance" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Historia danych finansowych</Typography>
            </MenuItem>
          </>
        )}
      </Popover>
    </>
  );
}
