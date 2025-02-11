import { useCallback } from "react";

import { Typography } from "@mui/material";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";
import { fNumber } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { IPurchaseItemProp } from "src/types/purchase";

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

  return (
    <>
      <TableRow hover>
        <TableCell>
          <InputBase value={row.lessonTitle} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={fNumber(row.lessonPrice ?? 0, 2)} />
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
