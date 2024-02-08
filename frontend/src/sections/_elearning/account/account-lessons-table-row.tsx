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

import { LessonStatus, IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

type Props = {
  row: IPurchaseItemProp;
};

export default function AccountLessonsTableRow({ row }: Props) {
  const [open, setOpen] = useState<HTMLButtonElement | null>(null);

  const handleOpen = useCallback((event: React.MouseEvent<HTMLButtonElement>) => {
    setOpen(event.currentTarget);
  }, []);

  const handleClose = useCallback(() => {
    setOpen(null);
  }, []);

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

  const avatarUrl = row?.teacher.photo || genderAvatarUrl;

  const isCompleted = useMemo(
    () => row.lessonStatus === LessonStatus.Zakończona,
    [row.lessonStatus],
  );

  const isPlanned = useMemo(
    () => row.lessonStatus === LessonStatus.Zaplanowana,
    [row.lessonStatus],
  );

  const isNew = useMemo(() => row.lessonStatus === LessonStatus.Nowa, [row.lessonStatus]);

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
            color={
              (isCompleted && "success") ||
              (isPlanned && "warning") ||
              (isNew && "info") ||
              "default"
            }
          >
            {row.lessonStatus}
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
          <IconButton onClick={handleOpen} disabled={isCompleted}>
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
        {isNew && (
          <MenuItem onClick={handleClose}>
            <Iconify icon="carbon:add" sx={{ mr: 1, color: "success.main" }} />
            <Typography variant="body2">Dodaj rezerwację</Typography>
          </MenuItem>
        )}

        {isPlanned && (
          <MenuItem onClick={handleClose} sx={{ color: "error.main" }}>
            <Iconify icon="carbon:trash-can" sx={{ mr: 1 }} />{" "}
            <Typography variant="body2">Odwołaj rezerwację</Typography>
          </MenuItem>
        )}
      </Popover>
    </>
  );
}
