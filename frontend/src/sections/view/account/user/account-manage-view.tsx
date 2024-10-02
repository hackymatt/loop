"use client";

import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import { Button, Divider } from "@mui/material";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import LoadingButton from "@mui/lab/LoadingButton";
import InputAdornment from "@mui/material/InputAdornment";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks/use-router";

import { useBoolean } from "src/hooks/use-boolean";
import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { MIN_PASSWORD_LENGTH } from "src/config-global";
import { usePasswordChange } from "src/api/auth/password-change";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

import { UserType } from "src/types/user";

import AccountDeleteForm from "./account-delete-form";

// ----------------------------------------------------------------------

export default function AccountManageView() {
  const { enqueueSnackbar } = useToastContext();
  const { push } = useRouter();
  const { logoutUser, userType } = useUserContext();

  const passwordShow = useBoolean();
  const deleteAccountFormOpen = useBoolean();

  const { mutateAsync: changePassword } = usePasswordChange();

  const ChangePasswordSchema = Yup.object().shape({
    old_password: Yup.string().required("Hasło jest wymagane"),
    password: Yup.string()
      .required("Hasło jest wymagane")
      .min(MIN_PASSWORD_LENGTH, `Hasło musi mieć minimum ${MIN_PASSWORD_LENGTH} znaków`)
      .matches(/^(?=.*[A-Z])/, "Hasło musi składać się z minimum jednej dużej litery.")
      .matches(/^(?=.*[a-z])/, "Hasło musi składać się z minimum jednej małej litery.")
      .matches(/^(?=.*[0-9])/, "Hasło musi składać się z minimum jednej cyfry")
      .matches(/^(?=.*[!@#$%^&])/, "Hasło musi składać się z minimum jednego znaku specjalnego"),
    password2: Yup.string()
      .required("Hasło jest wymagane")
      .oneOf([Yup.ref("password")], "Hasła nie są takie same"),
  });

  const defaultValues = {
    old_password: "",
    password: "",
    password2: "",
  };

  const methods = useForm({
    resolver: yupResolver(ChangePasswordSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await changePassword(data);
      reset();
      await logoutUser({});
      push(paths.login);
      enqueueSnackbar("Hasło zostało zmienione. Zaloguj się ponownie.", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Typography variant="h5" sx={{ mb: 3 }}>
          Zarządzaj kontem
        </Typography>

        <Stack spacing={3} sx={{ my: 5 }}>
          <Stack spacing={2.5}>
            <RHFTextField
              name="old_password"
              label="Obecne hasło"
              type={passwordShow.value ? "text" : "password"}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={passwordShow.onToggle} edge="end">
                      <Iconify icon={passwordShow.value ? "carbon:view" : "carbon:view-off"} />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <RHFTextField
              name="password"
              label="Nowe hasło"
              type={passwordShow.value ? "text" : "password"}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={passwordShow.onToggle} edge="end">
                      <Iconify icon={passwordShow.value ? "carbon:view" : "carbon:view-off"} />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <RHFTextField
              name="password2"
              label="Potwierdź nowe hasło"
              type={passwordShow.value ? "text" : "password"}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton onClick={passwordShow.onToggle} edge="end">
                      <Iconify icon={passwordShow.value ? "carbon:view" : "carbon:view-off"} />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Stack>
        </Stack>

        <LoadingButton
          color="inherit"
          size="large"
          type="submit"
          variant="contained"
          loading={isSubmitting}
        >
          Zapisz
        </LoadingButton>

        <Divider sx={{ borderStyle: "dashed", mt: 2, mb: 2 }} />

        <Button
          color="error"
          size="medium"
          variant="contained"
          onClick={deleteAccountFormOpen.onToggle}
          disabled={userType === UserType.Admin}
        >
          Usuń konto
        </Button>
      </FormProvider>
      <AccountDeleteForm
        open={deleteAccountFormOpen.value}
        onClose={deleteAccountFormOpen.onFalse}
      />
    </>
  );
}
