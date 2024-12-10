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

import { useCreateTechnology } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { schema, defaultValues } from "./technology";
import { useTechnologyFields } from "./technology-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TechnologyNewForm({ onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createTechnology } = useCreateTechnology();

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
      await createTechnology(data);
      reset();
      onClose();
      enqueueSnackbar("Technologia została dodana", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useTechnologyFields();

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj nową technologię</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.name}
            {fields.description}
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
