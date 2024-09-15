import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fNumber } from "src/utils/format-number";

import { IFinanceHistoryProp } from "src/types/finance";

// ----------------------------------------------------------------------

type Props = {
  row: IFinanceHistoryProp;
};

export default function AccountFinanceHistoryTableRow({ row }: Props) {
  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.teacher.name} />
      </TableCell>

      <TableCell>
        <InputBase value={row.account} />
      </TableCell>

      <TableCell>
        <InputBase value={fNumber(row.rate ?? 0)} />
      </TableCell>

      <TableCell>
        <InputBase value={fNumber(row.commission ?? 0)} />
      </TableCell>

      <TableCell>
        <InputBase value={fDate(row.createdAt)} />
      </TableCell>
    </TableRow>
  );
}
