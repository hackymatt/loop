"use client";

import * as Yup from "yup";
import { AxiosError } from "axios";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";
import { yupResolver } from "@hookform/resolvers/yup";
import { useRef, useMemo, useEffect, useCallback } from "react";

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
import { useQueryParams } from "src/hooks/use-query-params";
import { useFormErrorHandler } from "src/hooks/use-form-error-handler";
import { useGoogleAuth, useGithubAuth, useFacebookAuth } from "src/hooks/use-social-auth";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFCheckbox, RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function RegisterView() {
  const { enqueueSnackbar } = useToastContext();
  const { getQueryParams } = useQueryParams();

  const { push } = useRouter();

  const passwordShow = useBoolean();

  const { authUrl: googleAuthUrl } = useGoogleAuth();
  const { authUrl: facebookAuthUrl } = useFacebookAuth();
  const { authUrl: githubAuthUrl } = useGithubAuth();

  const queryParams = useMemo(() => getQueryParams(), [getQueryParams]);

  const {
    registerUser,
    loginGoogleUser,
    loginFacebookUser,
    loginGithubUser,
    isRegistered,
    isLoggedIn,
  } = useUserContext();

  const RegisterSchema = Yup.object().shape({
    first_name: Yup.string().required("Imię jest wymagane"),
    last_name: Yup.string().required("Nazwisko jest wymagane"),
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
    password: Yup.string()
      .required("Hasło jest wymagane")
      .min(8, "Hasło musi mieć minimum 8 znaków")
      .matches(/^(?=.*[A-Z])/, "Hasło musi składać się z minimum jednej dużej litery.")
      .matches(/^(?=.*[a-z])/, "Hasło musi składać się z minimum jednej małej litery.")
      .matches(/^(?=.*[0-9])/, "Hasło musi składać się z minimum jednej cyfry")
      .matches(/^(?=.*[!@#$%^&])/, "Hasło musi składać się z minimum jednego znaku specjalnego"),
    password2: Yup.string()
      .required("Hasło jest wymagane")
      .oneOf([Yup.ref("password")], "Hasła nie są takie same"),
    acceptance: Yup.boolean()
      .required("To pole jest wymagane")
      .oneOf([true], "To pole jest wymagane"),
    newsletter: Yup.boolean().required("To pole jest wymagane"),
  });

  const defaultValues = {
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password2: "",
    acceptance: false,
    newsletter: false,
  };

  const methods = useForm({
    resolver: yupResolver(RegisterSchema),
    defaultValues,
  });

  const {
    handleSubmit,
    formState: { isSubmitting },
    clearErrors,
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onEmailSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await registerUser(data);
      enqueueSnackbar("Zarejestrowano pomyślnie", { variant: "success" });
    } catch (error) {
      handleFormError(error);
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
    if (isRegistered) {
      push(paths.verify);
    }
  }, [isRegistered, push]);

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
        Rejestracja
      </Typography>

      <Typography variant="body2" sx={{ color: "text.secondary" }}>
        Masz już konto?{" "}
        <Link component={RouterLink} href={paths.login} variant="subtitle2" color="primary">
          Zaloguj się
        </Link>
      </Typography>
    </div>
  );

  const renderSocials = (
    <Stack direction="row" spacing={2}>
      <Button
        component={RouterLink}
        href={googleAuthUrl}
        fullWidth
        size="large"
        color="inherit"
        variant="outlined"
      >
        <Iconify icon="logos:google-icon" width={24} />
      </Button>

      <Button
        component={RouterLink}
        href={facebookAuthUrl}
        fullWidth
        size="large"
        color="inherit"
        variant="outlined"
      >
        <Iconify icon="carbon:logo-facebook" width={24} sx={{ color: "#1877F2" }} />
      </Button>

      <Button
        component={RouterLink}
        href={githubAuthUrl}
        color="inherit"
        fullWidth
        variant="outlined"
        size="large"
      >
        <Iconify icon="carbon:logo-github" width={24} sx={{ color: "text.primary" }} />
      </Button>
    </Stack>
  );

  const renderForm = (
    <FormProvider methods={methods} onSubmit={onEmailSubmit}>
      <Stack spacing={2.5}>
        <RHFTextField name="first_name" label="Imię" />

        <RHFTextField name="last_name" label="Nazwisko" />

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

        <RHFTextField
          name="password2"
          label="Powtórz hasło"
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

        <Stack spacing={0.5}>
          <RHFCheckbox
            name="acceptance"
            label={
              <Typography variant="caption" align="left" sx={{ color: "text.secondary" }}>
                Akceptuję{" "}
                <Link
                  target="_blank"
                  rel="noopener"
                  href={paths.termsAndConditions}
                  color="text.primary"
                  underline="always"
                >
                  regulamin
                </Link>{" "}
                i{" "}
                <Link
                  target="_blank"
                  rel="noopener"
                  href={paths.privacyPolicy}
                  color="text.primary"
                  underline="always"
                >
                  politykę prywatności.
                </Link>
              </Typography>
            }
          />

          <RHFCheckbox
            name="newsletter"
            label={
              <Typography variant="caption" align="left" sx={{ color: "text.secondary" }}>
                Chcę otrzymywać newsletter, informacje o promocjach i produktach dostępnych w loop.
              </Typography>
            }
          />
        </Stack>

        <LoadingButton
          fullWidth
          color="inherit"
          size="large"
          type="submit"
          variant="contained"
          loading={isSubmitting}
        >
          Zarejestruj się
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
