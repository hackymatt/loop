import { useMemo, useState, useCallback } from "react";

import { Stack } from "@mui/system";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Link, Avatar, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { paths } from "src/routes/paths";

import { fDate, fDateTime } from "src/utils/format-time";

import { useUserDetails } from "src/api/auth/details";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { LessonStatus, IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

const CANCELLATION_TIME = 24 as const; // 24 hours

// ----------------------------------------------------------------------

type Props = {
  row: IPurchaseItemProp;
  onAdd: (purchase: IPurchaseItemProp) => void;
  onDelete: (purchase: IPurchaseItemProp) => void;
};

export default function AccountLessonsTableRow({ row, onAdd, onDelete }: Props) {
  const { data: userDetails } = useUserDetails();

  const certificateUrl = useMemo(
    () => `${paths.certificate}/${userDetails?.id}-${row.reservationId}`,
    [row.reservationId, userDetails.id],
  );

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

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  const genderAvatarUrl =
    row?.teacher.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = row?.teacher.avatarUrl || genderAvatarUrl;

  const isCompleted = useMemo(
    () => row.lessonStatus === LessonStatus.zakończona,
    [row.lessonStatus],
  );

  const isPlanned = useMemo(
    () => row.lessonStatus === LessonStatus.zaplanowana,
    [row.lessonStatus],
  );

  const isConfirmed = useMemo(
    () => row.lessonStatus === LessonStatus.potwierdzona,
    [row.lessonStatus],
  );

  const isNew = useMemo(() => row.lessonStatus === LessonStatus.nowa, [row.lessonStatus]);

  const canCancel = useMemo(
    () =>
      (new Date(row.lessonSlot[0]).getTime() - new Date().getTime()) / (60 * 60 * 1000) >=
      CANCELLATION_TIME,
    [row.lessonSlot],
  );

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.lessonTitle} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={
              (isCompleted && "error") ||
              (isConfirmed && "success") ||
              (isPlanned && "warning") ||
              (isNew && "info") ||
              "default"
            }
          >
            {row.lessonStatus}
          </Label>
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <InputBase value={fDateTime(row.lessonSlot[0])} />
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
            sx: { width: "fit-content" },
          },
        }}
      >
        {isNew && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, color: "success.main" }}>
            <Iconify icon="carbon:add" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Dodaj rezerwację</Typography>
          </MenuItem>
        )}

        {isPlanned && (
          <MenuItem onClick={handleDelete} sx={{ color: "error.main" }} disabled={!canCancel}>
            <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Usuń rezerwację</Typography>
          </MenuItem>
        )}

        {isConfirmed && (
          <Link href={row.meetingUrl} target="_blank" underline="none" color="inherit">
            <MenuItem>
              <Iconify icon="logos:google-meet" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Dołącz do spotkania</Typography>
            </MenuItem>
          </Link>
        )}

        {isCompleted && (
          <Link href={certificateUrl} target="_blank" underline="none" color="inherit">
            <MenuItem sx={{ color: "success.main" }}>
              <Iconify icon="carbon:certificate" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Zobacz certyfikat ukończenia</Typography>
            </MenuItem>
          </Link>
        )}
      </Popover>
    </>
  );
}
