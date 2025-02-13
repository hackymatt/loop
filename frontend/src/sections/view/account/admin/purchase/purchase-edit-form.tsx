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
import { usePurchase } from "src/api/purchases/services-purchases";
import { IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function PurchaseEditForm({ purchase, onClose, ...other }: Props) {
  const { data: availableTechnologies } = useTechnologies({
    sort_by: "name",
    page_size: -1,
  });

  const { data: purchaseData } = usePurchase(purchase.id);
  const { mutateAsync: editPurchase } = useEditLesson(lesson.id);

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
    if (purchaseData && availableTechnologies) {
      reset({
        ...purchaseData,
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

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editLesson(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = usePurchaseFields();

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onClose}
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
            {fields.service}
            {fields.price}
            {fields.other}
            {fields.payment}
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
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>
          <LoadingButton color="success" type="submit" variant="contained" loading={isSubmitting}>
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
