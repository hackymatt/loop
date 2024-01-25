import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { ICourseProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
};

export default function CourseDetailsInfo({ course }: Props) {
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

          {course.lessons && (
            <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
              <Iconify icon="carbon:document" sx={{ mr: 1 }} />
              <Box component="strong" sx={{ mr: 0.5 }}>
                {course.lessons?.length}
              </Box>
              {polishPlurals("lekcja", "lekcje", "lekcji", course.lessons?.length)}
            </Stack>
          )}

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:data-accessor" sx={{ mr: 1 }} />
            Dożywotni dostęp
          </Stack>

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:devices" sx={{ mr: 1 }} />
            Dostęp na komputerach, tabletach i urządzeniach mobilnych
          </Stack>

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:certificate" sx={{ mr: 1 }} />
            Certyfikat ukończenia
          </Stack>
        </Stack>

        <Button
          size="large"
          color="inherit"
          variant="contained"
          startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
        >
          Dodaj do koszyka
        </Button>
      </Stack>
    </Card>
  );
}
