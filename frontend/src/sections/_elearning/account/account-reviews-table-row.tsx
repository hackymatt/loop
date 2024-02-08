import { useMemo, useState, useCallback } from "react";

import { Stack } from "@mui/system";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Avatar, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

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

export default function AccountLessonsTableRow({ row, onAdd, onEdit, onDelete }: Props) {
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
  };

  const genderAvatarUrl =
    row?.teacher.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = row?.teacher.avatarUrl || genderAvatarUrl;

  const isCompleted = useMemo(
    () => row.reviewStatus === ReviewStatus.ukończone,
    [row.reviewStatus],
  );

  const isPending = useMemo(() => row.reviewStatus === ReviewStatus.oczekujące, [row.reviewStatus]);

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.courseTitle} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.lessonTitle} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isCompleted && "success") || (isPending && "warning") || "default"}
          >
            {row.reviewStatus}
          </Label>
        </TableCell>

        <TableCell>
          <Stack spacing={0.5} direction="row" alignItems="center">
            {row.teacher.name && <Avatar src={avatarUrl} sx={{ width: 36, height: 36 }} />}
            <Typography variant="body2">{row.teacher.name}</Typography>
          </Stack>
        </TableCell>

        <TableCell>
          <InputBase value={fDate(row.createdAt)} />
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
        {isPending && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, color: "success.main" }}>
            <Iconify icon="carbon:add" />
            <Typography variant="body2">Dodaj recenzję</Typography>
          </MenuItem>
        )}

        {isCompleted && (
          <>
            <MenuItem onClick={handleEdit}>
              <Iconify icon="carbon:edit" sx={{ mr: 1 }} />{" "}
              <Typography variant="body2">Zmień recenzję</Typography>
            </MenuItem>
            <MenuItem onClick={handleDelete} sx={{ color: "error.main" }}>
              <Iconify icon="carbon:trash-can" sx={{ mr: 1 }} />{" "}
              <Typography variant="body2">Usuń recenzję</Typography>
            </MenuItem>
          </>
        )}
      </Popover>
    </>
  );
}
