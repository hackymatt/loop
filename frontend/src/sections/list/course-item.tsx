import { useMemo } from "react";
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

import { encodeUrl } from "src/utils/url-utils";
import { getGenderAvatar } from "src/utils/get-gender-avatar";
import { fCurrency, fShortenNumber } from "src/utils/format-number";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import TextMaxLine from "src/components/text-max-line";
import { CircularProgressWithLabel } from "src/components/progress-label/circle-progress";

import { ILevel, ICourseProps, ICourseTechnologyProps } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  course: ICourseProps;
  vertical?: boolean;
};

export default function CourseItem({ course, vertical }: Props) {
  const {
    id,
    title,
    level,
    price,
    teachers,
    image,
    technologies,
    priceSale,
    lowest30DaysPrice,
    totalHours,
    description,
    ratingNumber,
    totalReviews,
    totalStudents,
    progress,
  } = course;

  const firstTeacher = teachers.length > 0 ? teachers[0] : undefined;

  const genderAvatarUrl = getGenderAvatar(firstTeacher?.gender);

  const firstTeacherImage = firstTeacher?.image ?? genderAvatarUrl;

  const path = useMemo(() => `${title}-${id}`, [id, title]);

  return (
    <Link
      component={RouterLink}
      href={`${paths.course}/${encodeUrl(path)}/`}
      color="inherit"
      underline="none"
    >
      <Card
        sx={{
          display: { sm: "flex" },
          "&:hover": {
            boxShadow: (theme) => theme.customShadows.z24,
          },
          ...(vertical && {
            minHeight: 600,
            flexDirection: "column",
          }),
        }}
      >
        <Box sx={{ flexShrink: { sm: 0 } }}>
          <Image
            alt={title}
            src={image}
            sx={{
              objectFit: "cover",
              width: { xs: 1, md: 240 },
              height: { xs: 240, md: 1 },
              ...(vertical && {
                height: { md: 240 },
                width: { md: 1 },
              }),
            }}
          />
        </Box>

        {progress !== null ? (
          <Stack
            justifyContent="center"
            alignItems="center"
            sx={{
              top: 12,
              left: 12,
              position: "absolute",
            }}
          >
            <CircularProgressWithLabel value={progress} size={50} />
          </Stack>
        ) : null}

        <Stack spacing={3} minHeight={340} justifyContent="space-between" sx={{ p: 3 }}>
          <Stack
            spacing={{
              xs: 3,
              sm: vertical ? 3 : 1,
            }}
          >
            <Stack direction="row" alignItems="center" justifyContent="space-between">
              {technologies.length > 0 ? (
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
                  {technologies.map((technology: ICourseTechnologyProps) => (
                    <Typography
                      key={technology.id}
                      variant="overline"
                      sx={{ color: "primary.main" }}
                    >
                      {technology.name}
                    </Typography>
                  ))}
                </Stack>
              ) : null}

              <Typography variant="h4" sx={{ textAlign: "right" }}>
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

                {priceSale !== null && lowest30DaysPrice !== null ? (
                  <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "center" }}>
                    Najniższa cena z 30 dni przed: {fCurrency(lowest30DaysPrice)}
                  </Typography>
                ) : null}
              </Typography>
            </Stack>

            <Stack spacing={1}>
              <TextMaxLine variant="h6" line={2}>
                {title}
              </TextMaxLine>

              <TextMaxLine
                line={3}
                variant="body2"
                color="text.secondary"
                sx={{
                  ...(vertical && {
                    display: { sm: "none" },
                  }),
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
            {totalReviews > 0 ? (
              <Stack spacing={0.5} direction="row" alignItems="center">
                <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                <Box sx={{ typography: "h6" }}>
                  {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
                </Box>

                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  ({fShortenNumber(totalReviews)}{" "}
                  {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
                </Typography>
              </Stack>
            ) : null}

            {totalStudents > 0 && (
              <Stack direction="row" sx={{ typography: "subtitle2" }}>
                {fShortenNumber(totalStudents)}
                <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                  {polishPlurals("student", "studentów", "studentów", totalStudents)}
                </Box>
              </Stack>
            )}
          </Stack>

          {firstTeacher ? (
            <Stack direction="row" alignItems="center">
              <Avatar src={firstTeacherImage} />

              <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                {firstTeacher.name}
              </Typography>

              {teachers.length > 1 ? (
                <Typography
                  color="text.secondary"
                  variant="body2"
                  sx={{ textDecoration: "underline" }}
                >
                  + {teachers.length - 1}{" "}
                  {polishPlurals("nauczyciel", "nauczycieli", "nauczycieli", teachers.length - 1)}
                </Typography>
              ) : null}
            </Stack>
          ) : null}

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
    </Link>
  );
}
