import { useForm } from "react-hook-form";
import { useState, useCallback } from "react";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import { Step, Stepper, StepLabel, StepContent } from "@mui/material";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useCreateCourse } from "src/api/courses/courses";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";
import { isStepFailed } from "src/components/stepper/step";

import { ITagProps } from "src/types/tags";
import {
  ILevel,
  ICourseModuleProp,
  ICourseByTopicProps,
  ICourseByCandidateProps,
} from "src/types/course";

import { useCourseFields } from "./course-fields";
import { steps, schema, defaultValues } from "./course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CourseNewForm({ onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
  });

  const { mutateAsync: createCourse } = useCreateCourse();

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      if (availableTechnologies) {
        await createCourse({
          ...data,
          level: data.level.slice(0, 1) as ILevel,
          modules: data.modules.map((module: ICourseModuleProp) => module.id),
          tags: data.tags.map((tag: ITagProps) => tag.id),
          topics: data.topics.map((topic: ICourseByTopicProps) => topic.id),
          candidates: data.candidates.map((candidate: ICourseByCandidateProps) => candidate.id),
        });
      }
      reset();
      onCloseWithReset();
      enqueueSnackbar("Kurs został dodany", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = useCourseFields();

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onCloseWithReset}
      {...other}
      sx={{
        zIndex: (theme) => theme.zIndex.modal + 1,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj nowy kurs</DialogTitle>
          {fields.active}
        </Stack>

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
                Dodaj
              </LoadingButton>
            </>
          )}
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
