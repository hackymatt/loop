import { useForm } from "react-hook-form";

import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useCreateTeaching } from "src/api/teaching/teachings";

import FormProvider from "src/components/hook-form";

import { ITeachingProp } from "src/types/course";

import { defaultValues } from "./teaching";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  teaching: ITeachingProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TeachingAddForm({ teaching, onClose, ...other }: Props) {
  const { mutateAsync: createTeaching } = useCreateTeaching();

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
      await createTeaching({ lesson: teaching.id });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Zacznij prowadzić lekcję</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Typography>{`Czy na pewno chcesz zacząć prowadzić lekcję ${teaching.title}?`}</Typography>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="success" type="submit" variant="contained" loading={isSubmitting}>
            Zacznij
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
