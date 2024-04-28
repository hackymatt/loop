import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fNumber } from "src/utils/format-number";

import { IFinanceHistoryProp } from "src/types/finance";

// ----------------------------------------------------------------------

type Props = {
  row: IFinanceHistoryProp;
};

export default function AccountFinanceHistoryTableRow({ row }: Props) {
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
        <InputBase value={row.teacher.name} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={row.account} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fNumber(row.rate ?? 0)} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fNumber(row.commission ?? 0)} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fDate(row.createdAt)} />
      </TableCell>
    </TableRow>
  );
}
