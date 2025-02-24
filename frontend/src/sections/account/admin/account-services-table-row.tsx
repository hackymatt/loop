import { useMemo, useCallback } from "react";

import { Typography } from "@mui/material";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import InputBase from "@mui/material/InputBase";
import TableCell from "@mui/material/TableCell";
import IconButton from "@mui/material/IconButton";

import { usePopover } from "src/hooks/use-popover";

import { fNumber } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { IServiceProp } from "src/types/service";

// ----------------------------------------------------------------------

type Props = {
  row: IServiceProp;
  onEdit: (lesson: IServiceProp) => void;
};

export default function AccountServicesTableRow({ row, onEdit }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.title} sx={{ width: 1 }} />
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
          <InputBase value={fNumber(row.price ?? 0)} />
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
          <Typography variant="body2">Edytuj usługę</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
