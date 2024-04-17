import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
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

import { urlToBlob } from "src/utils/blob-to-base64";

import { useSkills } from "src/api/skills/skills";
import { useTopics } from "src/api/topics/topics";
import { useLessons } from "src/api/lessons/lessons";
import { useCourse, useEditCourse } from "src/api/courses/course";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import {
  ILevel,
  ICourseProps,
  ICourseLessonProp,
  ICourseBySkillProps,
  ICourseByTopicProps,
  ICourseByCategoryProps,
} from "src/types/course";

import { useCourseFields } from "./coupon-fields";
import { steps, schema, defaultValues } from "./coupon";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  course: ICourseProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CourseEditForm({ course, onClose, ...other }: Props) {
  const { data: availableLessons } = useLessons({
    sort_by: "title",
  });
  const { data: availableSkills } = useSkills({
    sort_by: "name",
  });
  const { data: availableTopics } = useTopics({
    sort_by: "name",
  });
  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
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
    if (courseData) {
      reset({
        ...courseData,
        title: courseData.slug,
        skills: courseData.skills.map((skill: string) =>
          availableSkills.find((s: ICourseBySkillProps) => s.name === skill),
        ),
        topics: courseData.learnList.map((topic: string) =>
          availableTopics.find((t: ICourseByTopicProps) => t.name === topic),
        ),
        lessons: courseData.lessons.map((lesson: ICourseLessonProp) => {
          const lessonData = availableLessons.find((l: ICourseLessonProp) => l.id === lesson.id);

          if (!lessonData) {
            return lessonData;
          }

          return {
            ...lessonData,
            github_url: lessonData.githubUrl,
            technologies: lessonData.category.map((category: string) =>
              availableTechnologies.find(
                (technology: ICourseByCategoryProps) => technology.name === category,
              ),
            ),
          };
        }),
        image: courseData.coverUrl ?? "",
        video: courseData.video ?? "",
      });
    }
  }, [
    availableLessons,
    availableSkills,
    availableTechnologies,
    availableTopics,
    courseData,
    reset,
  ]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editCourse({
        ...data,
        lessons: data.lessons.map((lesson: ICourseLessonProp) => lesson.id),
        skills: data.skills.map((skill: ICourseBySkillProps) => skill.id),
        topics: data.topics.map((topic: ICourseByTopicProps) => topic.id),
        level: data.level.slice(0, 1) as ILevel,
        image: (await urlToBlob(data.image)) as string,
        video: data.video ? ((await urlToBlob(data.video)) as string) : "",
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = useCourseFields();

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
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
              <Button variant="outlined" onClick={onClose} color="inherit">
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
