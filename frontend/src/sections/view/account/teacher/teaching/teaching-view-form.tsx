import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useState, useEffect, useCallback } from "react";

import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import { Step, Stack, Stepper, StepLabel, StepContent } from "@mui/material";

import { useLesson } from "src/api/lessons/lesson";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";

import { ITeachingProp } from "src/types/teaching";
import { ITechnologyProps } from "src/types/technology";
import { ICourseByTechnologyProps } from "src/types/course";

import { useTeachingFields } from "./teaching-fields";
import { steps, schema, defaultValues } from "./teaching";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  teaching: ITeachingProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TeachingViewForm({ teaching, onClose, ...other }: Props) {
  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
    page_size: -1,
  });

  const { data: lessonData } = useLesson(teaching.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const { reset } = methods;

  useEffect(() => {
    if (lessonData && availableTechnologies) {
      reset({
        ...lessonData,
        github_url: lessonData.githubUrl,
        technologies: lessonData.technologies.map((t: ICourseByTechnologyProps) =>
          availableTechnologies.find((technology: ITechnologyProps) => technology.name === t.name),
        ),
      });
    }
  }, [availableTechnologies, lessonData, reset]);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = useTeachingFields();

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onCloseWithReset} {...other}>
      <FormProvider methods={methods}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Szczegóły lekcji</DialogTitle>
          {fields.active}
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            <Stepper activeStep={activeStep} orientation="vertical">
              {steps.map((step, index) => (
                <Step key={step.label}>
                  <StepLabel>{step.label}</StepLabel>
                  <StepContent>
                    <Stack spacing={1}>{stepContent}</Stack>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </Stack>
        </DialogContent>

        <DialogActions>
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
              <Button variant="outlined" onClick={onCloseWithReset} color="success">
                Zamknij
              </Button>
            </>
          )}
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
