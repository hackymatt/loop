import * as Yup from "yup";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import LoadingButton from "@mui/lab/LoadingButton";

import { useResponsive } from "src/hooks/use-responsive";
import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useContact } from "src/api/contact/contact";

import Image from "src/components/image";
import { useToastContext } from "src/components/toast";
import FormProvider, { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export default function ContactForm() {
  const { enqueueSnackbar } = useToastContext();

  const mdUp = useResponsive("up", "md");

  const { mutateAsync: contact } = useContact();

  const ContactSchema = Yup.object().shape({
    full_name: Yup.string().required("Imię i Nazwisko jest wymagane"),
    email: Yup.string().required("Adres e-mail jest wymagany").email("Podaj poprawny adres e-mail"),
    subject: Yup.string().required("Temat jest wymagany"),
    message: Yup.string().required("Wiadomość jest wymagana"),
  });

  const defaultValues = {
    full_name: "",
    subject: "",
    email: "",
    message: "",
  };

  const methods = useForm({
    resolver: yupResolver(ContactSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await contact(data);
      enqueueSnackbar("Wysłano wiadomość", { variant: "success" });
      reset();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Box
      sx={{
        bgcolor: "background.neutral",
        py: { xs: 10, md: 15 },
      }}
    >
      <Container>
        <Grid container spacing={3} justifyContent="space-between">
          {mdUp && (
            <Grid xs={12} md={6} lg={5}>
              <Image
                alt="contact"
                src="/assets/illustrations/illustration_courses_contact.svg"
                sx={{ maxWidth: 260 }}
              />
            </Grid>
          )}

          <Grid xs={12} md={6} lg={6}>
            <Stack
              spacing={2}
              sx={{
                mb: 5,
                textAlign: { xs: "center", md: "left" },
              }}
            >
              <Typography variant="h3">Napisz do nas</Typography>

              <Typography sx={{ color: "text.secondary" }}>
                Zwykle odpowiadamy w ciągu 2 dni roboczych
              </Typography>
            </Stack>

            <FormProvider methods={methods} onSubmit={onSubmit}>
              <Stack spacing={2.5} alignItems="flex-start">
                <RHFTextField name="full_name" label="Imię i nazwisko" />

                <RHFTextField name="email" label="Adres e-mail" />

                <RHFTextField name="subject" label="Tytuł" />

                <RHFTextField
                  name="message"
                  multiline
                  rows={4}
                  label="Wiadomość"
                  sx={{ pb: 2.5 }}
                />

                <LoadingButton
                  size="large"
                  type="submit"
                  variant="contained"
                  loading={isSubmitting}
                  sx={{
                    mx: { xs: "auto !important", md: "unset !important" },
                  }}
                >
                  Wyślij wiadomość
                </LoadingButton>
              </Stack>
            </FormProvider>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}
