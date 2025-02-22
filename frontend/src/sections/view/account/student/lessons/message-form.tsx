import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDateTime } from "src/utils/format-time";

import { useCreateMessage } from "src/api/message/messages";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { UserType } from "src/consts/user-type";
import { MessageStatus } from "src/types/message";
import { IPurchaseItemProp } from "src/types/purchase";

import { schema, defaultValues } from "./message";
import { useMessageFields } from "./message-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function MessageForm({ purchase, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createMessage } = useCreateMessage();

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      ...defaultValues,
      subject: `Pytanie dotyczące lekcji ${purchase.lessonTitle} (${fDateTime(purchase.lessonSlot![0])})`,
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
        recipient_id: purchase.teacher!.id,
        recipient_type: UserType.Teacher,
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
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle
          sx={{ typography: "h3", pb: 3 }}
        >{`Nowa wiadomość do ${purchase.teacher!.name}`}</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.subject}
            {fields.body}
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
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
