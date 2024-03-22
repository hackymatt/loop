import { useMemo, useState, useCallback } from "react";

import { Typography } from "@mui/material";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { UserType, IUserDetailsProps } from "src/types/user";

// ----------------------------------------------------------------------

type Props = {
  row: IUserDetailsProps;
  onEdit: (user: IUserDetailsProps) => void;
};

export default function AccountUsersTableRow({ row, onEdit }: Props) {
  const [open, setOpen] = useState<HTMLButtonElement | null>(null);

  const handleOpen = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpen(event.currentTarget);
  }, []);

  const handleClose = useCallback(() => {
    setOpen(null);
  }, []);

  const handleEditDetails = useCallback(() => {
    handleClose();
    onEdit(row);
  }, [handleClose, onEdit, row]);

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  const isAdmin = useMemo(() => row.user_type === UserType.Admin, [row.user_type]);
  const isTeacher = useMemo(() => row.user_type === UserType.Wykładowca, [row.user_type]);

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.first_name} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.last_name} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.email} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.gender} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isAdmin && "error") || (isTeacher && "warning") || "default"}
          >
            {row.user_type}
          </Label>
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={fDate(row.created_at)} />
        </TableCell>

        <TableCell align="right" padding="none">
          <IconButton onClick={handleOpen}>
            <Iconify icon="carbon:overflow-menu-vertical" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
        open={Boolean(open)}
        anchorEl={open}
        onClose={handleClose}
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
      </Popover>
    </>
  );
}
