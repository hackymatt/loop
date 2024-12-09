import * as Yup from "yup";
import { m } from "framer-motion";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { Stack, InputAdornment } from "@mui/material";
import { LoadingButton, LoadingButtonProps } from "@mui/lab";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { trackEvents } from "src/utils/track-events";

import { textGradient } from "src/theme/css";
import { newsletterAcceptance } from "src/consts/acceptances";
import { useRegisterNewsletter } from "src/api/newsletter/register";

import { useToastContext } from "src/components/toast";
import FormProvider, { RHFCheckbox, RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function Newsletter() {
  return (
    <Box
      component="section"
      sx={{
        overflow: "hidden",
        position: "relative",
        bgcolor: "common.black",
        py: { xs: 10, md: 15 },
      }}
    >
      <Box
        sx={{
          top: 0,
          left: 0,
          bottom: 0,
          my: "auto",
          width: 760,
          height: 760,
          opacity: 0.24,
          position: "absolute",
          transform: "translateX(-50%)",
        }}
      >
        <Box
          component={m.img}
          animate={{ rotate: 360 }}
          transition={{ duration: 60, ease: "linear", repeat: Infinity }}
          alt="Texture"
          loading="lazy"
          src="/assets/background/texture-3.webp"
        />
      </Box>

      <Container>
        <Box
          sx={{
            mx: "auto",
            maxWidth: 480,
            textAlign: "center",
            color: "common.white",
          }}
        >
          <Box gap={2} display="flex" alignItems="center" justifyContent="center">
            <Box component="span" sx={{ textAlign: "right", typography: "h4" }}>
              Zarejestruj się już teraz i otrzymaj <br /> zniżkę na swój pierwszy zakup
            </Box>
            <Typography
              variant="h2"
              sx={(theme) => ({
                ...textGradient(
                  `90deg, ${theme.palette.primary.main} 20%, ${theme.palette.secondary.main} 100%`,
                ),
              })}
            >
              20%
            </Typography>
          </Box>

          <Typography sx={{ mt: 3, opacity: 0.64 }}>Zapisz się do newslettera</Typography>
          <Typography
            variant="h3"
            sx={(theme) => ({
              ...textGradient(
                `90deg, ${theme.palette.primary.main} 20%, ${theme.palette.secondary.main} 100%`,
              ),
              mb: 5,
            })}
          >
            Be in the loop
          </Typography>

          <NewsletterEmail buttonLabel="Zapisz" bgColor="common.white" />
        </Box>
      </Container>
    </Box>
  );
}

interface Props extends LoadingButtonProps {
  buttonLabel: string;
  showSnackbar?: boolean;
  onSuccess?: VoidFunction;
  onFailure?: VoidFunction;
  bgColor?: string;
}

export function NewsletterEmail({
  buttonLabel = "Zapisz",
  showSnackbar = true,
  onSuccess,
  onFailure,
  bgColor,
}: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: register } = useRegisterNewsletter();

  const NewsletterSchema = Yup.object().shape({
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
    newsletter: Yup.boolean()
      .required("To pole jest wymagane")
      .oneOf([true], "To pole jest wymagane"),
  });

  const defaultValues = {
    email: "",
    newsletter: false,
  };

  const methods = useForm({
    resolver: yupResolver(NewsletterSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
    clearErrors,
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    clearErrors();
    try {
      await register({ email: data.email });
      if (showSnackbar) {
        enqueueSnackbar("Zapisano do newslettera", { variant: "success" });
      }
      onSuccess?.();
      reset();
      trackEvents("enroll_to_newsletter", "newsletter", "Enrolled to newsletter", data.email);
    } catch (error) {
      onFailure?.();
      handleFormError(error);
    }
  });

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <RHFTextField
        name="email"
        label="Wpisz swój adres e-mail"
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <LoadingButton
                color="primary"
                size="large"
                variant="contained"
                type="submit"
                loading={isSubmitting}
              >
                {buttonLabel}
              </LoadingButton>
            </InputAdornment>
          ),
          sx: {
            pr: 0.5,
            pl: 1.5,
            height: 56,
            borderRadius: 1,
            ...(bgColor && {
              bgcolor: bgColor,
              "&:hover": {
                bgcolor: bgColor,
              },
              "&.Mui-focused": {
                bgcolor: bgColor,
              },
              "&.Mui-error": {
                bgcolor: bgColor,
              },
              "&.Mui-focused.Mui-error": {
                bgcolor: bgColor,
              },
            }),
          },
        }}
      />

      <Stack spacing={0.5} alignItems="flex-start">
        <RHFCheckbox
          name="newsletter"
          label={newsletterAcceptance({
            color: bgColor || undefined,
            opacity: bgColor ? 0.64 : 1,
          })}
        />
      </Stack>
    </FormProvider>
  );
}
