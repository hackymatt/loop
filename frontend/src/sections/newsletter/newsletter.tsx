import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import { Link, Stack } from "@mui/material";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import { LoadingButton, LoadingButtonProps } from "@mui/lab";

import { paths } from "src/routes/paths";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useRegisterNewsletter } from "src/api/newsletter/register";

import Image from "src/components/image";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFCheckbox, RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function Newsletter() {
  return (
    <Box
      sx={{
        py: { xs: 10, md: 15 },
        overflow: "hidden",
        bgcolor: "primary.lighter",
      }}
    >
      <Container>
        <Grid
          container
          spacing={{ xs: 5, md: 3 }}
          alignItems={{ md: "center" }}
          justifyContent={{ md: "space-between" }}
          direction={{ xs: "column-reverse", md: "row" }}
        >
          <Grid xs={12} md={5} sx={{ textAlign: "center", color: "grey.800" }}>
            <Typography variant="h3">
              Bądź na bieżąco z naszą aktualną ofertą i promocjami
            </Typography>

            <Typography sx={{ mt: 2.5, mb: 5 }}>
              Zapisz się do newslettera{" "}
              <Typography
                variant="overline"
                color="primary"
                sx={{ fontSize: 17, textTransform: "none" }}
              >
                loop
              </Typography>
            </Typography>

            <NewsletterEmail buttonLabel="Zapisz" sx={{ mt: 0.3 }} />
          </Grid>

          <Grid xs={12} md={5}>
            <Image
              alt="newsletter"
              src="/assets/illustrations/illustration_newsletter.svg"
              sx={{ maxWidth: 366, mx: "auto" }}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

interface Props extends LoadingButtonProps {
  buttonLabel: string;
}

export function NewsletterEmail({ buttonLabel = "Zapisz", sx }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: register } = useRegisterNewsletter();

  const NewsletterSchema = Yup.object().shape({
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
    acceptance: Yup.boolean()
      .required("To pole jest wymagane")
      .oneOf([true], "To pole jest wymagane"),
    newsletter: Yup.boolean()
      .required("To pole jest wymagane")
      .oneOf([true], "To pole jest wymagane"),
  });

  const defaultValues = {
    email: "",
    acceptance: false,
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
      await register(data);
      enqueueSnackbar("Zapisano do newslettera", { variant: "success" });
      reset();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <FormProvider methods={methods} onSubmit={onSubmit}>
      <Stack spacing={2.5} direction="row" alignItems="center">
        <RHFTextField name="email" label="Wpisz swój adres e-mail" />

        <LoadingButton
          color="primary"
          size="large"
          variant="contained"
          type="submit"
          loading={isSubmitting}
          sx={sx}
        >
          {buttonLabel}
        </LoadingButton>
      </Stack>

      <Stack spacing={0.5} alignItems="flex-start">
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
    </FormProvider>
  );
}
