"use client";

import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { yupResolver } from "@hookform/resolvers/yup";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function ForgotPasswordView() {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const ForgotPasswordSchema = Yup.object().shape({
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
  });

  const { resetUserPassword } = useUserContext();

  const defaultValues = {
    email: "",
  };

  const methods = useForm({
    resolver: yupResolver(ForgotPasswordSchema),
    defaultValues,
  });

  const {
    handleSubmit,
    formState: { isSubmitting },
    clearErrors,
    reset,
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await resetUserPassword(data);
      push(paths.login);
      enqueueSnackbar("Wysłano tymczasowe hasło", { variant: "success" });
      reset();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Stack sx={{ textAlign: "center" }}>
      <Image
        alt="reset password"
        src="/assets/icons/ic_lock_password.svg"
        sx={{ mb: 5, width: 96, height: 96, mx: "auto" }}
      />

      <Typography variant="h3" paragraph>
        Nie pamiętasz hasła?
      </Typography>

      <Typography variant="body2" sx={{ color: "text.secondary", mb: 5 }}>
        Podaj adres e-mail powiązany z Twoim kontem, a my wyślemy Ci Twoje tymczasowe hasło.
      </Typography>

      <FormProvider methods={methods} onSubmit={onSubmit}>
        <RHFTextField name="email" hiddenLabel placeholder="Adres e-mail" />

        <LoadingButton
          fullWidth
          size="large"
          color="inherit"
          type="submit"
          variant="contained"
          loading={isSubmitting}
          sx={{ mt: 2.5 }}
        >
          Resetuj hasło
        </LoadingButton>
      </FormProvider>

      <Link
        component={RouterLink}
        href={paths.login}
        color="inherit"
        variant="subtitle2"
        sx={{
          mt: 3,
          mx: "auto",
          alignItems: "center",
          display: "inline-flex",
        }}
      >
        <Iconify icon="carbon:chevron-left" width={16} sx={{ mr: 1 }} />
        Wróć do logowania
      </Link>
    </Stack>
  );
}
