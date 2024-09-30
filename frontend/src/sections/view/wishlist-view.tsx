"use client";

import { useMemo } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import { LoadingButton } from "@mui/lab";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";
import { useRouter } from "src/routes/hooks/use-router";

import { fCurrency } from "src/utils/format-number";

import { useCreateCart } from "src/api/carts/carts";
import { useWishlists } from "src/api/wishlists/wishlists";
import { useDeleteWishlist } from "src/api/wishlists/wishlist";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

import { ICartProp } from "src/types/cart";

import CartList from "../cart/cart-list";

// ----------------------------------------------------------------------

export default function WishlistView() {
  const { enqueueSnackbar } = useToastContext();
  const { isLoggedIn } = useUserContext();
  const { push } = useRouter();

  const { data: wishlistItems } = useWishlists({ page_size: -1 });
  const { mutateAsync: createCartItem, isLoading: isAddingToCart } = useCreateCart();
  const { mutateAsync: deleteWishlist, isLoading: isDeletingWishlist } = useDeleteWishlist();

  const prices = useMemo(
    () => wishlistItems?.map((wishlistItem: ICartProp) => Number(wishlistItem.lesson.price)),
    [wishlistItems],
  );

  const total = prices?.reduce((accumulator, currentValue) => accumulator + currentValue, 0);

  const handleSubmit = async () => {
    if (!isLoggedIn) {
      push(paths.login);
      return;
    }
    try {
      const cartItems = wishlistItems.map((wishlistItem: ICartProp) => [
        createCartItem({ lesson: wishlistItem.lesson.id }),
        deleteWishlist({ id: wishlistItem.id }),
      ]);
      await Promise.allSettled(cartItems);
      enqueueSnackbar("Ulubione zostały dodane do koszyka", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
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
        {`Ulubione (${wishlistItems?.length ?? 0})`}
      </Typography>

      {wishlistItems && wishlistItems.length === 0 && (
        <Stack alignItems="center">
          <Typography variant="h5">Nie masz jeszcze nic na liście ulubionych</Typography>
        </Stack>
      )}

      {wishlistItems && wishlistItems.length > 0 && (
        <>
          <CartList wishlist cartItems={wishlistItems} />
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
                {total === 0 ? "0,00 zł" : fCurrency(total)}
              </Stack>

              <LoadingButton
                size="large"
                color="inherit"
                variant="contained"
                startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
                onClick={handleSubmit}
                loading={isAddingToCart || isDeletingWishlist}
              >
                Dodaj do koszyka
              </LoadingButton>
            </Stack>
          </Stack>
        </>
      )}
    </Container>
  );
}
