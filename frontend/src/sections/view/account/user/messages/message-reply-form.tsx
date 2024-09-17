import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useCreateMessage } from "src/api/message/messages";
import { useMessage, useEditMessage } from "src/api/message/message";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { IMessageProp, MessageStatus } from "src/types/message";

import { schema, defaultValues } from "./message";
import { useMessageFields } from "./message-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  message: IMessageProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function MessageReplyForm({ message, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();
  const [read, setRead] = useState<boolean>(false);

  const { mutateAsync: createMessage } = useCreateMessage();
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
    if (!read && message.status === MessageStatus.NEW && messageData) {
      handleEdit();
    }
    setRead(true);
  }, [editMessage, enqueueSnackbar, message.status, messageData, read]);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      ...defaultValues,
      subject: `Re: ${message.subject}`,
    },
  });

  const {
    handleSubmit,
    reset,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await createMessage({
        ...data,
        recipient_uuid: message.sender.id,
        status: MessageStatus.NEW,
      });
      reset();
      onClose();
      enqueueSnackbar("Wiadomość została wysłana", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useMessageFields();

  return (
    <Dialog
      fullWidth
      maxWidth="sm"
      onClose={() => {
        setRead(false);
        onClose();
      }}
      {...other}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle
          sx={{ typography: "h3", pb: 3 }}
        >{`Nowa wiadomość do ${message.sender.name}`}</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.subject}
            {fields.body}
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button
            variant="outlined"
            onClick={() => {
              setRead(false);
              onClose();
            }}
            color="inherit"
          >
            Anuluj
          </Button>

          <LoadingButton color="success" type="submit" variant="contained" loading={isSubmitting}>
            Wyślij
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
