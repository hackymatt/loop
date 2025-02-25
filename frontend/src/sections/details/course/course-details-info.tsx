import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import { LoadingButton } from "@mui/lab";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";

import { encodeUrl } from "src/utils/url-utils";
import { fCurrency } from "src/utils/format-number";
import { trackEvents } from "src/utils/track-events";

import { UserType } from "src/consts/user-type";
import { useCreateCart } from "src/api/carts/carts";
import { useCreateWishlist } from "src/api/wishlists/wishlists";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

import {
  ICourseModuleProps,
  ICourseDetailsProps,
  ICourseModuleLessonProps,
} from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseDetailsProps;
};

export default function CourseDetailsInfo({ course }: Props) {
  const { id, title, price, priceSale, lowest30DaysPrice, modules } = course;

  const { enqueueSnackbar } = useToastContext();
  const { isLoggedIn, userType } = useUserContext();
  const { push } = useRouter();

  const { mutateAsync: createWishlistItem, isLoading: isAddingToFavorites } = useCreateWishlist();
  const { mutateAsync: createCartItem, isLoading: isAddingToCart } = useCreateCart();

  const allLessons = useMemo(
    () => (modules ?? []).map((module: ICourseModuleProps) => module.lessons).flat(),
    [modules],
  );

  const path = useMemo(() => `${paths.course}/${encodeUrl(`${title}-${id}`)}/`, [id, title]);

  const handleAddToFavorites = async () => {
    if (!isLoggedIn) {
      push(`${paths.login}?redirect=${path}`);
      return;
    }

    try {
      const wishlistItems = allLessons.map((lesson: ICourseModuleLessonProps) =>
        createWishlistItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(wishlistItems);
      enqueueSnackbar("Kurs został dodany do ulubionych", { variant: "success" });
      trackEvents("add_to_wishlist", "course", "Course added to wishlist", title);
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do ulubionych", { variant: "error" });
    }
  };

  const handleAddToCart = async () => {
    if (!isLoggedIn) {
      push(`${paths.login}?redirect=${path}`);
      return;
    }
    try {
      const cartItems = allLessons.map((lesson: ICourseModuleLessonProps) =>
        createCartItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(cartItems);
      enqueueSnackbar("Kurs został dodany do koszyka", { variant: "success" });
      trackEvents("add_to_cart", "course", "Course added to cart", title);
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
    }
  };

  return (
    <Card sx={{ p: 3, borderRadius: 2 }}>
      <Stack spacing={3}>
        <Stack>
          <Stack direction="row" justifyContent="left" sx={{ typography: "h3" }}>
            {priceSale !== null ? (
              <Box
                component="span"
                sx={{
                  mr: 0.5,
                  color: "text.disabled",
                  textDecoration: "line-through",
                }}
              >
                {fCurrency(priceSale)}
              </Box>
            ) : null}
            {fCurrency(price)}
          </Stack>
          {priceSale !== null && lowest30DaysPrice !== null && (
            <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "left" }}>
              Najniższa cena z 30 dni przed: {fCurrency(lowest30DaysPrice)}
            </Typography>
          )}
        </Stack>

        <Stack spacing={2}>
          <Typography>Ten kurs zawiera:</Typography>

          {modules.length > 0 ? (
            <>
              <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                <Iconify icon="carbon:document-multiple-01" sx={{ mr: 1 }} />
                <Box component="strong" sx={{ mr: 0.5 }}>
                  {modules.length}
                </Box>
                {polishPlurals("moduł", "moduły", "modułów", modules.length)}
              </Stack>

              <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                <Iconify icon="carbon:document" sx={{ mr: 1 }} />
                <Box component="strong" sx={{ mr: 0.5 }}>
                  {allLessons?.length}
                </Box>
                {polishPlurals("lekcję", "lekcje", "lekcji", allLessons?.length)}
              </Stack>
            </>
          ) : null}

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:data-accessor" sx={{ mr: 1 }} />
            Dożywotni dostęp
          </Stack>

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:devices" sx={{ mr: 1, width: "30px" }} />
            Dostęp na komputerach, tabletach i urządzeniach mobilnych
          </Stack>

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:certificate" sx={{ mr: 1 }} />
            Certyfikat ukończenia
          </Stack>
        </Stack>

        <Stack direction="row" spacing={0.5}>
          <LoadingButton
            size="large"
            color="error"
            variant="contained"
            loading={isAddingToFavorites}
            onClick={handleAddToFavorites}
            disabled={userType !== UserType.Student}
          >
            <Iconify icon="carbon:favorite" />
          </LoadingButton>
          <LoadingButton
            size="large"
            color="inherit"
            variant="contained"
            startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
            loading={isAddingToCart}
            onClick={handleAddToCart}
            disabled={userType !== UserType.Student}
            sx={{ width: 1 }}
          >
            Dodaj do koszyka
          </LoadingButton>
        </Stack>
      </Stack>
    </Card>
  );
}
