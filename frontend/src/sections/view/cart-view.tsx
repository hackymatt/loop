"use client";

import { AxiosError } from "axios";
import { useMemo, useState } from "react";

import { Stack } from "@mui/material";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";
import { RouterLink } from "src/routes/components";

import { trackEvents } from "src/utils/track-events";

import { useCarts } from "src/api/carts/carts";
import { useCreatePurchase } from "src/api/purchases/purchases";

import Iconify from "src/components/iconify";
import { useToastContext } from "src/components/toast";

import { ICartProp } from "src/types/cart";
import { IPurchaseError } from "src/types/purchase";

import CartList from "../cart/cart-list";
import CartSummary from "../cart/cart-summary";

// ----------------------------------------------------------------------

export default function CartView() {
  const { enqueueSnackbar } = useToastContext();
  const { push } = useRouter();

  const [error, setError] = useState<IPurchaseError | undefined>();

  const { data: cartItems } = useCarts({ page_size: -1 });

  const prices = useMemo(
    () => cartItems?.map((wishlistItem: ICartProp) => Number(wishlistItem.lesson.price)),
    [cartItems],
  );

  const total = prices?.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

  const { mutateAsync: createPurchase, isLoading: isSubmitting } = useCreatePurchase();

  const handlePurchase = async (coupon: string) => {
    try {
      const paymentRegistration = await createPurchase({
        lessons: cartItems.map((cItem: ICartProp) => ({ lesson: cItem.lesson.id })),
        coupon,
      });

      const { token } = paymentRegistration;

      if (token === undefined) {
        enqueueSnackbar("Wystąpił błąd podczas zakupu", { variant: "error" });
        return;
      }

      trackEvents(
        "purchase_started",
        "purchase",
        "Purchase started",
        [cartItems?.map((cartItem: ICartProp) => cartItem.lesson.title).join(","), coupon].join(
          ";",
        ),
      );

      if (token === "") {
        push(paths.order.completed);
      } else {
        const paymentUrl = `${paths.payment.url}/${token}`;
        push(paymentUrl);
      }
    } catch (err) {
      setError((err as AxiosError).response?.data as IPurchaseError);
      enqueueSnackbar("Wystąpił błąd podczas zakupu", { variant: "error" });
    }
  };

  return (
    <Container
      sx={{
        overflow: "hidden",
        pt: 5,
        pb: { xs: 5, md: 10 },
      }}
    >
      <Typography variant="h3" sx={{ mb: 5 }}>
        {`Koszyk (${cartItems?.length ?? 0})`}
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
              <CartList cartItems={cartItems} error={error} />
            </Grid>

            <Grid xs={12} md={4}>
              <CartSummary
                total={total}
                onPurchase={handlePurchase}
                isLoading={isSubmitting}
                error={error?.coupon}
              />
            </Grid>
          </Grid>
          <Button
            component={RouterLink}
            href={paths.courses}
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
