import { useMemo } from "react";

import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import Label from "src/components/label";

import { IPaymentProp, PaymentStatus } from "src/types/payment";

// ----------------------------------------------------------------------

type Props = {
  row: IPaymentProp;
};

export default function AccountLessonsPaymentsTableRow({ row }: Props) {
  const isSuccess = useMemo(() => row.status === PaymentStatus.SUCCESS, [row.status]);
  const isFailure = useMemo(() => row.status === PaymentStatus.FAILURE, [row.status]);

  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.sessionId} sx={{ width: 1 }} />
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
    </TableRow>
  );
}
