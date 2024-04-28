import { useForm } from "react-hook-form";

import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import FormProvider from "src/components/hook-form";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function AccountDeleteForm({ onClose, ...other }: Props) {
  const { unregisterUser } = useUserContext();
  const { enqueueSnackbar } = useToastContext();

  const methods = useForm();

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const onSubmit = handleSubmit(async () => {
    try {
      await unregisterUser();
      reset();
      onClose();
      enqueueSnackbar("Pomyślnie usunięto konto", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd", { variant: "error" });
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Usuń konto</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Typography>Czy na pewno chcesz usunąć swoje konto oraz wszystkie dane?</Typography>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="error" type="submit" variant="contained" loading={isSubmitting}>
            Usuń
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
