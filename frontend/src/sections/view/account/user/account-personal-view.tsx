"use client";

import * as Yup from "yup";
import { useEffect } from "react";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, Controller } from "react-hook-form";

import Box from "@mui/material/Box";
import { alpha } from "@mui/material";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

import { countries } from "src/assets/data";
import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import { useToastContext } from "src/components/toast";
import FormProvider, {
  RHFSelect,
  RHFTextField,
  RHFAutocompleteCountry,
} from "src/components/hook-form";

import AccountImage from "src/sections/account/account-image";

import { IGender } from "src/types/testimonial";

// ----------------------------------------------------------------------

const GENDER_OPTIONS = [
  { label: "Mężczyzna", value: "Mężczyzna" },
  { label: "Kobieta", value: "Kobieta" },
  { label: "Inne", value: "Inne" },
];

// ----------------------------------------------------------------------

export default function AccountPersonalView() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updateUserDetails } = useUpdateUserDetails();

  const userSchemaObject = {
    first_name: Yup.string().required("Imię jest wymagane"),
    last_name: Yup.string().required("Nazwisko jest wymagane"),
    email: Yup.string().required("Adres email jest wymagany"),
    phone_number: Yup.string().nullable(),
    dob: Yup.mixed<any>().nullable(),
    gender: Yup.string().required("Płeć jest wymagana"),
    street_address: Yup.string().nullable(),
    zip_code: Yup.string().nullable(),
    city: Yup.string().nullable(),
    country: Yup.string().required("Państwo jest wymagane"),
    image: Yup.string().nullable(),
  };

  const AccountPersonalSchema = Yup.object().shape(userSchemaObject);

  const defaultValues = {
    ...userDetails,
    first_name: userDetails?.first_name ?? "",
    last_name: userDetails?.last_name ?? "",
    phone_number: userDetails?.phone_number ?? "",
    street_address: userDetails?.street_address ?? "",
    zip_code: userDetails?.zip_code ?? "",
    city: userDetails?.city ?? "",
    country: userDetails?.country ?? "",
    dob: userDetails?.dob ? new Date(userDetails?.dob) : undefined,
    gender: userDetails?.gender ? userDetails.gender : "Mężczyzna",
  };

  const methods = useForm({
    resolver: yupResolver(AccountPersonalSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  useEffect(() => {
    if (userDetails) {
      reset({
        ...userDetails,
        first_name: userDetails?.first_name ?? "",
        last_name: userDetails?.last_name ?? "",
        phone_number: userDetails?.phone_number ?? "",
        street_address: userDetails?.street_address ?? "",
        zip_code: userDetails?.zip_code ?? "",
        city: userDetails?.city ?? "",
        country: userDetails?.country ?? "",
        dob: userDetails?.dob ? new Date(userDetails?.dob) : undefined,
        gender: userDetails?.gender !== null ? userDetails.gender : "Mężczyzna",
      });
    }
  }, [reset, userDetails]);

  const onSubmit = handleSubmit(async (data) => {
    delete data.image;
    const { phone_number, dob, gender, street_address, zip_code, city } = data;
    try {
      await updateUserDetails({
        ...data,
        phone_number: phone_number ?? "",
        dob: fDate(dob, "yyyy-MM-dd") ?? "",
        gender: (gender as IGender) ?? "",
        street_address: street_address ?? "",
        zip_code: zip_code ?? "",
        city: city ?? "",
      });
      enqueueSnackbar("Dane zostały zmienione", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Dane osobowe
      </Typography>

      <Box
        sx={{
          p: 3,
          mt: 3,
          borderRadius: 2,
          display: { xs: "flex", md: "none" },
          border: (theme) => `solid 1px ${alpha(theme.palette.grey[500], 0.24)}`,
        }}
      >
        <AccountImage />
      </Box>

      <Box
        rowGap={2.5}
        columnGap={2}
        display="grid"
        gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
        sx={{ my: 5 }}
      >
        <RHFTextField name="first_name" label="Imię" />

        <RHFTextField name="last_name" label="Nazwisko" />

        <RHFTextField name="email" label="Adres e-mail" disabled />

        <RHFTextField name="phone_number" label="Numer telefonu" />

        <Controller
          name="dob"
          render={({ field, fieldState: { error } }) => (
            <DatePicker
              label="Data urodzenia"
              slotProps={{
                textField: {
                  helperText: error?.message,
                  error: !!error?.message,
                },
              }}
              {...field}
              value={field.value}
            />
          )}
        />

        <RHFSelect name="gender" label="Płeć" options={GENDER_OPTIONS} placeholder="Wybierz płeć" />

        <RHFTextField name="street_address" label="Ulica, numer budynku, numer lokalu" />

        <RHFTextField name="zip_code" label="Kod pocztowy" />

        <RHFTextField name="city" label="Miasto" />

        <RHFAutocompleteCountry
          name="country"
          label="Państwo"
          placeholder="Wybierz państwo"
          fullWidth
          options={countries.map((option) => option.label)}
          getOptionLabel={(option) => option}
        />
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
