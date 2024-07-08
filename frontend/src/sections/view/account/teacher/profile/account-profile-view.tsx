"use client";

import * as Yup from "yup";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import { InputAdornment } from "@mui/material";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useUserFinanceDetail, useEditUserFinanceDetail } from "src/api/finance/finance";

import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function AccountProfileView() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userFinanceDetails } = useUserFinanceDetail();
  const { mutateAsync: updateUserFinanceDetails } = useEditUserFinanceDetail();

  const schema = Yup.object().shape({
    account: Yup.string().nullable().length(26, "Numer konta musi mieć 26 znaków"),
    rate: Yup.number().nullable().min(0, "Stawka musi wynosić min 0 zł"),
    commission: Yup.number()
      .nullable()
      .min(0, "Prowizja musi wynosić min 0 %")
      .max(100, "Prowizja musi wynosić max 100 %"),
  });

  const defaultValues = userFinanceDetails;

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  useEffect(() => {
    if (userFinanceDetails) {
      reset(userFinanceDetails);
    }
  }, [reset, userFinanceDetails]);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await updateUserFinanceDetails(data);
      enqueueSnackbar("Dane finansowe zostały zmienione", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Profil instruktora
      </Typography>

      <Box
        rowGap={2.5}
        columnGap={2}
        display="grid"
        gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
        sx={{ mt: 5 }}
      >
        <RHFTextField name="user_title" label="Tytuł zawodowy" />

        <RHFTextField
          name="linkedin_url"
          label="Profil linkedin"
          InputProps={{
            startAdornment: <InputAdornment position="start">www.linkedin.com/in/</InputAdornment>,
          }}
          InputLabelProps={{ shrink: true }}
        />
      </Box>
      <Box sx={{ my: 2.5 }}>
        <RHFTextField name="description" label="Opis" multiline rows={20} fullWidth />
      </Box>

      <LoadingButton
        color="inherit"
        size="large"
        type="submit"
        variant="contained"
        loading={isSubmitting}
      >
        Zapisz
      </LoadingButton>
    </FormProvider>
  );
}
