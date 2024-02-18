import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";
import { fCurrency } from "src/utils/format-number";

import { ICourseLessonPriceHistoryProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  row: ICourseLessonPriceHistoryProp;
};

export default function AccountLessonsPriceHistoryTableRow({ row }: Props) {
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
        <InputBase value={row.lesson.title} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fCurrency(row.price ?? 0)} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fDate(row.createdAt)} />
      </TableCell>
    </TableRow>
  );
}
