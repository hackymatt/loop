import { polishPlurals } from "polish-plurals";

import Typography from "@mui/material/Typography";
import AccordionDetails from "@mui/material/AccordionDetails";
import Accordion, { accordionClasses } from "@mui/material/Accordion";
import { Box, Link, Stack, Avatar, Button, Divider, LinearProgress } from "@mui/material";
import AccordionSummary, { accordionSummaryClasses } from "@mui/material/AccordionSummary";

import { fCurrency, fShortenNumber } from "src/utils/format-number";

import Label from "src/components/label";
import Iconify from "src/components/iconify";

import { ICourseLessonProp } from "src/types/course";

import Repository from "../repository/repository";

// ----------------------------------------------------------------------

type LessonItemProps = {
  lesson: Pick<
    ICourseLessonProp,
    "id" | "title" | "bestSeller" | "price" | "priceSale" | "lowest30DaysPrice"
  >;
  details: ICourseLessonProp;
  expanded: boolean;
  onExpanded: (event: React.SyntheticEvent, isExpanded: boolean) => void;
  loading: boolean;
};

export default function CourseDetailsLessonItem({
  lesson,
  details,
  expanded,
  onExpanded,
  loading,
}: LessonItemProps) {
  const genderAvatarUrl =
    details?.teachers?.[0]?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = details?.teachers?.[0]?.avatarUrl
    ? details?.teachers?.[0]?.avatarUrl
    : genderAvatarUrl;
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
        <Typography
          variant="subtitle1"
          sx={{
            flexGrow: 1,
          }}
        >
          {lesson.title}
        </Typography>

        {lesson.bestSeller && (
          <Label color="warning" variant="filled" sx={{ textTransform: "uppercase", mr: 2 }}>
            Bestseller
          </Label>
        )}

        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h6" sx={{ textAlign: "right" }}>
            {lesson?.priceSale && (
              <Box
                component="span"
                sx={{
                  mr: 0.5,
                  color: "text.disabled",
                  textDecoration: "line-through",
                }}
              >
                {fCurrency(lesson.priceSale)}
              </Box>
            )}
            {lesson?.price ? fCurrency(lesson.price) : null}
            {lesson?.priceSale && lesson?.lowest30DaysPrice && (
              <Typography sx={{ fontSize: 10, color: "text.disabled", textAlign: "center" }}>
                Najniższa cena z 30 dni przed: {fCurrency(lesson.lowest30DaysPrice)}
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
        {loading ? (
          <LinearProgress />
        ) : (
          <Stack spacing={3}>
            <Typography sx={{ color: "text.secondary", textAlign: "justify" }}>
              {details?.description}
            </Typography>

            <Stack
              spacing={1.5}
              direction="row"
              alignItems="center"
              divider={<Divider orientation="vertical" sx={{ height: 20 }} />}
            >
              {details?.duration && (
                <Stack spacing={2}>
                  <Stack
                    direction="row"
                    flexWrap="wrap"
                    sx={{
                      "& > *": { my: 0.5 },
                    }}
                  >
                    <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                      <Iconify icon="carbon:time" sx={{ mr: 1 }} /> {details.duration}{" "}
                      {polishPlurals("minuta", "minuty", "minut", details.duration)}
                    </Stack>
                  </Stack>
                </Stack>
              )}

              {details?.totalReviews && (
                <Stack spacing={0.5} direction="row" alignItems="center">
                  <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                  <Box sx={{ typography: "h6" }}>
                    {Number.isInteger(details.ratingNumber)
                      ? `${details.ratingNumber}.0`
                      : details.ratingNumber}
                  </Box>

                  {details?.totalReviews && (
                    <Link variant="body2" sx={{ color: "text.secondary" }}>
                      ({fShortenNumber(details.totalReviews)}{" "}
                      {polishPlurals("recenzja", "recenzje", "recenzji", details.totalReviews)})
                    </Link>
                  )}
                </Stack>
              )}

              {details?.totalStudents && (
                <Stack direction="row" sx={{ typography: "subtitle2" }}>
                  {fShortenNumber(details.totalStudents)}
                  <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                    {polishPlurals("student", "studentów", "studentów", details.totalStudents)}
                  </Box>
                </Stack>
              )}
            </Stack>

            {details?.teachers && (
              <Stack direction="row" alignItems="center">
                <Avatar src={avatarUrl} />
                <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                  {details.teachers[0]?.name}
                </Typography>
                {details.teachers?.length > 1 && (
                  <Link underline="always" color="text.secondary" variant="body2">
                    + {details.teachers.length - 1}{" "}
                    {polishPlurals(
                      "nauczyciel",
                      "nauczycieli",
                      "nauczycieli",
                      details.teachers.length - 1,
                    )}
                  </Link>
                )}
              </Stack>
            )}

            {details?.githubUrl && (
              <Stack direction="row" flexWrap="wrap">
                <Repository githubUrl={details.githubUrl} />
              </Stack>
            )}

            <Divider sx={{ borderStyle: "dashed" }} />

            <Stack direction="row" spacing={2} flexWrap="wrap" justifyContent="right">
              <Button variant="text" size="large" color="info">
                Sprawdź terminy
              </Button>

              <Button
                size="large"
                color="inherit"
                variant="contained"
                startIcon={<Iconify icon="carbon:shopping-cart-plus" />}
              >
                Dodaj do koszyka
              </Button>
            </Stack>
          </Stack>
        )}
      </AccordionDetails>
    </Accordion>
  );
}
