import { useState, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import Iconify from "src/components/iconify";

import { ICourseModuleProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseModuleProp;
  onEdit: (module: ICourseModuleProp) => void;
  onDelete: (module: ICourseModuleProp) => void;
};

export default function AccountModulesTableRow({ row, onEdit, onDelete }: Props) {
  const [open, setOpen] = useState<HTMLButtonElement | null>(null);

  const handleOpen = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpen(event.currentTarget);
  }, []);

  const handleClose = useCallback(() => {
    setOpen(null);
  }, []);

  const handleEdit = useCallback(() => {
    handleClose();
    onEdit(row);
  }, [handleClose, onEdit, row]);

  const handleDelete = useCallback(() => {
    handleClose();
    onDelete(row);
  }, [handleClose, onDelete, row]);

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.title} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.lessonsCount} sx={inputStyles} />
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
        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj moduł</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleDelete} sx={{ mr: 1, width: "100%", color: "error.main" }}>
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń moduł</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
