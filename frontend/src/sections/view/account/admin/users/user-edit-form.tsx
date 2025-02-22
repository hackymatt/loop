import * as Yup from "yup";
import { useEffect } from "react";
import { parseISO } from "date-fns";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

import { UserType } from "src/consts/user-type";
import { useUser, useEditUser } from "src/api/users/user";

import FormProvider from "src/components/hook-form";

import { IUserDetailsProps } from "src/types/user";

import { useUserFields } from "./user-fields";
import { schema, defaultValues, DEFAULT_COUNTRY } from "./user";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  user: IUserDetailsProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function UserEditForm({ user, onClose, ...other }: Props) {
  const { data: userData } = useUser(user.id);
  const { mutateAsync: editUser } = useEditUser(user.id);

  const methods = useForm({
    resolver: yupResolver(schema.shape({ userType: Yup.string().required("Typ jest wymagany") })),
    defaultValues: { ...defaultValues, userType: UserType.Student },
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (userData) {
      const { phoneNumber, streetAddress, zipCode, city, country, dob, userType, ...rest } =
        userData;
      reset({
        ...rest,
        phoneNumber: phoneNumber ?? "",
        streetAddress: streetAddress ?? "",
        zipCode: zipCode ?? "",
        city: city ?? "",
        country: country ?? DEFAULT_COUNTRY,
        dob: dob ? parseISO(dob) : null,
        userType: userType ?? UserType.Student,
      });
    }
  }, [reset, userData]);

  const handleFormError = useFormErrorHandler(methods, {
    first_name: "firstName",
    last_name: "lastName",
    phone_number: "phoneNumber",
    street_address: "streetAddress",
    zip_code: "zipCode",
    user_type: "userType",
  });

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
      userType,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      image: _,
      ...rest
    } = data;
    try {
      await editUser({
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
        user_type: userType,
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useUserFields();

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onClose}
      {...other}
      sx={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj użytkownika</DialogTitle>
          {fields.image}
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.userType}
            {fields.firstName}
            {fields.lastName}
            {fields.email}
            {fields.gender}
            {fields.dob}
            {fields.phoneNumber}
            {fields.streetAddress}
            {fields.zipCode}
            {fields.city}
            {fields.country}
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

          <LoadingButton color="inherit" type="submit" variant="contained" loading={isSubmitting}>
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
