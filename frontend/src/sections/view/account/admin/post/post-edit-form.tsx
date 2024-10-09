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

import { GITHUB_REPO } from "src/config-global";
import { usePost, useEditPost } from "src/api/posts/post";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { ICoursePostProp, ICourseByCategoryProps } from "src/types/course";

import { usePostFields } from "./post-fields";
import { steps, schema, defaultValues } from "./post";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  post: ICoursePostProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PostEditForm({ post, onClose, ...other }: Props) {
  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
  });

  const { data: postData } = usePost(post.id);
  const { mutateAsync: editPost } = useEditPost(post.id);

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
    if (postData && availableTechnologies) {
      reset({
        ...postData,
        github_url: postData.githubUrl.replace(GITHUB_REPO, ""),
        technologies: postData.category.map((category: string) =>
          availableTechnologies.find(
            (technology: ICourseByCategoryProps) => technology.name === category,
          ),
        ),
      });
    }
  }, [availableTechnologies, postData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editPost({
        ...data,
        technologies: data.technologies.map((technology: ICourseByCategoryProps) => technology.id),
        github_url: `${GITHUB_REPO}${data.github_url}`,
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = usePostFields();

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
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
