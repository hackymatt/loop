import { useEffect } from "react";
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

import { useOthers } from "src/api/others/others";
import { usePayments } from "src/api/payment/payments";
import { useServices } from "src/api/services/services";
import { useServicePurchase, useEditServicePurchase } from "src/api/purchases/services-purchase";

import FormProvider from "src/components/hook-form";

import { IPaymentProp } from "src/types/payment";
import { IServiceProp } from "src/types/service";
import { ITeamMemberProps } from "src/types/team";
import { IPurchaseItemProp } from "src/types/purchase";

import { schema, defaultValues } from "./purchase";
import { usePurchaseFields } from "./purchase-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PurchaseEditForm({ purchase, onClose, ...other }: Props) {
  const { data: availableServices } = useServices({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableOthers } = useOthers({
    sort_by: "full_name",
    page_size: -1,
  });

  const { data: availablePayments } = usePayments({
    sort_by: "session_id",
    page_size: -1,
  });
  const { data: purchaseData } = useServicePurchase(purchase.id);
  const { mutateAsync: editPurchase } = useEditServicePurchase(purchase.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (purchaseData && availableServices && availableOthers && availablePayments) {
      reset({
        ...purchaseData,
        price: purchaseData.lessonPrice,
        service: [availableServices.find((s: IServiceProp) => s.id === purchaseData.lessonId)],
        other: [availableOthers.find((o: ITeamMemberProps) => o.id === purchaseData.teacher!.id)],
        payment: [
          availablePayments.find((p: IPaymentProp) => p.sessionId === purchaseData.paymentId),
        ],
      });
    }
  }, [availableOthers, availablePayments, availableServices, purchaseData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editPurchase({
        ...data,
        service: data.service.map((s: IServiceProp) => s.id)[0],
        other: data.other.map((o: ITeamMemberProps) => o.id)[0],
        payment: data.payment.map((p: IPaymentProp) => p.id)[0]!,
      });
      reset();
      onClose();
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
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj zakup</DialogTitle>
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
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
