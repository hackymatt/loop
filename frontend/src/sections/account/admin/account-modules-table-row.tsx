import { useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { ICourseModuleProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseModuleProp;
  onEdit: (module: ICourseModuleProp) => void;
  onDelete: (module: ICourseModuleProp) => void;
};

export default function AccountModulesTableRow({ row, onEdit, onDelete }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.title} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={`${(row?.totalHours ?? 0) * 60} min`} />
        </TableCell>

        <TableCell>
          <InputBase value={fCurrency(row.price ?? 0)} />
        </TableCell>

        <TableCell>
          <InputBase value={row.lessonsCount} />
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
          <Typography variant="body2">Edytuj moduł</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleDelete} sx={{ mr: 1, width: "100%", color: "error.main" }}>
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń moduł</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
