import { useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";

import Iconify from "src/components/iconify";

import { ICourseByTopicProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseByTopicProps;
  onEdit: (topic: ICourseByTopicProps) => void;
  onDelete: (topic: ICourseByTopicProps) => void;
};

export default function AccountTopicsTableRow({ row, onEdit, onDelete }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.name} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
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
        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj temat</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleDelete} sx={{ mr: 1, color: "error.main", width: "fit-content" }}>
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń temat</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
