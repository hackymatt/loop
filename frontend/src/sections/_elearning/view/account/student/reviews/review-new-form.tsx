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

import { useCreateReview } from "src/api/reviews/reviews";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { IPurchaseItemProp } from "src/types/purchase";

import { schema, defaultValues } from "./review";
import { useReviewFields } from "./review-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function ReviewNewForm({ purchase, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createReview } = useCreateReview();

  const constValues = {
    lesson: purchase.id,
    lecturer: purchase.teacher.id,
  };

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    handleSubmit,
    reset,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await createReview({ ...data, ...constValues });
      reset();
      onClose();
      enqueueSnackbar("Recenzja została dodana", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useReviewFields();

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Nowa recenzja</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={2.5}>
            {fields.rating}
            {fields.review}
          </Stack>
        </DialogContent>

        <DialogActions>
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
