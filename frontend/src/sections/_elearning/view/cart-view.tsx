"use client";

import { useMemo, useEffect } from "react";

import { Stack } from "@mui/material";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { useCarts } from "src/api/carts/carts";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";

import { ICartProp } from "src/types/cart";

import CartList from "../cart/cart-list";
import CartSummary from "../cart/cart-summary";

// ----------------------------------------------------------------------

export default function CartView() {
  const { isLoggedIn } = useUserContext();
  const { push } = useRouter();

  const { data: cartItems } = useCarts({ page_size: -1 });

  const prices = useMemo(
    () => cartItems?.map((wishlistItem: ICartProp) => Number(wishlistItem.lesson.price)),
    [cartItems],
  );

  const total = prices?.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

  useEffect(() => {
    if (!isLoggedIn) {
      push(paths.login);
    }
  }, [isLoggedIn, push]);

  return (
    <Container
      sx={{
        overflow: "hidden",
        pt: 5,
        pb: { xs: 5, md: 10 },
      }}
    >
      <Typography variant="h3" sx={{ mb: 5 }}>
        Koszyk
      </Typography>

      {cartItems && cartItems.length === 0 && (
        <Stack alignItems="center">
          <Typography variant="h5">Nie masz jeszcze nic w koszyku</Typography>
        </Stack>
      )}

      {cartItems && cartItems.length > 0 && (
        <>
          <Grid container spacing={{ xs: 5, md: 8 }}>
            <Grid xs={12} md={8}>
              <CartList cartItems={cartItems} />
            </Grid>

            <Grid xs={12} md={4}>
              <CartSummary total={total} subtotal={total} discount={0} />
            </Grid>
          </Grid>
          <Button
            component={RouterLink}
            href={paths.eCommerce.products}
            color="inherit"
            startIcon={<Iconify icon="carbon:chevron-left" />}
            sx={{ mt: 3 }}
          >
            Kontynuuj przeglądanie kursów
          </Button>
        </>
      )}
    </Container>
  );
}
