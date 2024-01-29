"use client";

import * as Yup from "yup";
import { AxiosError } from "axios";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { yupResolver } from "@hookform/resolvers/yup";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import InputAdornment from "@mui/material/InputAdornment";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useBoolean } from "src/hooks/use-boolean";
import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function LoginView() {
  const { enqueueSnackbar } = useToastContext();

  const { push } = useRouter();

  const passwordShow = useBoolean();

  const { loginUser, isUnverified, isLoggedIn } = useUserContext();

  const LoginSchema = Yup.object().shape({
    email: Yup.string().required("Adres email jest wymagany").email("Podaj poprawny adres e-mail"),
    password: Yup.string().required("Hasło jest wymagane"),
  });

  const defaultValues = {
    email: "",
    password: "",
  };

  const methods = useForm({
    resolver: yupResolver(LoginSchema),
    defaultValues,
  });

  const {
    handleSubmit,
    formState: { isSubmitting, errors },
    clearErrors,
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await loginUser(data);
      enqueueSnackbar("Zalogowano pomyślnie", { variant: "success" });
    } catch (error) {
      if ((error as AxiosError).response?.status !== 403) {
        handleFormError(error);
      }
    }
  });

  if (isUnverified) {
    push(paths.verify);
  }

  if (isLoggedIn) {
    push(paths.account.personal);
  }

  const renderHead = (
    <div>
      <Typography variant="h3" paragraph>
        Logowanie
      </Typography>

      <Typography variant="body2" sx={{ color: "text.secondary" }}>
        Nie masz jeszcze konta?{" "}
        <Link component={RouterLink} href={paths.register} variant="subtitle2" color="primary">
          Zarejestruj się
        </Link>
      </Typography>
    </div>
  );

  const renderSocials = (
    <Stack direction="row" spacing={2}>
      <Button fullWidth size="large" color="inherit" variant="outlined">
        <Iconify icon="logos:google-icon" width={24} />
      </Button>

      <Button fullWidth size="large" color="inherit" variant="outlined">
        <Iconify icon="carbon:logo-facebook" width={24} sx={{ color: "#1877F2" }} />
      </Button>

      <Button color="inherit" fullWidth variant="outlined" size="large">
        <Iconify icon="carbon:logo-github" width={24} sx={{ color: "text.primary" }} />
      </Button>
    </Stack>
  );

  const renderForm = (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Stack spacing={2.5} alignItems="flex-end">
        <RHFTextField name="email" label="Adres e-mail" />

        <RHFTextField
          name="password"
          label="Hasło"
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

        {errors.root && (
          <Typography variant="body2" color="error" sx={{ width: 1 }}>
            {errors.root.message}
          </Typography>
        )}

        <Link
          component={RouterLink}
          href={paths.forgotPassword}
          variant="body2"
          underline="always"
          color="text.secondary"
        >
          Nie pamiętasz hasła?
        </Link>

        <LoadingButton
          fullWidth
          color="inherit"
          size="large"
          type="submit"
          variant="contained"
          loading={isSubmitting}
        >
          Zaloguj się
        </LoadingButton>
      </Stack>
    </FormProvider>
  );

  return (
    <>
      {renderHead}

      {renderForm}

      <Divider>
        <Typography variant="body2" sx={{ color: "text.disabled" }}>
          lub
        </Typography>
      </Divider>

      {renderSocials}
    </>
  );
}
