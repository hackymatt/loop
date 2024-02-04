"use client";

import * as Yup from "yup";
import { useEffect } from "react";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, Controller } from "react-hook-form";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

import { countries } from "src/assets/data";
import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import FormProvider, { RHFSelect, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { IGender } from "src/types/testimonial";

// ----------------------------------------------------------------------

const GENDER_OPTIONS = [
  { label: "Mężczyzna", value: "Mężczyzna" },
  { label: "Kobieta", value: "Kobieta" },
  { label: "Inne", value: "Inne" },
];

// ----------------------------------------------------------------------

export default function AccountPersonalView() {
  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updateUserDetails } = useUpdateUserDetails();

  const AccountPersonalSchema = Yup.object().shape({
    firstName: Yup.string().required("Imię jest wymagane"),
    lastName: Yup.string().required("Nazwisko jest wymagane"),
    emailAddress: Yup.string().required("Adres email jest wymagany"),
    phoneNumber: Yup.string().nullable(),
    birthday: Yup.mixed<any>().nullable(),
    gender: Yup.string().required("Płeć jest wymagana"),
    streetAddress: Yup.string().nullable(),
    zipCode: Yup.string().nullable(),
    city: Yup.string().nullable(),
    country: Yup.string().required("Państwo jest wymagane"),
    photo: Yup.string().nullable(),
  });

  const defaultValues = { ...userDetails, birthday: new Date(userDetails?.birthday) };

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
      reset({ ...userDetails, birthday: new Date(userDetails?.birthday) });
    }
  }, [reset, userDetails]);

  const onSubmit = handleSubmit(async (data) => {
    const {
      firstName,
      lastName,
      emailAddress,
      phoneNumber,
      birthday,
      gender,
      streetAddress,
      zipCode,
      city,
      country,
      photo,
    } = data;
    try {
      await updateUserDetails({
        first_name: firstName,
        last_name: lastName,
        email: emailAddress,
        phone_number: phoneNumber ?? "",
        dob: fDate(birthday, "yyyy-MM-dd") ?? "",
        gender: (gender as IGender) ?? "",
        street_address: streetAddress ?? "",
        zip_code: zipCode ?? "",
        city: city ?? "",
        country,
        image: photo ?? "",
      });
      reset();
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
        rowGap={2.5}
        columnGap={2}
        display="grid"
        gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
        sx={{ my: 5 }}
      >
        <RHFTextField name="firstName" label="Imię" />

        <RHFTextField name="lastName" label="Nazwisko" />

        <RHFTextField name="emailAddress" label="Adres e-mail" disabled />

        <RHFTextField name="phoneNumber" label="Numer telefonu" />

        <Controller
          name="birthday"
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

        <RHFTextField name="streetAddress" label="Ulica, numer budynku, numer lokalu" />

        <RHFTextField name="zipCode" label="Kod pocztowy" />

        <RHFTextField name="city" label="Miasto" />

        <RHFAutocomplete
          name="country"
          type="country"
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
