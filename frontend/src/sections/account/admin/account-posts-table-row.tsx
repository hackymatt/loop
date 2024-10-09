import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { IPostProps } from "src/types/blog";

// ----------------------------------------------------------------------

type Props = {
  row: IPostProps;
  onEdit: (post: IPostProps) => void;
  onDelete: (post: IPostProps) => void;
};

export default function AccountPostsTableRow({ row, onEdit, onDelete }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.title} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={row.duration} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isActive && "success") || (isInactive && "error") || "default"}
          >
            {row.active ? "Aktywny" : "Nieaktywny"}
          </Label>
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
          <Typography variant="body2">Edytuj artykuł</Typography>
        </MenuItem>

        {!isActive && (
          <>
            <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />
            <MenuItem
              onClick={handleDelete}
              sx={{ mr: 1, color: "error.main", width: "fit-content" }}
              disabled={row.active}
            >
              <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
              <Typography variant="body2">Usuń artykuł</Typography>
            </MenuItem>
          </>
        )}
      </Popover>
    </>
  );
}
