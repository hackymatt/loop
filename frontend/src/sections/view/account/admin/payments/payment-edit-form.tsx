import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import { Alert } from "@mui/material";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { usePayment, useEditPayment } from "src/api/payment/payment";

import FormProvider from "src/components/hook-form";

import {
  IPaymentProp,
  IPaymentStatus,
  IPaymentMethodProp,
  IPaymentCurrencyProp,
} from "src/types/payment";

import { schema, defaultValues } from "./payment";
import { usePaymentFields } from "./payment-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  payment: IPaymentProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PaymentEditForm({ payment, onClose, ...other }: Props) {
  const { data: paymentData } = usePayment(payment.id!);
  const { mutateAsync: editPayment } = useEditPayment(payment.id!);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    control,
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = methods;

  useEffect(() => {
    if (paymentData) {
      reset(paymentData);
    }
  }, [reset, paymentData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editPayment({
        ...data,
        amount: data.amount * 100,
        currency: data.currency as IPaymentCurrencyProp,
        method: data.method as IPaymentMethodProp,
        status: data.status as IPaymentStatus,
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = usePaymentFields(control);

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
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj płatność</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.amount}
            {fields.currency}
            {fields.method}
            {fields.status}
            {fields.notes}
            {errors.root && <Alert severity="error">{errors.root.message}</Alert>}
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

          <LoadingButton
            color="inherit"
            type="submit"
            variant="contained"
            loading={isSubmitting}
            disabled={!!errors.root}
          >
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
