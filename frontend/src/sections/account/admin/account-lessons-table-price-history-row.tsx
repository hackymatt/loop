import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import { ICourseLessonPriceHistoryProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseLessonPriceHistoryProp;
};

export default function AccountLessonsPriceHistoryTableRow({ row }: Props) {
  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.lesson.title} sx={{ width: 1 }} />
      </TableCell>

      <TableCell>
        <InputBase value={fCurrency(row.price ?? 0)} />
      </TableCell>

      <TableCell>
        <InputBase value={fDate(row.createdAt)} />
      </TableCell>
    </TableRow>
  );
}
