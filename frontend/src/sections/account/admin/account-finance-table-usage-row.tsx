import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

import { ICouponUsageProps } from "src/types/coupon";

// ----------------------------------------------------------------------

type Props = {
  row: ICouponUsageProps;
};

export default function AccountCouponUsageTableRow({ row }: Props) {
  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.user.email} />
      </TableCell>

      <TableCell>
        <InputBase value={row.coupon.code} />
      </TableCell>

      <TableCell>
        <InputBase value={fDate(row.created_at)} />
      </TableCell>
    </TableRow>
  );
}
