import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fCurrency, fShortenNumber } from "src/utils/format-number";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import TextMaxLine from "src/components/text-max-line";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import { ILevel, ICourseProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
  vertical?: boolean;
};

export default function CourseItem({ course, vertical }: Props) {
  const {
    id,
    slug,
    level,
    price,
    teachers,
    coverUrl,
    category: categories,
    priceSale,
    lowest30DaysPrice,
    totalHours,
    description,
    ratingNumber,
    totalReviews,
    totalStudents,
    progress,
  } = course;

  const genderAvatarUrl =
    teachers?.[0]?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = teachers?.[0]?.avatarUrl || genderAvatarUrl;

  return (
    <Card
      sx={{
        display: { sm: "flex" },
        "&:hover": {
          boxShadow: (theme) => theme.customShadows.z24,
        },
        ...(vertical && {
          flexDirection: "column",
        }),
      }}
    >
      <Box sx={{ flexShrink: { sm: 0 } }}>
        <Image
          alt={slug}
          src={coverUrl}
          sx={{
            height: 1,
            objectFit: "cover",
            width: { sm: 240 },
            ...(vertical && {
              width: { sm: 1 },
            }),
          }}
        />
      </Box>

      {progress && (
        <Box
          sx={{
            top: 12,
            left: 12,
            position: "absolute",
          }}
        >
          <CircularProgressWithLabel value={progress} size={50} />
        </Box>
      )}

      <Stack spacing={3} sx={{ p: 3 }}>
        <Stack
          spacing={{
            xs: 3,
            sm: vertical ? 3 : 1,
          }}
        >
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            {categories && (
              <Stack
                spacing={0.5}
                direction="row"
                alignItems="center"
                flexWrap="wrap"
                divider={
                  <Box
                    sx={{
                      width: 4,
                      height: 4,
                      bgcolor: "text.disabled",
                      borderRadius: "50%",
                    }}
                  />
                }
              >
                {categories.map((category: string) => (
                  <Typography key={category} variant="overline" sx={{ color: "primary.main" }}>
                    {category}
                  </Typography>
                ))}
              </Stack>
            )}

            <Typography variant="h4" sx={{ textAlign: "right" }}>
              {priceSale && (
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
              )}
              {fCurrency(price)}
              {priceSale && lowest30DaysPrice && (
                <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "center" }}>
                  Najniższa cena z 30 dni przed: {fCurrency(lowest30DaysPrice)}
                </Typography>
              )}
            </Typography>
          </Stack>

          <Stack spacing={1}>
            <Link component={RouterLink} href={`${paths.course}/${id}`} color="inherit">
              <TextMaxLine variant="h6" line={1}>
                {slug}
              </TextMaxLine>
            </Link>

            <TextMaxLine
              variant="body2"
              color="text.secondary"
              sx={{
                ...(vertical && {
                  display: { sm: "none" },
                }),
                textAlign: "justify",
              }}
            >
              {description}
            </TextMaxLine>
          </Stack>
        </Stack>

        <Stack
          spacing={1.5}
          direction="row"
          alignItems="center"
          flexWrap="wrap"
          divider={<Divider orientation="vertical" sx={{ height: 20, my: "auto" }} />}
        >
          {totalReviews && (
            <Stack spacing={0.5} direction="row" alignItems="center">
              <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
              <Box sx={{ typography: "h6" }}>
                {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
              </Box>

              <Link variant="body2" sx={{ color: "text.secondary" }}>
                ({fShortenNumber(totalReviews)}{" "}
                {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
              </Link>
            </Stack>
          )}

          {totalStudents > 0 && (
            <Stack direction="row" sx={{ typography: "subtitle2" }}>
              {fShortenNumber(totalStudents)}
              <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                {polishPlurals("student", "studentów", "studentów", totalStudents)}
              </Box>
            </Stack>
          )}
        </Stack>

        {teachers?.length > 0 && (
          <Stack direction="row" alignItems="center">
            <Avatar src={avatarUrl} />

            <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
              {teachers[0]?.name}
            </Typography>

            {teachers?.length > 1 && (
              <Link underline="always" color="text.secondary" variant="body2">
                + {teachers.length - 1}{" "}
                {polishPlurals("nauczyciel", "nauczycieli", "nauczycieli", teachers.length - 1)}
              </Link>
            )}
          </Stack>
        )}

        <Divider
          sx={{
            borderStyle: "dashed",
            display: { sm: "none" },
            ...(vertical && {
              display: "block",
            }),
          }}
        />

        <Stack
          direction="row"
          flexWrap="wrap"
          alignItems="center"
          sx={{ color: "text.disabled", "& > *:not(:last-child)": { mr: 2.5 } }}
        >
          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify icon="carbon:time" sx={{ mr: 1 }} />
            {totalHours < 1 ? totalHours : fShortenNumber(Math.floor(totalHours), 0)}+{" "}
            {polishPlurals("godzina", "godziny", "godzin", totalHours)}
          </Stack>

          <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
            <Iconify
              icon={
                (level === ("Podstawowy" as ILevel) && "carbon:skill-level") ||
                (level === ("Średniozaawansowany" as ILevel) && "carbon:skill-level-basic") ||
                (level === ("Zaawansowany" as ILevel) && "carbon:skill-level-intermediate") ||
                "carbon:skill-level-advanced"
              }
              sx={{ mr: 1 }}
            />
            {level}
          </Stack>
        </Stack>
      </Stack>
    </Card>
  );
}
