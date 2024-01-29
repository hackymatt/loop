import * as Yup from "yup";
import packageInfo from "package.json";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import { Stack } from "@mui/material";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import { LoadingButton, LoadingButtonProps } from "@mui/lab";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useRegisterNewsletter } from "src/api/newsletter/register";

import Image from "src/components/image";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

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
                sx={{
                  fontSize: 15,
                  color: "primary.main",
                }}
              >
                {packageInfo.name}
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
    email: Yup.string().required("Adres email jest wymagany").email("Podaj poprawny adres e-mail"),
  });

  const defaultValues = {
    email: "",
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
      <Stack spacing={2.5} direction="row">
        <RHFTextField name="email" label="Wpisz swój adres e-mail" />

        <Stack justifyContent="flex-start">
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
      </Stack>
    </FormProvider>
  );
}
