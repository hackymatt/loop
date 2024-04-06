import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import { IEarningProp } from "src/types/finance";

// ----------------------------------------------------------------------

type Props = {
  row: IEarningProp;
};

export default function AccountEarningsTableRow({ row }: Props) {
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
        <InputBase value={row.year} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fDate(new Date(2000, row.month, 1), "LLLL")} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fCurrency(row.earnings ?? 0)} sx={inputStyles} />
      </TableCell>
    </TableRow>
  );
}
