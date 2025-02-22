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

import { UserType } from "src/consts/user-type";
import { useCreateUser } from "src/api/users/users";

import FormProvider from "src/components/hook-form";
import { useToastContext } from "src/components/toast";

import { IUserType } from "src/types/user";
import { IGender } from "src/types/testimonial";

import { useUserFields } from "./user-fields";
import { schema, defaultValues } from "./user";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function UserNewForm({ onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: createUser } = useCreateUser();

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
    reset({ ...defaultValues, dob: new Date() });
  }, [reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      delete data.image;
      await createUser({
        ...data,
        user_type: data.user_type as IUserType,
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
      enqueueSnackbar("Płatność została dodana", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useUserFields();

  const {
    field: { value: userType },
  } = useController({ name: "user_type", control });

  const isTeacher = useMemo(() => userType === UserType.Teacher, [userType]);

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
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj użytkownika</DialogTitle>
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
