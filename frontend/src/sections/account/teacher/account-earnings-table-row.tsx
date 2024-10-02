import TableRow from "@mui/material/TableRow";
import { Stack, Tooltip } from "@mui/material";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { IEarningProp } from "src/types/finance";

// ----------------------------------------------------------------------

type Props = {
  row: IEarningProp;
};

export default function AccountEarningsTableRow({ row }: Props) {
  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.year} />
      </TableCell>

      <TableCell>
        <InputBase value={fDate(new Date(2000, row.month - 1, 1), "LLLL")} />
      </TableCell>

      <TableCell>
        <Stack direction="row" alignItems="center">
          <InputBase value={fCurrency(row.earnings ?? 0)} />
          {!row.actual && (
            <Tooltip title="Wartość szacunkowa">
              <Iconify icon="carbon:information-filled" />
            </Tooltip>
          )}
        </Stack>
      </TableCell>
    </TableRow>
  );
}
