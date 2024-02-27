import { useMemo, useState, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Link, Divider, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { paths } from "src/routes/paths";

import { fCurrency } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { ICourseProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseProps;
  onEdit: (course: ICourseProps) => void;
  onDelete: (course: ICourseProps) => void;
};

export default function AccountCoursesTableRow({ row, onEdit, onDelete }: Props) {
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

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.slug} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.totalHours * 60} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isActive && "success") || (isInactive && "error") || "default"}
          >
            {row.active ? "Aktywny" : "Nieaktywny"}
          </Label>
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={fCurrency(row.price ?? 0)} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.level} sx={inputStyles} />
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
            sx: { width: 160 },
          },
        }}
      >
        <Link href={`${paths.course}/${row.id}`} target="_blank" rel="noopener">
          <MenuItem sx={{ mr: 1, width: "fit-content", color: "success.main" }}>
            <Iconify icon="carbon:view" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Podgląd</Typography>
          </MenuItem>
        </Link>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "fit-content" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj kurs</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem
          onClick={handleDelete}
          sx={{ mr: 1, color: "error.main", width: "fit-content" }}
          disabled={row.active}
        >
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń kurs</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
