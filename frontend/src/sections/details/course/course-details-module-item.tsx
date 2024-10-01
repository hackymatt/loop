import { LoadingButton } from "@mui/lab";
import Typography from "@mui/material/Typography";
import { Box, Stack, Divider } from "@mui/material";
import AccordionDetails from "@mui/material/AccordionDetails";
import Accordion, { accordionClasses } from "@mui/material/Accordion";
import AccordionSummary, { accordionSummaryClasses } from "@mui/material/AccordionSummary";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks/use-router";

import { fCurrency } from "src/utils/format-number";
import { romanize } from "src/utils/romanize-number";
import { trackEvent } from "src/utils/google-analytics";

import { useCreateCart } from "src/api/carts/carts";
import { useCreateWishlist } from "src/api/wishlists/wishlists";

import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import { useToastContext } from "src/components/toast";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import { UserType } from "src/types/user";
import { ICourseLessonProp, ICourseModuleProp } from "src/types/course";

import CourseDetailsLessonList from "./course-details-lesson-list";

// ----------------------------------------------------------------------

type ModuleItemProps = {
  module: ICourseModuleProp;
  index: number;
  expanded: boolean;
  onExpanded: (event: React.SyntheticEvent, isExpanded: boolean) => void;
};

// ----------------------------------------------------------------------

export default function CourseDetailsModuleItem({
  module,
  index,
  expanded,
  onExpanded,
}: ModuleItemProps) {
  const { enqueueSnackbar } = useToastContext();
  const { isLoggedIn, userType } = useUserContext();
  const { push } = useRouter();

  const { mutateAsync: createWishlistItem, isLoading: isAddingToFavorites } = useCreateWishlist();
  const { mutateAsync: createCartItem, isLoading: isAddingToCart } = useCreateCart();

  const handleAddToFavorites = async () => {
    if (!isLoggedIn) {
      push(paths.login);
      return;
    }
    try {
      const wishlistItems = module.lessons!.map((lesson: ICourseLessonProp) =>
        createWishlistItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(wishlistItems);
      enqueueSnackbar("Moduł został dodany do ulubionych", { variant: "success" });
      trackEvent("add_to_wishlist", "module", "Module added to wishlist", module.title);
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
      const cartItems = module.lessons!.map((lesson: ICourseLessonProp) =>
        createCartItem({ lesson: lesson.id }),
      );
      await Promise.allSettled(cartItems);
      enqueueSnackbar("Moduł został dodany do koszyka", { variant: "success" });
      trackEvent("add_to_cart", "module", "Module added to cart", module.title);
    } catch (error) {
      enqueueSnackbar("Wystąpił błąd podczas dodawania do koszyka", { variant: "error" });
    }
  };

  return (
    <Accordion
      expanded={expanded}
      onChange={onExpanded}
      sx={{
        [`&.${accordionClasses.expanded}`]: {
          borderRadius: 0,
        },
      }}
    >
      <AccordionSummary
        sx={{
          px: 1,
          minHeight: 64,
          [`& .${accordionSummaryClasses.content}`]: {
            p: 0,
            m: 0,
            alignItems: "center",
          },
          [`&.${accordionSummaryClasses.expanded}`]: {
            bgcolor: "action.selected",
          },
        }}
      >
        <Stack
          direction="row"
          spacing={1}
          alignItems="center"
          sx={{
            flexGrow: 1,
          }}
        >
          {module.progress !== undefined ? (
            <CircularProgressWithLabel value={module.progress} size={35} />
          ) : null}

          <Typography variant="subtitle1">{`Moduł ${romanize(index)}: ${module.title}`}</Typography>
        </Stack>

        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h6" sx={{ textAlign: "right" }}>
            {module?.priceSale !== undefined && (
              <Box
                component="span"
                sx={{
                  mr: 0.5,
                  color: "text.disabled",
                  textDecoration: "line-through",
                }}
              >
                {fCurrency(module.priceSale)}
              </Box>
            )}
            {module?.price !== undefined ? fCurrency(module.price) : null}
            {module?.priceSale !== undefined &&
              module?.priceSale !== null &&
              module?.lowest30DaysPrice !== undefined &&
              module?.lowest30DaysPrice !== null && (
                <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "center" }}>
                  Najniższa cena z 30 dni przed: {fCurrency(module.lowest30DaysPrice)}
                </Typography>
              )}
          </Typography>
        </Stack>

        <Iconify icon={expanded ? "carbon:chevron-down" : "carbon:chevron-right"} sx={{ ml: 2 }} />
      </AccordionSummary>

      <AccordionDetails
        sx={{
          p: 2,
          typography: "body",
        }}
      >
        <Stack spacing={3}>
          {module.lessons && <CourseDetailsLessonList lessons={module.lessons ?? []} />}

          <Divider sx={{ borderStyle: "dashed" }} />

          <Stack direction="row" spacing={0.5} flexWrap="wrap" justifyContent="right">
            <LoadingButton
              size="medium"
              color="error"
              variant="contained"
              onClick={handleAddToFavorites}
              loading={isAddingToFavorites}
              disabled={userType !== UserType.Student}
            >
              <Iconify icon="carbon:favorite" />
            </LoadingButton>
            <LoadingButton
              size="medium"
              color="inherit"
              variant="contained"
              onClick={handleAddToCart}
              loading={isAddingToCart}
              disabled={userType !== UserType.Student}
            >
              <Iconify icon="carbon:shopping-cart-plus" />
            </LoadingButton>
          </Stack>
        </Stack>
      </AccordionDetails>
    </Accordion>
  );
}
