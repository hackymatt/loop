import { useMemo } from "react";

import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { fDate } from "src/utils/format-time";

import Label from "src/components/label";

import { INewsletterProps } from "src/types/newsletter";

// ----------------------------------------------------------------------

type Props = {
  row: INewsletterProps;
};

export default function AccountNewsletterTableRow({ row }: Props) {
  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
    width: 1,
  };

  const isActive = useMemo(() => row.active, [row.active]);

  const isInactive = useMemo(() => !row.active, [row.active]);

  return (
    <TableRow hover>
      <TableCell sx={{ px: 1 }}>
        <InputBase value={row.uuid} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={row.email} sx={inputStyles} />
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <Label
          sx={{ textTransform: "uppercase" }}
          color={(isActive && "success") || (isInactive && "error") || "default"}
        >
          {row.active ? "Aktywny" : "Nieaktywny"}
        </Label>
      </TableCell>

      <TableCell sx={{ px: 1 }}>
        <InputBase value={fDate(row.created_at)} sx={inputStyles} />
      </TableCell>
    </TableRow>
  );
}
