"use client";

import * as Yup from "yup";
import { AxiosError } from "axios";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { yupResolver } from "@hookform/resolvers/yup";
import { useRef, useMemo, useEffect, useCallback } from "react";

import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";
import InputAdornment from "@mui/material/InputAdornment";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useBoolean } from "src/hooks/use-boolean";
import { useQueryParams } from "src/hooks/use-query-params";
import { useFormErrorHandler } from "src/hooks/use-form-error-handler";
import { useGoogleAuth, useGithubAuth, useFacebookAuth } from "src/hooks/use-social-auth";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function LoginView() {
  const { enqueueSnackbar } = useToastContext();
  const { getQueryParams } = useQueryParams();

  const { push } = useRouter();

  const passwordShow = useBoolean();

  const { authUrl: googleAuthUrl } = useGoogleAuth();
  const { authUrl: facebookAuthUrl } = useFacebookAuth();
  const { authUrl: githubAuthUrl } = useGithubAuth();

  const queryParams = useMemo(() => getQueryParams(), [getQueryParams]);

  const {
    loginUser,
    loginGoogleUser,
    loginFacebookUser,
    loginGithubUser,
    isRegistered,
    isUnverified,
    isLoggedIn,
  } = useUserContext();

  const LoginSchema = Yup.object().shape({
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
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

  const onEmailSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await loginUser(data);
      enqueueSnackbar("Zalogowano pomyślnie", { variant: "success" });
    } catch (error) {
      if ((error as AxiosError).response?.status !== 403) {
        handleFormError(error);
      } else {
        enqueueSnackbar("Wystąpił błąd podczas logowania", { variant: "error" });
      }
    }
  });

  const onGoogleSubmit = useCallback(async () => {
    clearErrors();
    try {
      const { code } = queryParams;
      await loginGoogleUser({ code });
      enqueueSnackbar("Zalogowano pomyślnie", { variant: "success" });
    } catch (error) {
      if ((error as AxiosError).response?.status !== 403) {
        handleFormError(error);
      } else {
        enqueueSnackbar("Wystąpił błąd podczas logowania", { variant: "error" });
      }
    }
  }, [clearErrors, enqueueSnackbar, handleFormError, loginGoogleUser, queryParams]);

  const onFacebookSubmit = useCallback(async () => {
    clearErrors();
    try {
      const { code } = queryParams;
      await loginFacebookUser({ code });
      enqueueSnackbar("Zalogowano pomyślnie", { variant: "success" });
    } catch (error) {
      if ((error as AxiosError).response?.status !== 403) {
        handleFormError(error);
      } else {
        enqueueSnackbar("Wystąpił błąd podczas logowania", { variant: "error" });
      }
    }
  }, [clearErrors, enqueueSnackbar, handleFormError, loginFacebookUser, queryParams]);

  const onGithubSubmit = useCallback(async () => {
    clearErrors();
    try {
      const { code } = queryParams;
      await loginGithubUser({ code });
      enqueueSnackbar("Zalogowano pomyślnie", { variant: "success" });
    } catch (error) {
      if ((error as AxiosError).response?.status !== 403) {
        handleFormError(error);
      } else {
        enqueueSnackbar("Wystąpił błąd podczas logowania", { variant: "error" });
      }
    }
  }, [clearErrors, enqueueSnackbar, handleFormError, loginGithubUser, queryParams]);

  useEffect(() => {
    if (isRegistered && isUnverified) {
      push(paths.verify);
    }
  }, [isRegistered, isUnverified, push]);

  useEffect(() => {
    if (isLoggedIn) {
      push(paths.account.personal);
    }
  }, [isLoggedIn, push]);

  const effectRan = useRef(false);
  useEffect(() => {
    const { type } = queryParams;
    if (type) {
      if (!effectRan.current) {
        switch (type) {
          case "google":
            onGoogleSubmit();
            break;
          case "facebook":
            onFacebookSubmit();
            break;
          case "github":
            onGithubSubmit();
            break;
          default:
            break;
        }
        effectRan.current = true;
      }
    }
  }, [onGoogleSubmit, onFacebookSubmit, queryParams, onGithubSubmit]);

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
    <Stack direction="row" justifyContent="center" spacing={5}>
      <IconButton href={googleAuthUrl}>
        <Iconify icon="logos:google-icon" width={20} />
      </IconButton>

      <IconButton href={facebookAuthUrl}>
        <Iconify icon="carbon:logo-facebook" width={24} sx={{ color: "#1877F2" }} />
      </IconButton>

      <IconButton href={githubAuthUrl}>
        <Iconify icon="carbon:logo-github" width={24} sx={{ color: "text.primary" }} />
      </IconButton>
    </Stack>
  );

  const renderForm = (
    <FormProvider methods={methods} onSubmit={onEmailSubmit}>
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
