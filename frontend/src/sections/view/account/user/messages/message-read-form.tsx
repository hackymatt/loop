import { useEffect } from "react";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { TextField } from "@mui/material";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useMessage, useEditMessage } from "src/api/message/message";

import { useToastContext } from "src/components/toast";

import { IMessageProp, MessageStatus, MessageType } from "src/types/message";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  message: IMessageProp;
  type: MessageType;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function MessageReadForm({ message, type, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { data: messageData } = useMessage(message.id);
  const { mutateAsync: editMessage } = useEditMessage(message.id);

  useEffect(() => {
    const handleEdit = async () => {
      try {
        await editMessage({
          ...messageData,
          status: MessageStatus.READ,
        });
      } catch {
        enqueueSnackbar("Wystąpił błąd", { variant: "error" });
      }
    };
    if (type === MessageType.INBOX) {
      handleEdit();
    }
  }, [editMessage, enqueueSnackbar, messageData, type]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <DialogTitle
        sx={{ typography: "h3", pb: 3 }}
      >{`Wiadomość od ${message.sender.name}`}</DialogTitle>

      <DialogContent sx={{ py: 0 }}>
        <Stack spacing={1}>
          <TextField label="Tytuł" value={message.subject} />
          <TextField label="Wiadomość" rows={3} multiline value={message.body} />
        </Stack>
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>
      </DialogActions>
    </Dialog>
  );
}
