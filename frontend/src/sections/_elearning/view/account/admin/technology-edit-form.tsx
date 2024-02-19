import * as Yup from "yup";
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

import { useEditTechnology } from "src/api/technologies/technology";

import FormProvider, { RHFTextField } from "src/components/hook-form";

import { ICourseByCategoryProps } from "src/types/course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  technology: ICourseByCategoryProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TechnologyEditForm({ technology, onClose, ...other }: Props) {
  const { mutateAsync: editTechnology } = useEditTechnology(technology.id);

  const defaultValues = {
    name: "",
  };

  const EditTechnologySchema = Yup.object().shape({
    name: Yup.string().required("Nazwa jest wymagana"),
  });

  const methods = useForm({
    resolver: yupResolver(EditTechnologySchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (technology) {
      reset(technology);
    }
  }, [reset, technology]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editTechnology(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj technologię</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            <RHFTextField name="name" label="Nazwa" />
          </Stack>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="inherit" type="submit" variant="contained" loading={isSubmitting}>
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
