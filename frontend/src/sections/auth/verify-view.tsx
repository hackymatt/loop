"use client";

import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { paths } from "src/routes/paths";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import Image from "src/components/image";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFCode } from "src/components/hook-form";

import NotFoundView from "../error/not-found-view";

// ----------------------------------------------------------------------

export default function VerifyView() {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const { email, verifyUser, resendVerificationCode, isUnverified, isLoading } = useUserContext();

  const VerifySchema = Yup.object().shape({
    code: Yup.string()
      .min(8, "Kod weryfikacyjny musi mieć 8 znaków")
      .required("Kod weryfikacyjny jest wymagany"),
  });

  const defaultValues = {
    code: "",
  };

  const methods = useForm({
    mode: "onChange",
    resolver: yupResolver(VerifySchema),
    defaultValues,
  });

  const {
    handleSubmit,
    reset,
    formState: { isSubmitting },
    clearErrors,
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await verifyUser({ email, code: data.code });
      enqueueSnackbar("Weryfikacja poprawna", { variant: "success" });
    } catch (error) {
      handleFormError(error);
    }
  });

  const onResendCode = async () => {
    clearErrors();
    try {
      await resendVerificationCode({ email });
      enqueueSnackbar("Wysłano kod weryfikacyjny ponownie", { variant: "success" });
      reset();
    } catch (error) {
      handleFormError(error);
    }
  };

  if (!email) {
    return <NotFoundView />;
  }

  if (!isUnverified) {
    push(paths.login);
  }

  return (
    <Stack sx={{ textAlign: "center" }}>
      <Image
        alt="email inbox"
        src="/assets/icons/ic_email_inbox.svg"
        sx={{ mb: 5, width: 96, height: 96, mx: "auto" }}
      />

      <Typography variant="h3">Sprawdź swoją skrzynkę mailową</Typography>

      <Typography variant="body2" sx={{ mt: 2, mb: 5, color: "text.secondary" }}>
        Wprowadź kod w poniższym polu, aby zweryfikować swój adres e-mail.
      </Typography>

      <FormProvider methods={methods} onSubmit={onSubmit}>
        <RHFCode name="code" />

        <LoadingButton
          fullWidth
          size="large"
          color="inherit"
          type="submit"
          variant="contained"
          loading={isSubmitting}
          sx={{ mt: 3 }}
        >
          Weryfikuj
        </LoadingButton>
      </FormProvider>

      <Stack direction="row" alignItems="center" justifyContent="center" sx={{ mt: 3 }}>
        <Typography variant="body2" align="center">
          Kod nie dotarł lub wygasł?
        </Typography>
        <LoadingButton variant="text" color="primary" onClick={onResendCode} loading={isLoading}>
          Wyślij kod ponownie
        </LoadingButton>
      </Stack>
    </Stack>
  );
}
