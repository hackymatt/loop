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

import { urlToBlob } from "src/utils/blob-to-base64";

import { useTags } from "src/api/tags/tags";
import { useTopics } from "src/api/topics/topics";
import { useModules } from "src/api/modules/modules";
import { useCandidates } from "src/api/candidates/candidates";
import { useCourse, useEditCourse } from "src/api/courses/course";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { ITagProps } from "src/types/tags";
import { ITopicProps } from "src/types/topic";
import { IModuleProps } from "src/types/module";
import { ICandidateProps } from "src/types/candidate";
import { ILevel, ICourseProps, ICourseModuleProp } from "src/types/course";

import { useCourseFields } from "./course-fields";
import { steps, schema, defaultValues } from "./course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  course: ICourseProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CourseEditForm({ course, onClose, ...other }: Props) {
  const { data: availableModules } = useModules({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableTags } = useTags({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableTopics } = useTopics({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableCandidates } = useCandidates({
    sort_by: "name",
    page_size: -1,
  });

  const { data: courseData } = useCourse(course.id);
  const { mutateAsync: editCourse } = useEditCourse(course.id);

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
    if (courseData && availableTags && availableCandidates && availableTopics && availableModules) {
      reset({
        ...courseData,
        title: courseData.slug,
        tags: courseData.tags.map((tag: string) =>
          availableTags.find((s: ITagProps) => s.name === tag),
        ),
        topics: courseData.learnList.map((topic: string) =>
          availableTopics.find((t: ITopicProps) => t.name === topic),
        ),
        candidates: courseData.candidateList.map((candidate: string) =>
          availableCandidates.find((c: ICandidateProps) => c.name === candidate),
        ),
        modules: courseData.modules.map((module: ICourseModuleProp) => {
          const moduleData = availableModules.find((m: IModuleProps) => m.id === module.id);

          if (!moduleData) {
            return moduleData;
          }

          return {
            ...moduleData,
          };
        }),
        image: courseData.coverUrl ?? "",
        video: courseData.video ?? "",
      });
    }
  }, [availableCandidates, availableModules, availableTags, availableTopics, courseData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editCourse({
        ...data,
        modules: data.modules.map((module: IModuleProps) => module.id),
        tags: data.tags.map((tag: ITagProps) => tag.id),
        topics: data.topics.map((topic: ITopicProps) => topic.id),
        candidates: data.candidates.map((candidate: ICandidateProps) => candidate.id),
        level: data.level.slice(0, 1) as ILevel,
        image: (await urlToBlob(data.image)) as string,
        video: data.video ? ((await urlToBlob(data.video)) as string) : "",
      });
      reset();
      onCloseWithReset();
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
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj kurs</DialogTitle>
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
