"use client";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fCurrency } from "src/utils/format-number";

import { LESSONS, _courses, _products } from "src/_mock";

import Iconify from "src/components/iconify";

import CartList from "../cart/cart-list";

// ----------------------------------------------------------------------

export default function WishlistView() {
  const handleSubmit = async () => {};

  return (
    <Container
      sx={{
        overflow: "hidden",
        pt: 5,
        pb: { xs: 5, md: 10 },
      }}
    >
      <Typography variant="h3" sx={{ mb: 5 }}>
        Ulubione
      </Typography>

      <CartList wishlist lessons={LESSONS} />

      <Stack
        direction={{ xs: "column-reverse", sm: "row" }}
        alignItems={{ sm: "center" }}
        justifyContent={{ sm: "space-between" }}
        sx={{ mt: 3 }}
      >
        <Button
          component={RouterLink}
          href={paths.courses}
          color="inherit"
          startIcon={<Iconify icon="carbon:chevron-left" />}
          sx={{ mt: 3 }}
        >
          Kontynuuj przeglądanie kursów
        </Button>

        <Stack spacing={3} sx={{ minWidth: 240 }}>
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            sx={{ typography: "h6" }}
          >
            <Box component="span">Wartość koszyka</Box>
            {fCurrency(125.45)}
          </Stack>

          <Button
            size="large"
            color="inherit"
            variant="contained"
            startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
            onClick={handleSubmit}
          >
            Dodaj do koszyka
          </Button>
        </Stack>
      </Stack>
    </Container>
  );
}
