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

import { useCandidate, useEditCandidate } from "src/api/candidates/candidate";

import FormProvider from "src/components/hook-form";

import { ICourseByCandidateProps } from "src/types/course";

import { schema, defaultValues } from "./candidate";
import { useCandidateFields } from "./candidate-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  candidate: ICourseByCandidateProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CandidateEditForm({ candidate, onClose, ...other }: Props) {
  const { data: candidateData } = useCandidate(candidate.id);
  const { mutateAsync: editCandidate } = useEditCandidate(candidate.id);

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
    if (candidateData) {
      reset(candidateData);
    }
  }, [reset, candidateData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editCandidate(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useCandidateFields();

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj kandydata</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>{fields.name}</Stack>
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
