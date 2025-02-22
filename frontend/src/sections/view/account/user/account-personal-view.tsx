"use client";

import { useEffect } from "react";
import { parseISO } from "date-fns";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import { alpha } from "@mui/material";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

import { useUserDetails, useUpdateUserDetails } from "src/api/auth/details";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import AccountImage from "src/sections/account/account-image";

import { useUserFields } from "../admin/users/user-fields";
import { schema, defaultValues, DEFAULT_COUNTRY } from "../admin/users/user";

// ----------------------------------------------------------------------

export default function AccountPersonalView() {
  const { enqueueSnackbar } = useToastContext();

  const { data: userDetails } = useUserDetails();
  const { mutateAsync: updateUserDetails } = useUpdateUserDetails();

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods, {
    first_name: "firstName",
    last_name: "lastName",
    phone_number: "phoneNumber",
    street_address: "streetAddress",
    zip_code: "zipCode",
  });

  useEffect(() => {
    if (userDetails) {
      const { phoneNumber, streetAddress, zipCode, city, country, dob, ...rest } = userDetails;
      reset({
        ...rest,
        phoneNumber: phoneNumber ?? "",
        streetAddress: streetAddress ?? "",
        zipCode: zipCode ?? "",
        city: city ?? "",
        country: country ?? DEFAULT_COUNTRY,
        dob: dob ? parseISO(dob) : null,
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

  const { fields } = useUserFields();

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
        {fields.firstName}
        {fields.lastName}
        {fields.email}
        {fields.phoneNumber}
        {fields.dob}
        {fields.gender}
        {fields.streetAddress}
        {fields.zipCode}
        {fields.city}
        {fields.country}
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
