import { useState, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Button, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { ICourseLessonProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseLessonProp;
  onEdit: (lesson: ICourseLessonProp) => void;
};

export default function AccountLessonsTableRow({ row, onEdit }: Props) {
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

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
  };

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
          <InputBase value={fCurrency(row.price ?? 0)} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Button
            size="small"
            variant="outlined"
            component="a"
            href={row.githubUrl}
            target="_blank"
            startIcon={<Iconify icon="carbon:logo-github" />}
            sx={{ ml: 1 }}
          >
            GitHub
          </Button>
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
        <MenuItem onClick={handleEdit} sx={{ mr: 1 }}>
          <Iconify icon="carbon:edit" />
          <Typography variant="body2">Edytuj lekcję</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
