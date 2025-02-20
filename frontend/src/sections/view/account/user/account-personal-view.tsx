"use client";

import * as Yup from "yup";
import { useEffect } from "react";
import { parseISO } from "date-fns";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, Controller } from "react-hook-form";

import Box from "@mui/material/Box";
import { alpha } from "@mui/material";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

import { Gender } from "src/consts/gender";
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

const GENDER_OPTIONS = Object.values(Gender).map((gender: IGender) => ({
  label: gender,
  value: gender,
}));

const DEFAULT_COUNTRY = "Polska";

// ----------------------------------------------------------------------

export default function AccountPersonalView() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updateUserDetails } = useUpdateUserDetails();

  const userSchemaObject = {
    firstName: Yup.string().required("Imię jest wymagane"),
    lastName: Yup.string().required("Nazwisko jest wymagane"),
    email: Yup.string().required("Adres email jest wymagany"),
    phoneNumber: Yup.string().nullable(),
    dob: Yup.mixed<any>().nullable(),
    gender: Yup.string().required("Płeć jest wymagana"),
    streetAddress: Yup.string().nullable(),
    zipCode: Yup.string().nullable(),
    city: Yup.string().nullable(),
    country: Yup.string().required("Państwo jest wymagane"),
    image: Yup.string().nullable(),
  };

  const AccountPersonalSchema = Yup.object().shape(userSchemaObject);

  const defaultValues = {
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    dob: null,
    gender: Gender.Other,
    streetAddress: "",
    zipCode: "",
    city: "",
    country: DEFAULT_COUNTRY,
    image: "",
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
        phoneNumber: userDetails.phoneNumber ?? "",
        streetAddress: userDetails.streetAddress ?? "",
        zipCode: userDetails.zipCode ?? "",
        city: userDetails.city ?? "",
        country: userDetails.country ?? DEFAULT_COUNTRY,
        dob: userDetails.dob ? parseISO(userDetails.dob) : null,
      });
    }
  }, [reset, userDetails]);

  const onSubmit = handleSubmit(async (data) => {
    const {
      firstName,
      lastName,
      dob,
      gender,
      phoneNumber,
      streetAddress,
      zipCode,
      city,
      country,
      image,
      ...rest
    } = data;
    try {
      await updateUserDetails({
        ...rest,
        first_name: firstName,
        last_name: lastName,
        dob: dob ? fDate(dob, "yyyy-MM-dd") : null,
        gender,
        phone_number: phoneNumber ?? null,
        street_address: streetAddress ?? null,
        zip_code: zipCode ?? null,
        city: city ?? null,
        country: country ?? null,
        image: image ?? "",
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
        <RHFTextField name="firstName" label="Imię" />

        <RHFTextField name="lastName" label="Nazwisko" />

        <RHFTextField name="email" label="Adres e-mail" disabled />

        <RHFTextField name="phoneNumber" label="Numer telefonu" />

        <Controller
          name="dob"
          render={({ field, fieldState: { error } }) => (
            <DatePicker
              label="Data urodzenia"
              localeText={{
                toolbarTitle: "Wybierz datę",
                cancelButtonLabel: "Anuluj",
              }}
              slotProps={{
                field: { clearable: true, onClear: () => field.onChange("") },
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
