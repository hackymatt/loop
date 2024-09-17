import { useMemo } from "react";

import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

import Label from "src/components/label";

import { INewsletterProps } from "src/types/newsletter";

// ----------------------------------------------------------------------

type Props = {
  row: INewsletterProps;
};

export default function AccountNewsletterTableRow({ row }: Props) {
  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  return (
    <TableRow hover>
      <TableCell>
        <InputBase value={row.uuid} sx={{ width: 1 }} />
      </TableCell>

      <TableCell>
        <InputBase value={row.email} sx={{ width: 1 }} />
      </TableCell>

      <TableCell>
        <Label
          sx={{ textTransform: "uppercase" }}
          color={(isActive && "success") || (isInactive && "error") || "default"}
        >
          {row.active ? "Aktywny" : "Nieaktywny"}
        </Label>
      </TableCell>

      <TableCell>
        <InputBase value={fDate(row.created_at)} />
      </TableCell>
    </TableRow>
  );
}
