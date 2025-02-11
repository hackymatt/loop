import { useMemo, useCallback } from "react";

import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import { Popover, Divider, MenuItem, Typography, IconButton } from "@mui/material";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { IPaymentProp, PaymentStatus } from "src/types/payment";

// ----------------------------------------------------------------------

type Props = {
  row: IPaymentProp;
  onEdit: (payment: IPaymentProp) => void;
  onDelete: (payment: IPaymentProp) => void;
};

export default function AccountServicesPaymentsTableRow({ row, onEdit, onDelete }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleDelete = useCallback(() => {
    openOptions.onClose();
    onDelete(row);
  }, [openOptions, onDelete, row]);

  const isSuccess = useMemo(() => row.status === PaymentStatus.SUCCESS, [row.status]);
  const isFailure = useMemo(() => row.status === PaymentStatus.FAILURE, [row.status]);

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.sessionId} />
        </TableCell>

        <TableCell>
          <InputBase value={fCurrency(row.amount ?? 0, row.currency ?? "PLN")} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isSuccess && "success") || (isFailure && "error") || "default"}
          >
            {row.status}
          </Label>
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
        <MenuItem onClick={handleEdit} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:edit" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Edytuj płatność</Typography>
        </MenuItem>

        <Divider sx={{ borderStyle: "dashed", mt: 0.5 }} />

        <MenuItem onClick={handleDelete} sx={{ mr: 1, color: "error.main", width: "fit-content" }}>
          <Iconify icon="carbon:trash-can" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Usuń płatność</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
