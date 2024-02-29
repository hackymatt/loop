import { useMemo, useEffect } from "react";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, useController } from "react-hook-form";

import { Box } from "@mui/material";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";
import { urlToBlob } from "src/utils/blob-to-base64";

import { useUser, useEditUser } from "src/api/users/user";

import FormProvider from "src/components/hook-form";

import { IGender } from "src/types/testimonial";
import { UserType, IUserType, IUserDetailsProps } from "src/types/user";

import { useUserFields } from "./user-fields";
import { schema, defaultValues } from "./user";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  user: IUserDetailsProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function UserEditForm({ user, onClose, ...other }: Props) {
  const { data: userData } = useUser(user.id!);
  const { mutateAsync: editUser } = useEditUser(user.id!);

  const date18YearsAgo = useMemo(() => new Date().setFullYear(new Date().getFullYear() - 18), []);

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
    if (userData) {
      reset({
        ...userData,
        dob: userData?.dob ? new Date(userData?.dob) : date18YearsAgo,
        gender: userData?.gender !== null ? userData.gender : "Mężczyzna",
      });
    }
  }, [userData, reset, date18YearsAgo]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editUser({
        ...data,
        phone_number: data.phone_number ?? "",
        dob: fDate(data.dob, "yyyy-MM-dd") ?? "",
        gender: data.gender as IGender,
        user_type: data.user_type as IUserType,
        street_address: data.street_address ?? "",
        zip_code: data.zip_code ?? "",
        city: data.city ?? "",
        country: data.country ?? "",
        image: (await urlToBlob(data.image ?? "")) as string,
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useUserFields();

  // const {
  //   field: { value: userType },
  // } = useController({ name: "user_type", control });

  const isTeacher = useMemo(() => user.user_type === UserType.Wykładowca, [user.user_type]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj użytkownika</DialogTitle>
          <Box sx={{ p: 3 }}>{fields.image}</Box>
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.user_type}
            {fields.first_name}
            {fields.last_name}
            {fields.email}
            {fields.gender}
            {isTeacher && fields.user_title}
            {isTeacher && fields.rate}
            {isTeacher && fields.commission}
            {fields.phone_number}
            {fields.dob}
            {fields.street_address}
            {fields.zip_code}
            {fields.city}
            {fields.country}
          </Stack>
        </DialogContent>

        <DialogActions>
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
