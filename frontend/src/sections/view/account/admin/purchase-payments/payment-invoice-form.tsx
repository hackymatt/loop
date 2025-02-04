import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useState, useEffect, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import { Step, Stepper, StepLabel, StepContent } from "@mui/material";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useInvoice, useCreateInvoice } from "src/api/purchase/invoice";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { IPaymentItemProp } from "src/types/purchase";
import { IInvoicePaymentMethod, IInvoicePaymentStatus } from "src/types/invoice";

import { useInvoiceFields } from "./invoice-fields";
import { steps, schema, defaultValues } from "./invoice";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  payment: IPaymentItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PaymentInvoiceForm({ payment, onClose, ...other }: Props) {
  const { data: invoiceData } = useInvoice(payment.id);
  const { mutateAsync: createInvoice } = useCreateInvoice();

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
    if (invoiceData) {
      reset(invoiceData);
    }
  }, [reset, invoiceData]);

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      const {
        name: full_name,
        streetAddress: street_address,
        zipCode: zip_code,
        ...customerData
      } = data.customer;
      const { status, method, ...paymentData } = data.payment;
      await createInvoice({
        ...data,
        customer: { ...customerData, full_name, street_address, zip_code },
        payment: {
          ...paymentData,
          status: status as IInvoicePaymentStatus,
          method: method as IInvoicePaymentMethod,
        },
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = useInvoiceFields(control);

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

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
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Wygeneruj fakturę</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            <Stepper activeStep={activeStep} orientation="vertical">
              {steps.map((step, index) => {
                const labelProps: {
                  optional?: React.ReactNode;
                  error?: boolean;
                } = {};
                labelProps.error = isStepFailed(steps[index].fields, errors);

                return (
                  <Step key={step.label}>
                    <StepLabel {...labelProps}>{step.label}</StepLabel>
                    <StepContent>
                      <Stack spacing={1}>{stepContent}</Stack>
                    </StepContent>
                  </Step>
                );
              })}
            </Stepper>
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
          {activeStep === 0 && (
            <>
              <Button variant="outlined" onClick={onCloseWithReset} color="inherit">
                Anuluj
              </Button>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(activeStep + 1)}
                color="success"
              >
                Dalej
              </Button>
            </>
          )}
          {activeStep > 0 && activeStep < steps.length - 1 && (
            <>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(activeStep - 1)}
                color="inherit"
              >
                Wstecz
              </Button>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(activeStep + 1)}
                color="success"
              >
                Dalej
              </Button>
            </>
          )}
          {activeStep === steps.length - 1 && (
            <>
              <Button
                variant="outlined"
                onClick={() => setActiveStep(activeStep - 1)}
                color="inherit"
              >
                Wstecz
              </Button>
              <LoadingButton
                color="success"
                type="submit"
                variant="contained"
                loading={isSubmitting}
              >
                Wygeneruj
              </LoadingButton>
            </>
          )}
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
