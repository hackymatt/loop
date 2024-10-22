import { useMemo, useEffect } from "react";
import { yupResolver } from "@hookform/resolvers/yup";
import { useForm, useController } from "react-hook-form";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { fDate } from "src/utils/format-time";

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
  const { data: userData } = useUser(user.id);
  const { mutateAsync: editUser } = useEditUser(user.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
    control,
  } = methods;

  useEffect(() => {
    if (userData) {
      reset({ ...userData, dob: userData?.dob ? new Date(userData?.dob) : null });
    }
  }, [reset, userData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      delete data.image;
      await editUser({
        ...data,
        user_type: data.user_type as IUserType,
        rate: data.rate ?? 0,
        commission: data.commission ?? 0,
        dob: data.dob ? fDate(data.dob, "yyyy-MM-dd") : null,
        gender: data.gender as IGender,
        phone_number: data.phone_number ?? "",
        street_address: data.street_address ?? "",
        zip_code: data.zip_code ?? "",
        city: data.city ?? "",
        country: data.country ?? "",
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useUserFields();

  const {
    field: { value: userType },
  } = useController({ name: "user_type", control });

  const isTeacher = useMemo(() => userType === UserType.TEACHER, [userType]);

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj użytkownika</DialogTitle>
          {fields.image}
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.user_type}

            {isTeacher && fields.rate}
            {isTeacher && fields.commission}
            {isTeacher && fields.account}

            {fields.first_name}
            {fields.last_name}
            {fields.email}
            {fields.gender}
            {fields.dob}
            {fields.phone_number}
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
