import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Link, Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

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
  const openOptions = usePopover();

  const handleAdd = useCallback(() => {
    openOptions.onClose();
    onAdd(row);
  }, [openOptions, onAdd, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const handleView = useCallback(() => {
    openOptions.onClose();
    onView(row);
  }, [openOptions, onView, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  const isTeaching = useMemo(() => row.teaching, [row.teaching]);

  const isNotTeaching = useMemo(() => !row.teaching, [row.teaching]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.title} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={`${row.duration} min`} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isActive && "success") || (isInactive && "error") || "default"}
          >
            {row.active ? "Aktywna" : "Nieaktywna"}
          </Label>
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isTeaching && "success") || (isNotTeaching && "error") || "default"}
          >
            {row.teaching ? "Prowadzona" : "Nieprowadzona"}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fCurrency(row.price ?? 0)} />
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
