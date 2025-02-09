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

import { PaymentStatus } from "src/types/payment";
import { IPaymentItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

type Props = {
  row: IPaymentItemProp;
  onEdit: (payment: IPaymentItemProp) => void;
  onInvoice: (payment: IPaymentItemProp) => void;
};

export default function AccountPaymentsTableRow({ row, onEdit, onInvoice }: Props) {
  const openOptions = usePopover();

  const handleEdit = useCallback(() => {
    openOptions.onClose();
    onEdit(row);
  }, [openOptions, onEdit, row]);

  const handleInvoice = useCallback(() => {
    openOptions.onClose();
    onInvoice(row);
  }, [openOptions, onInvoice, row]);

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

        <MenuItem onClick={handleInvoice} sx={{ mr: 1, width: "100%" }}>
          <Iconify icon="carbon:document-signed" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Wygeneruj fakturę</Typography>
        </MenuItem>
      </Popover>
    </>
  );
}
