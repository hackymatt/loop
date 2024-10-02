import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fDate, fDateTime } from "src/utils/format-time";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { ReviewStatus, IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

type Props = {
  row: IPurchaseItemProp;
  onAdd: (purchase: IPurchaseItemProp) => void;
  onEdit: (purchase: IPurchaseItemProp) => void;
  onDelete: (purchase: IPurchaseItemProp) => void;
};

export default function AccountReviewsTableRow({ row, onAdd, onEdit, onDelete }: Props) {
  const openOptions = usePopover();

  const handleAdd = useCallback(() => {
    openOptions.onClose();
    onAdd(row);
  }, [openOptions, onAdd, row]);

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const isCompleted = useMemo(
    () => row.reviewStatus === ReviewStatus.ukończone,
    [row.reviewStatus],
  );

  const isPending = useMemo(() => row.reviewStatus === ReviewStatus.oczekujące, [row.reviewStatus]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.lessonTitle} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isCompleted && "success") || (isPending && "warning") || "default"}
          >
            {row.reviewStatus}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fDateTime(row.lessonSlot[0])} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={row.teacher.name} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={fDate(row.createdAt)} />
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
        {isPending && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, width: "100%", color: "success.main" }}>
            <Iconify icon="carbon:add" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Dodaj recenzję</Typography>
          </MenuItem>
        )}

        {isCompleted && (
          <>
            <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
              <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Edytuj recenzję</Typography>
            </MenuItem>
            <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />
            <MenuItem onClick={handleDelete} sx={{ mr: 1, width: "100%", color: "error.main" }}>
              <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Usuń recenzję</Typography>
            </MenuItem>
          </>
        )}
      </Popover>
    </>
  );
}
