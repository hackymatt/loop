import { useForm } from "react-hook-form";

import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useDeleteCoupon } from "src/api/coupons/coupon";

import FormProvider from "src/components/hook-form";

import { ICouponProps } from "src/types/coupon";

import { defaultValues } from "./coupon";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  coupon: ICouponProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CouponDeleteForm({ coupon, onClose, ...other }: Props) {
  const { mutateAsync: deleteCoupon } = useDeleteCoupon();

  const methods = useForm({
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async () => {
    try {
      await deleteCoupon({ id: coupon.id });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

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
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Usuń kupon</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Typography>{`Czy na pewno chcesz usunąć kupon ${coupon.code}?`}</Typography>
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

          <LoadingButton color="error" type="submit" variant="contained" loading={isSubmitting}>
            Usuń
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
