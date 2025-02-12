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

import { useCreatePurchase } from "src/api/purchases/services-purchases";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { IServiceProp } from "src/types/service";
import { IPaymentProp } from "src/types/payment";
import { IUserDetailsProps } from "src/types/user";

import { schema, defaultValues } from "./purchase";
import { usePurchaseFields } from "./purchase-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PurchaseNewForm({ onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createPurchase } = useCreatePurchase();

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
      await createPurchase({
        ...data,
        service: data.service.map((s: IServiceProp) => s.id)[0],
        other: data.other.map((o: IUserDetailsProps) => o.id)[0],
        payment: data.payment.map((p: IPaymentProp) => p.id)[0]!,
      });
      reset();
      onClose();
      enqueueSnackbar("Zakup został dodany", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = usePurchaseFields();

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
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj nowy zakup</DialogTitle>
          {fields.active}
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.service}
            {fields.price}
            {fields.other}
            {fields.payment}
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
