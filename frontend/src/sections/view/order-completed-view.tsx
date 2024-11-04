"use client";

import { m } from "framer-motion";
import { useEffect } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { trackEvents } from "src/utils/track-events";

import { useCarts } from "src/api/carts/carts";
import { useDeleteCart } from "src/api/carts/cart";

import Iconify from "src/components/iconify";
import { useToastContext } from "src/components/toast";
import { varBounce, MotionContainer } from "src/components/animate";

import { ICartProp } from "src/types/cart";

// ----------------------------------------------------------------------

export default function OrderCompletedView() {
  const { enqueueSnackbar } = useToastContext();

  const { data: cartItems } = useCarts({ page_size: -1 });
  const { mutateAsync: deleteCart } = useDeleteCart();

  useEffect(() => {
    if (cartItems) {
      try {
        const clearCart = async () => {
          await Promise.allSettled(
            cartItems.map((cItem: ICartProp) => deleteCart({ id: cItem.id })),
          );
        };
        clearCart();
        trackEvents(
          "purchase_completed",
          "purchase",
          "Purchase completed",
          cartItems?.map((cartItem: ICartProp) => cartItem.lesson.title).join(","),
        );
      } catch {
        enqueueSnackbar("Wystąpił błąd podczas czyszczenia koszyka", { variant: "error" });
      }
    }
  }, [cartItems, deleteCart, enqueueSnackbar]);

  return (
    <Container
      component={MotionContainer}
      sx={{
        textAlign: "center",
        pt: { xs: 5, md: 10 },
        pb: { xs: 10, md: 20 },
      }}
    >
      <m.div variants={varBounce().in}>
        <Box sx={{ fontSize: 128 }}>🎉</Box>
      </m.div>

      <Stack spacing={1} sx={{ my: 5 }}>
        <Typography variant="h3">Twój zakup jest zakończony!</Typography>
      </Stack>

      <Button
        component={RouterLink}
        href={`${paths.account.lessons}/?sort_by=-created_at&page_size=10`}
        size="large"
        color="inherit"
        variant="contained"
        endIcon={<Iconify icon="carbon:chevron-right" />}
      >
        Sprawdź swoje lekcje
      </Button>
    </Container>
  );
}
