import { useMemo, useState, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Link, Divider, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fCurrency } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { ITeachingProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ITeachingProp;
  onView: (teaching: ITeachingProp) => void;
  onAdd: (teaching: ITeachingProp) => void;
  onDelete: (teaching: ITeachingProp) => void;
};

export default function AccountTeachingsTableRow({ row, onView, onAdd, onDelete }: Props) {
  const [open, setOpen] = useState<HTMLButtonElement | null>(null);

  const handleOpen = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpen(event.currentTarget);
  }, []);

  const handleClose = useCallback(() => {
    setOpen(null);
  }, []);

  const handleAdd = useCallback(() => {
    handleClose();
    onAdd(row);
  }, [handleClose, onAdd, row]);

  const handleDelete = useCallback(() => {
    handleClose();
    onDelete(row);
  }, [handleClose, onDelete, row]);

  const handleView = useCallback(() => {
    handleClose();
    onView(row);
  }, [handleClose, onView, row]);

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  const isTeaching = useMemo(() => row.teaching, [row.teaching]);

  const isNotTeaching = useMemo(() => !row.teaching, [row.teaching]);

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.title} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.duration} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isActive && "success") || (isInactive && "error") || "default"}
          >
            {row.active ? "Aktywna" : "Nieaktywna"}
          </Label>
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isTeaching && "success") || (isNotTeaching && "error") || "default"}
          >
            {row.teaching ? "Prowadzona" : "Nieprowadzona"}
          </Label>
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={fCurrency(row.price ?? 0)} sx={inputStyles} />
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
        {isNotTeaching && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, width: "100%", color: "success.main" }}>
            <Iconify icon="carbon:add" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Zacznij uczyć</Typography>
          </MenuItem>
        )}

        {isTeaching && (
          <MenuItem onClick={handleDelete} sx={{ mr: 1, width: "100%", color: "error.main" }}>
            <Iconify icon="carbon:subtract" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Przestań uczyć</Typography>
          </MenuItem>
        )}
        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <Link href={row.githubUrl} target="_blank" underline="none" color="inherit">
          <MenuItem>
            <Iconify icon="carbon:logo-github" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Repozytorium</Typography>
          </MenuItem>
        </Link>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleView} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Szczegóły</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
