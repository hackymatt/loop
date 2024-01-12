import { useState } from "react";
import packageInfo from "package.json";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import InputAdornment from "@mui/material/InputAdornment";
import InputBase, { inputBaseClasses } from "@mui/material/InputBase";

import { useRegisterNewsletter } from "src/api/newsletter/newsletter";

import Image from "src/components/image";

// ----------------------------------------------------------------------

export default function Newsletter() {
  const [email, setEmail] = useState<string>();
  const { mutateAsync: register } = useRegisterNewsletter();

  const handleRegister = () => {
    if (email) {
      register({ email });
    }
  };

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

            <InputBase
              fullWidth
              placeholder="Wpisz swój adres e-mail"
              endAdornment={
                <InputAdornment position="end">
                  <Button
                    color="primary"
                    size="large"
                    variant="contained"
                    disabled={!email}
                    onClick={handleRegister}
                  >
                    Zapisz
                  </Button>
                </InputAdornment>
              }
              sx={{
                pr: 0.5,
                pl: 1.5,
                height: 56,
                maxWidth: 560,
                borderRadius: 1,
                bgcolor: "common.white",
                transition: (theme) => theme.transitions.create(["box-shadow"]),
                [`&.${inputBaseClasses.focused}`]: {
                  boxShadow: (theme) => theme.customShadows.z4,
                },
              }}
              onChange={(event) => setEmail(event.target.value)}
            />
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
