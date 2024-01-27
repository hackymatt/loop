"use client";

import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import FormProvider, { RHFCode } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function VerifyView({ email }: { email?: string }) {
  const VerifySchema = Yup.object().shape({
    code: Yup.string()
      .min(8, "Kod weryfikacyjny musi mieć 8 znaków")
      .required("Kod weryfikacyjny jest wymagany"),
  });

  const defaultValues = {
    email: email ?? "",
    code: "",
  };

  const methods = useForm({
    mode: "onChange",
    resolver: yupResolver(VerifySchema),
    defaultValues,
  });

  const {
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const onSubmit = handleSubmit(async (data) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      console.log("DATA", data);
    } catch (error) {
      console.error(error);
    }
  });

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

      <Typography variant="body2" align="center" sx={{ mt: 3 }}>
        Kod nie dotarł?{" "}
        <Link variant="subtitle2" underline="none">
          Wyślij kod ponownie
        </Link>
      </Typography>

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
        Wróć do strony logowania
      </Link>
    </Stack>
  );
}
