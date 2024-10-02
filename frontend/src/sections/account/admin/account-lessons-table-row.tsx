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

import { ICourseLessonProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseLessonProp;
  onEdit: (lesson: ICourseLessonProp) => void;
  onPriceHistoryView: (lesson: ICourseLessonProp) => void;
};

export default function AccountLessonsTableRow({ row, onEdit, onPriceHistoryView }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleViewPriceHistory = useCallback(() => {
    openOptions.onClose();
    onPriceHistoryView(row);
  }, [openOptions, onPriceHistoryView, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

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
        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj lekcję</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleViewPriceHistory} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:chart-line" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Historia cen</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <Link href={row.githubUrl} target="_blank" underline="none" color="inherit">
          <MenuItem>
            <Iconify icon="carbon:logo-github" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Repozytorium</Typography>
          </MenuItem>
        </Link>
      </Popover>
    </>
  );
}
