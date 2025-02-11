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

import { useCreateService } from "src/api/services/services";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { schema, defaultValues } from "./service";
import { useServiceFields } from "./service-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function ServiceNewForm({ onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createService } = useCreateService();

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await createService(data);
      reset();
      onClose();
      enqueueSnackbar("Usługa została dodana", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useServiceFields();

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onClose}
      {...other}
      sx={{
        zIndex: (theme) => theme.zIndex.modal + 1,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj nową usługę</DialogTitle>
          {fields.active}
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.title}
            {fields.description}
            {fields.price}
          </Stack>
        </DialogContent>

        <DialogActions
          sx={{
            position: "fixed",
            bottom: 0,
            left: 0,
            right: 0,
            zIndex: (theme) => theme.zIndex.modal + 2,
            bgcolor: "background.paper",
            boxShadow: (theme) => theme.shadows[4],
            p: 2,
          }}
        >
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>
          <LoadingButton color="success" type="submit" variant="contained" loading={isSubmitting}>
            Dodaj
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
