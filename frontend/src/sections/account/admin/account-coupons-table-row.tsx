import { useMemo, useCallback } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";
import { Divider, Typography } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fDateTime } from "src/utils/format-time";
import { fPercent, fCurrency } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { ICouponProps } from "src/types/coupon";

// ----------------------------------------------------------------------

type Props = {
  row: ICouponProps;
  onEdit: (coupon: ICouponProps) => void;
  onDelete: (coupon: ICouponProps) => void;
  onViewUsage: (coupon: ICouponProps) => void;
};

export default function AccountCouponsTableRow({ row, onEdit, onDelete, onViewUsage }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const handleViewUsage = useCallback(() => {
    openOptions.onClose();
    onViewUsage(row);
  }, [openOptions, onViewUsage, row]);

  const isActive = useMemo(() => row.active, [row.active]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.code} />
        </TableCell>

        <TableCell>
          <InputBase value={row.is_percentage ? fPercent(row.discount) : fCurrency(row.discount)} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isActive && "success") || (!isActive && "error") || "default"}
          >
            {row.active ? "Aktywny" : "Nieaktywny"}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fDateTime(row.expiration_date)} />
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
        <MenuItem onClick={handleViewUsage} sx={{ mr: 1, width: "100%", color: "success.main" }}>
          <Iconify icon="carbon:user-activity" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Wykorzystanie kuponu</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj kupon</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleDelete} sx={{ mr: 1, width: "100%", color: "error.main" }}>
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń kupon</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
