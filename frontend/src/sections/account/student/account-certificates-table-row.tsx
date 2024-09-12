import { useMemo } from "react";

import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import { Link, Typography } from "@mui/material";
import IconButton from "@mui/material/IconButton";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";

import { BASE_URL } from "src/config-global";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { CertificateType, ICertificateProps } from "src/types/certificate";

// ----------------------------------------------------------------------

type Props = {
  row: ICertificateProps;
};

export default function AccountCertificatesTableRow({ row }: Props) {
  const openOptions = usePopover();

  const inputStyles = {
    pl: 1,
    [`&.${inputBaseClasses.focused}`]: {
      bgcolor: "action.selected",
    },
  };

  const isModule = useMemo(() => row.type === CertificateType.MODULE, [row.type]);

  const isCourse = useMemo(() => row.type === CertificateType.COURSE, [row.type]);

  const certificateUrl = useMemo(() => `${BASE_URL}/certificate/${row.id}`, [row.id]);

  return (
    <>
      <TableRow hover>
        <TableCell sx={{ px: 1 }}>
          <InputBase value={row.title} sx={inputStyles} />
        </TableCell>

        <TableCell sx={{ px: 1 }}>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isCourse && "success") || (isModule && "warning") || "default"}
          >
            {row.type}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fDate(row.completedAt)} />
        </TableCell>

        <TableCell align="right" padding="none">
          <IconButton onClick={openOptions.onOpen}>
            <Iconify icon="carbon:overflow-menu-vertical" />
          </IconButton>
        </TableCell>
      </TableRow>

      <Popover
        open={openOptions.open}
        anchorEl={openOptions.anchorEl}
        onClose={openOptions.onClose}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        transformOrigin={{ vertical: "top", horizontal: "right" }}
        slotProps={{
          paper: {
            sx: { width: "fit-content" },
          },
        }}
      >
        <Link href={certificateUrl} target="_blank" underline="none" color="inherit">
          <MenuItem sx={{ color: "success.main" }}>
            <Iconify icon="carbon:certificate" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Zobacz certyfikat</Typography>
          </MenuItem>
        </Link>
      </Popover>
    </>
  );
}
