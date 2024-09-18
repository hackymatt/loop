import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Link, Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fDate, fDateTime } from "src/utils/format-time";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { LessonStatus, IRecordingProp, IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

const CANCELLATION_TIME = 24 as const; // 24 hours

// ----------------------------------------------------------------------

type Props = {
  row: IPurchaseItemProp;
  onAdd: (purchase: IPurchaseItemProp) => void;
  onDelete: (purchase: IPurchaseItemProp) => void;
  onSendMessage: (purchase: IPurchaseItemProp) => void;
};

export default function AccountLessonsTableRow({ row, onAdd, onDelete, onSendMessage }: Props) {
  const openOptions = usePopover();

  const handleAdd = useCallback(() => {
    openOptions.onClose();
    onAdd(row);
  }, [openOptions, onAdd, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const handleSendMessage = useCallback(() => {
    openOptions.onClose();
    onSendMessage(row);
  }, [openOptions, onSendMessage, row]);

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

  const hasRecordings = useMemo(() => row.recordings.length > 0, [row.recordings.length]);
  const moreThanOneRecording = useMemo(() => row.recordings.length > 1, [row.recordings.length]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.lessonTitle} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
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

        <TableCell>
          <InputBase value={fDateTime(row.lessonSlot[0])} />
        </TableCell>

        <TableCell>
          <InputBase value={row.teacher.name} />
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
        {isNew && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, color: "success.main" }}>
            <Iconify icon="carbon:add" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Dodaj rezerwację</Typography>
          </MenuItem>
        )}

        {!isNew && (
          <MenuItem onClick={handleSendMessage} sx={{ color: "success.main" }}>
            <Iconify icon="carbon:email" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Napisz do instruktora</Typography>
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
          <>
            {hasRecordings && <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />}
            {row.recordings.map((recording: IRecordingProp, index: number) => (
              <Link
                key={recording.name}
                href={recording.url}
                target="_blank"
                underline="none"
                color="inherit"
              >
                <MenuItem>
                  <Iconify icon="carbon:download" sx={{ mr: 0.5 }} />
                  <Typography variant="body2">
                    Pobierz nagranie{moreThanOneRecording ? ` #${index + 1}` : ""}
                  </Typography>
                </MenuItem>
              </Link>
            ))}
          </>
        )}
      </Popover>
    </>
  );
}
