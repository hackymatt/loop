import { polishPlurals } from "polish-plurals";

import Stack from "@mui/material/Stack";
import { LoadingButton } from "@mui/lab";
import Typography from "@mui/material/Typography";

import { fCurrency } from "src/utils/format-number";
import { trackEvents } from "src/utils/track-events";

import { useDeleteCart } from "src/api/carts/cart";
import { useCreateCart } from "src/api/carts/carts";
import { useDeleteWishlist } from "src/api/wishlists/wishlist";

import Iconify from "src/components/iconify";
import { useToastContext } from "src/components/toast";
import TextMaxLine from "src/components/text-max-line";

import { ICartProp } from "src/types/cart";
import { ICourseTeacherProp, ICourseByTechnologyProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  cartItem: ICartProp;
  error?: string;
  wishlist: boolean;
};

export default function CartItem({ cartItem, error, wishlist }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: deleteWishlist, isLoading: isDeletingWishlist } = useDeleteWishlist();
  const { mutateAsync: deleteCart, isLoading: isDeletingCart } = useDeleteCart();
  const { mutateAsync: createCartItem, isLoading: isCreatingCart } = useCreateCart();

  const handleDeleteFromWishlist = async () => {
    try {
      await deleteWishlist({ id: cartItem.id });
      enqueueSnackbar("Lekcja została usunięta z ulubionych", { variant: "success" });
      trackEvents("wishlist_to_trash", "wishlist", "Wishlist item removed", cartItem.lesson.title);
    } catch (err) {
      enqueueSnackbar("Wystąpił błąd podczas usuwania z ulubionych", { variant: "error" });
    }
  };

  const handleDeleteFromCart = async () => {
    try {
      await deleteCart({ id: cartItem.id });
      enqueueSnackbar("Lekcja została usunięta z koszyka", { variant: "success" });
      trackEvents("cart_to_trash", "cart", "Cart item removed", cartItem.lesson.title);
    } catch (err) {
      enqueueSnackbar("Wystąpił błąd podczas usuwania z koszyka", { variant: "error" });
    }
  };

  const handleAddToCart = async () => {
    try {
      await Promise.allSettled([
        createCartItem({ lesson: cartItem.lesson.id }),
        deleteWishlist({ id: cartItem.id }),
      ]);
      enqueueSnackbar("Lekcja została dodana do koszyka", { variant: "success" });
      trackEvents(
        "wishlist_to_cart",
        "wishlist",
        "Wishlist item added to cart",
        cartItem.lesson.title,
      );
    } catch (err) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
    }
  };

  return (
    <Stack
      direction="row"
      alignItems="center"
      sx={{
        py: 1,
        minWidth: 720,
        borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
      }}
    >
      <Stack direction="row" alignItems="center" flexGrow={1}>
        <Stack spacing={0.5} sx={{ p: 2 }}>
          <TextMaxLine variant="subtitle2" line={1}>
            {cartItem.lesson.title}
          </TextMaxLine>

          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Czas trwania: {cartItem.lesson.duration}{" "}
            {polishPlurals("minuta", "minuty", "minut", cartItem.lesson.duration)}
          </Typography>
          {cartItem.lesson.technologies && cartItem.lesson.technologies.length > 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              Technologie:{" "}
              {cartItem.lesson.technologies
                .map((technology: ICourseByTechnologyProps) => technology.name)
                .join(", ")}{" "}
            </Typography>
          )}
          {cartItem.lesson.teachers && cartItem.lesson.teachers.length > 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              Nauczyciele:{" "}
              {cartItem.lesson.teachers
                ?.map((teacher: ICourseTeacherProp) => teacher.name)
                .join(", ")}{" "}
            </Typography>
          )}
          <Typography variant="body2" sx={{ color: "error.main" }}>
            {error}
          </Typography>
        </Stack>
      </Stack>

      <Stack sx={{ width: 120, typography: "subtitle2" }}>
        {" "}
        {fCurrency(cartItem.lesson.price)}{" "}
      </Stack>

      <LoadingButton
        size="small"
        color="error"
        variant="text"
        onClick={wishlist ? handleDeleteFromWishlist : handleDeleteFromCart}
        loading={wishlist ? isDeletingWishlist : isDeletingCart}
      >
        <Iconify icon="carbon:trash-can" />
      </LoadingButton>

      {wishlist && (
        <LoadingButton
          size="small"
          color="success"
          variant="text"
          onClick={handleAddToCart}
          loading={isCreatingCart}
        >
          <Iconify icon="carbon:shopping-cart-plus" />
        </LoadingButton>
      )}
    </Stack>
  );
}
