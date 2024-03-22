import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useDeleteReview } from "src/api/reviews/review";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { IPurchaseItemProp } from "src/types/purchase";

import { schema, defaultValues } from "./review";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function ReviewDeleteForm({ purchase, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: deleteReview } = useDeleteReview(purchase.reviewId);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    handleSubmit,
    reset,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (purchase) {
      reset({ rating: purchase.ratingNumber, review: purchase.review });
    }
  }, [purchase, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await deleteReview({});
      reset();
      onClose();
      enqueueSnackbar("Recenzja została usunięta", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Usuń recenzję</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Typography>Czy na pewno chcesz usunąć recenzję?</Typography>
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
