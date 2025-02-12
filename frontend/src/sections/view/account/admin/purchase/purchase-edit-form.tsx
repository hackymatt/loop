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

import { GITHUB_REPO } from "src/config-global";
import { useLesson, useEditLesson } from "src/api/lessons/lesson";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { ICourseLessonProp, ICourseByTechnologyProps } from "src/types/course";

import { usePurchaseFields } from "./purchase-fields";
import { steps, schema, defaultValues } from "./purchase";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  lesson: ICourseLessonProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function LessonEditForm({ lesson, onClose, ...other }: Props) {
  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
    page_size: -1,
  });

  const { data: lessonData } = useLesson(lesson.id);
  const { mutateAsync: editLesson } = useEditLesson(lesson.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = methods;

  useEffect(() => {
    if (lessonData && availableTechnologies) {
      reset({
        ...lessonData,
        github_url: lessonData.githubUrl.replace(GITHUB_REPO, ""),
        technologies: lessonData.technologies.map((t: ICourseByTechnologyProps) =>
          availableTechnologies.find(
            (technology: ICourseByTechnologyProps) => technology.name === t.name,
          ),
        ),
      });
    }
  }, [availableTechnologies, lessonData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editLesson({
        ...data,
        technologies: (data.technologies ?? []).map(
          (technology: ICourseByTechnologyProps) => technology.id,
        ),
        github_url: `${GITHUB_REPO}${data.github_url}`,
      });
      reset();
      onCloseWithReset();
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = usePurchaseFields();

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
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj lekcję</DialogTitle>
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
                Zapisz
              </LoadingButton>
            </>
          )}
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
