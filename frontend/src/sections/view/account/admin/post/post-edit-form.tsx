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
import { usePost, useEditPost } from "src/api/posts/post";
import { useLecturers } from "src/api/lecturers/lecturers";
import { usePostCategories } from "src/api/post-categories/post-categories";

import FormProvider from "src/components/hook-form";
import { isStepFailed } from "src/components/stepper/step";

import { ITagProps } from "src/types/tags";
import { IAuthorProps } from "src/types/author";
import { ITeamMemberProps } from "src/types/team";
import { IPostProps, IPostCategoryProps } from "src/types/blog";

import { usePostFields } from "./post-fields";
import { steps, schema, defaultValues } from "./post";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  post: IPostProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PostEditForm({ post, onClose, ...other }: Props) {
  const { data: availableCategories } = usePostCategories({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableLecturers } = useLecturers({
    sort_by: "full_name",
    page_size: -1,
  });
  const { data: availableTags } = useTags({
    sort_by: "name",
    page_size: -1,
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
    if (postData && availableTags && availableCategories && availableLecturers) {
      reset({
        ...postData,
        category: [availableCategories.find((c: IPostCategoryProps) => c.name === post.category)],
        authors: postData.authors.map((author: IAuthorProps) =>
          availableLecturers.find((lecturer: ITeamMemberProps) => lecturer.id === author.id),
        ),
        tags: postData.tags.map((tag: string) =>
          availableTags.find((s: ITagProps) => s.name === tag),
        ),
        image: postData.coverUrl ?? "",
      });
    }
  }, [availableCategories, availableLecturers, availableTags, post.category, postData, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onCloseWithReset = useCallback(() => {
    onClose();
    setActiveStep(0);
  }, [onClose]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editPost({
        ...data,
        authors: data.authors.map((author: IAuthorProps) => author.id),
        category: data.category.map((c: IPostCategoryProps) => c.id)[0],
        tags: data.tags.map((tag: ITagProps) => tag.id),
        image: (await urlToBlob(data.image)) as string,
      });
      reset();
      onCloseWithReset();
    } catch (error) {
      handleFormError(error);
    }
  });

  const [activeStep, setActiveStep] = useState(0);

  const { fields } = usePostFields();

  const stepContent = steps[activeStep].fields.map((field: string) => fields[field]);

  return (
    <Dialog fullWidth maxWidth="lg" onClose={onCloseWithReset} sx={{ zIndex: 1 }} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj artykuł</DialogTitle>
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
