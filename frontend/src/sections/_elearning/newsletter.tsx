import * as Yup from "yup";
import packageInfo from "package.json";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import { Stack } from "@mui/material";
import { LoadingButton } from "@mui/lab";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";

import { useRegisterNewsletter } from "src/api/newsletter/newsletter";

import Image from "src/components/image";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function Newsletter() {
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
  } = methods;

  const onSubmit = handleSubmit(async (data) => {
    try {
      await register(data);
      reset();
    } catch (error) {
      console.error(error);
    }
  });

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
                    sx={{ mt: 0.3 }}
                  >
                    Zapisz
                  </LoadingButton>
                </Stack>
              </Stack>
            </FormProvider>
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
