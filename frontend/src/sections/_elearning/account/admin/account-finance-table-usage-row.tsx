import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

import { ICouponUsageProps } from "src/types/coupon";

// ----------------------------------------------------------------------

type Props = {
  row: ICouponUsageProps;
};

export default function AccountCouponUsageTableRow({ row }: Props) {
  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  return (
    <TableRow hover>
      <TableCell sx={{ px: 1 }}>
        <InputBase value={row.user.email} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={row.coupon.code} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fDate(row.created_at)} />
      </TableCell>
    </TableRow>
  );
}
