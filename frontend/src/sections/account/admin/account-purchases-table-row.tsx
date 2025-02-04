import { useMemo, useCallback } from "react";

import { Typography } from "@mui/material";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";

import { usePopover } from "src/hooks/use-popover";

import { fDate, fDateTime } from "src/utils/format-time";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { LessonStatus, IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

type Props = {
  row: IPurchaseItemProp;
  onViewPayment: (purchase: IPurchaseItemProp) => void;
};

export default function AccountPurchasesTableRow({ row, onViewPayment }: Props) {
  const openOptions = usePopover();

  const handleViewPayment = useCallback(() => {
    openOptions.onClose();
    onViewPayment(row);
  }, [openOptions, onViewPayment, row]);

  const isCompleted = useMemo(
    () => row.lessonStatus === LessonStatus.COMPLETED,
    [row.lessonStatus],
  );

  const isPlanned = useMemo(() => row.lessonStatus === LessonStatus.PLANNED, [row.lessonStatus]);

  const isConfirmed = useMemo(
    () => row.lessonStatus === LessonStatus.CONFIRMED,
    [row.lessonStatus],
  );

  const isNew = useMemo(() => row.lessonStatus === LessonStatus.NEW, [row.lessonStatus]);

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
        <MenuItem onClick={handleViewPayment} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:money" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Zobacz płatność</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
