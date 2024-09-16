import { useMemo, useCallback } from "react";

import { Typography } from "@mui/material";
import Popover from "@mui/material/Popover";
import MenuItem from "@mui/material/MenuItem";
import TableRow from "@mui/material/TableRow";
import TableCell from "@mui/material/TableCell";
import InputBase from "@mui/material/InputBase";
import IconButton from "@mui/material/IconButton";

import { usePopover } from "src/hooks/use-popover";

import { fDate } from "src/utils/format-time";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { MessageType, IMessageProp, MessageStatus } from "src/types/message";

// ----------------------------------------------------------------------

type Props = {
  row: IMessageProp;
  type: MessageType;
  onAdd: (message: IMessageProp) => void;
  onRead: (message: IMessageProp) => void;
};

export default function AccountMessagesTableRow({ row, type, onAdd, onRead }: Props) {
  const openOptions = usePopover();

  const handleAdd = useCallback(() => {
    openOptions.onClose();
    onAdd(row);
  }, [openOptions, onAdd, row]);

  const handleRead = useCallback(() => {
    openOptions.onClose();
    onRead(row);
  }, [openOptions, onRead, row]);

  const isInbox = useMemo(() => type === MessageType.INBOX, [type]);

  const isSent = useMemo(() => type === MessageType.SENT, [type]);

  const isNew = useMemo(() => row.status === MessageStatus.NEW, [row.status]);

  const isRead = useMemo(() => row.status === MessageStatus.READ, [row.status]);

  return (
    <>
      <TableRow hover>
        {isInbox && (
          <TableCell>
            <InputBase value={row.sender.name} sx={{ width: 1 }} />
          </TableCell>
        )}

        {isSent && (
          <TableCell>
            <InputBase value={row.recipient.name} sx={{ width: 1 }} />
          </TableCell>
        )}

        <TableCell>
          <InputBase value={row.subject} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <InputBase value={row.body} sx={{ width: 1 }} />
        </TableCell>

        <TableCell>
          <Label
            sx={{ textTransform: "uppercase" }}
            color={(isNew && "error") || (isRead && "success") || "default"}
          >
            {isNew ? "NOWA" : "PRZECZYTANA"}
          </Label>
        </TableCell>

        <TableCell>
          <InputBase value={fDate(row.createdAt)} sx={{ width: 1 }} />
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
        <MenuItem onClick={handleRead} sx={{ mr: 1 }}>
          <Iconify icon="carbon:view" sx={{ mr: 0.5 }} />
          <Typography variant="body2">Przeczytaj</Typography>
        </MenuItem>

        {isInbox && (
          <MenuItem onClick={handleAdd} sx={{ mr: 1, color: "success.main" }}>
            <Iconify icon="carbon:mail-reply" sx={{ mr: 0.5 }} />
            <Typography variant="body2">Odpowiedz</Typography>
          </MenuItem>
        )}
      </Popover>
    </>
  );
}
