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
import { useCourse, useEditCourse } from "src/api/courses/course";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { ITagProps } from "src/types/tags";
import { ILevel, ICourseProps, ICourseModuleProp, ICourseByTopicProps } from "src/types/course";

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
    if (courseData && availableTags && availableTopics && availableModules) {
      reset({
        ...courseData,
        title: courseData.slug,
        tags: courseData.tags.map((tag: string) =>
          availableTags.find((s: ITagProps) => s.name === tag),
        ),
        topics: courseData.learnList.map((topic: string) =>
          availableTopics.find((t: ICourseByTopicProps) => t.name === topic),
        ),
        modules: courseData.modules.map((module: ICourseModuleProp) => {
          const moduleData = availableModules.find((m: ICourseModuleProp) => m.id === module.id);

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
  }, [availableModules, availableTags, availableTopics, courseData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editCourse({
        ...data,
        modules: data.modules.map((module: ICourseModuleProp) => module.id),
        tags: data.tags.map((tag: ITagProps) => tag.id),
        topics: data.topics.map((topic: ICourseByTopicProps) => topic.id),
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
    <Dialog fullWidth maxWidth="sm" onClose={onCloseWithReset} {...other}>
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
