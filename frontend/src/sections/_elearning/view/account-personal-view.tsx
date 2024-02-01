"use client";

import * as Yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, Controller } from "react-hook-form";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";

import { countries } from "src/assets/data";

import FormProvider, { RHFSelect, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

// ----------------------------------------------------------------------

const GENDER_OPTIONS = ["Male", "Female", "Other"];

// ----------------------------------------------------------------------

export default function AccountPersonalView() {
  const EcommerceAccountPersonalSchema = Yup.object().shape({
    firstName: Yup.string().required("First name is required"),
    lastName: Yup.string().required("Last name is required"),
    emailAddress: Yup.string().required("Email address is required"),
    phoneNumber: Yup.string().required("Phone number is required"),
    birthday: Yup.mixed<any>().nullable().required("Birthday is required"),
    gender: Yup.string().required("Gender is required"),
    streetAddress: Yup.string().required("Street address is required"),
    city: Yup.string().required("City is required"),
    zipCode: Yup.string().required("Zip code is required"),
  });

  const defaultValues = {
    firstName: "Jayvion",
    lastName: "Simon",
    emailAddress: "nannie_abernathy70@yahoo.com",
    phoneNumber: "365-374-4961",
    birthday: null,
    gender: "Male",
    streetAddress: "",
    zipCode: "",
    city: "",
    country: "United States",
  };

  const methods = useForm({
    resolver: yupResolver(EcommerceAccountPersonalSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const onSubmit = handleSubmit(async (data) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      reset();
      console.log("DATA", data);
    } catch (error) {
      console.error(error);
    }
  });

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Personal
      </Typography>

      <Box
        rowGap={2.5}
        columnGap={2}
        display="grid"
        gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
        sx={{ my: 5 }}
      >
        <RHFTextField name="firstName" label="First Name" />

        <RHFTextField name="lastName" label="Last Name" />

        <RHFTextField name="emailAddress" label="Email Address" />

        <RHFTextField name="phoneNumber" label="Phone Number" />

        <Controller
          name="birthday"
          render={({ field, fieldState: { error } }) => (
            <DatePicker
              label="Birthday"
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

        <RHFSelect native name="gender" label="Gender">
          {GENDER_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </RHFSelect>

        <RHFTextField name="streetAddress" label="Street Address" />

        <RHFTextField name="zipCode" label="Zip Code" />

        <RHFTextField name="city" label="City" />

        <RHFAutocomplete
          name="country"
          type="country"
          label="Country"
          placeholder="Choose a country"
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
        Save Changes
      </LoadingButton>
    </FormProvider>
  );
}
