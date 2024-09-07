import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import { LoadingButton } from "@mui/lab";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";

import { fCurrency } from "src/utils/format-number";

import { useCreateCart } from "src/api/carts/carts";
import { useCreateWishlist } from "src/api/wishlists/wishlists";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";

import { UserType } from "src/types/user";
import { ICourseProps, ICourseLessonProp, ICourseModuleProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
};

export default function CourseDetailsInfo({ course }: Props) {
  const { enqueueSnackbar } = useToastContext();
  const { isLoggedIn, userType } = useUserContext();
  const { push } = useRouter();

  const { mutateAsync: createWishlistItem, isLoading: isAddingToFavorites } = useCreateWishlist();
  const { mutateAsync: createCartItem, isLoading: isAddingToCart } = useCreateCart();

  const allLessons = useMemo(
    () =>
      course?.modules
        ?.map((module: ICourseModuleProp) => module.lessons)
        .flat() as ICourseLessonProp[],
    [course?.modules],
  );

  const handleAddToFavorites = async () => {
    if (!isLoggedIn) {
      push(paths.login);
      return;
    }
    try {
      const wishlistItems = allLessons.map((lesson: ICourseLessonProp) =>
        createWishlistItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(wishlistItems);
      enqueueSnackbar("Kurs został dodany do ulubionych", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do ulubionych", { variant: "error" });
    }
  };

  const handleAddToCart = async () => {
    if (!isLoggedIn) {
      push(paths.login);
      return;
    }
    try {
      const cartItems = allLessons.map((lesson: ICourseLessonProp) =>
        createCartItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(cartItems);
      enqueueSnackbar("Kurs został dodany do koszyka", { variant: "success" });
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
    }
  };

  return (
    <Card sx={{ p: 3, borderRadius: 2 }}>
      <Stack spacing={3}>
        <Stack>
          <Stack direction="row" justifyContent="left" sx={{ typography: "h3" }}>
            {!!course.priceSale && (
              <Box
                component="span"
                sx={{
                  mr: 0.5,
                  color: "text.disabled",
                  textDecoration: "line-through",
                }}
              >
                {fCurrency(course.priceSale)}
              </Box>
            )}
            {fCurrency(course.price)}
          </Stack>
          {!!course.priceSale && course.lowest30DaysPrice && (
            <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "left" }}>
              Najniższa cena z 30 dni przed: {fCurrency(course.lowest30DaysPrice)}
            </Typography>
          )}
        </Stack>

        <Stack spacing={2}>
          <Typography>Ten kurs zawiera:</Typography>

          {course.modules && (
            <>
              <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                <Iconify icon="carbon:document-multiple-01" sx={{ mr: 1 }} />
                <Box component="strong" sx={{ mr: 0.5 }}>
                  {course.modules?.length}
                </Box>
                {polishPlurals("moduł", "moduły", "modułów", course.modules?.length)}
              </Stack>

              <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                <Iconify icon="carbon:document" sx={{ mr: 1 }} />
                <Box component="strong" sx={{ mr: 0.5 }}>
                  {allLessons?.length}
                </Box>
                {polishPlurals("lekcję", "lekcje", "lekcji", allLessons?.length)}
              </Stack>
            </>
          )}

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

        <Stack spacing={0.5}>
          <LoadingButton
            size="large"
            color="primary"
            variant="contained"
            startIcon={<Iconify icon="carbon:certificate-check" />}
            loading={isAddingToFavorites}
            onClick={handleAddToFavorites}
            disabled={userType !== UserType.Student || (course.progress ?? 0) < 100}
          >
            Wygeneruj certyfikat
          </LoadingButton>
          <LoadingButton
            size="large"
            color="error"
            variant="contained"
            startIcon={<Iconify icon="carbon:favorite-filled" />}
            loading={isAddingToFavorites}
            onClick={handleAddToFavorites}
            disabled={userType !== UserType.Student}
          >
            Dodaj do ulubionych
          </LoadingButton>
          <LoadingButton
            size="large"
            color="inherit"
            variant="contained"
            startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
            loading={isAddingToCart}
            onClick={handleAddToCart}
            disabled={userType !== UserType.Student}
          >
            Dodaj do koszyka
          </LoadingButton>
        </Stack>
      </Stack>
    </Card>
  );
}
