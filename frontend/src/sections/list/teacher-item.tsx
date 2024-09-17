import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fShortenNumber } from "src/utils/format-number";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import TextMaxLine from "src/components/text-max-line";

import { ITeamMemberProps } from "src/types/team";

// ----------------------------------------------------------------------

type Props = {
  teacher: ITeamMemberProps;
  vertical?: boolean;
};

export default function TeacherItem({ teacher, vertical }: Props) {
  const {
    id,
    name,
    role,
    description,
    avatarUrl,
    gender,
    ratingNumber,
    totalReviews,
    totalLessons,
    totalHours,
    totalStudents,
  } = teacher;

  const genderAvatarUrl =
    gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const photoUrl = avatarUrl || genderAvatarUrl;

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
          alt={name}
          src={photoUrl}
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

      <Stack spacing={3} sx={{ p: 3 }}>
        <Stack
          spacing={{
            xs: 3,
            sm: vertical ? 3 : 1,
          }}
        >
          <Stack direction="row" alignItems="center" justifyContent="space-between">
            <Typography variant="overline" sx={{ color: "primary.main" }}>
              {role}
            </Typography>
          </Stack>

          <Stack spacing={1}>
            <Link component={RouterLink} href={`${paths.teacher}/${id}`} color="inherit">
              <TextMaxLine variant="h6" line={1}>
                {name}
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
          {ratingNumber && ratingNumber > 0 && totalReviews && totalReviews > 0 && (
            <Stack spacing={0.5} direction="row" alignItems="center">
              {ratingNumber && ratingNumber > 0 && (
                <>
                  <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                  <Box sx={{ typography: "h6" }}>
                    {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
                  </Box>
                </>
              )}

              {totalReviews && totalReviews > 0 && (
                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  ({fShortenNumber(totalReviews)}{" "}
                  {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
                </Typography>
              )}
            </Stack>
          )}

          {totalStudents && totalStudents > 0 && (
            <Stack direction="row" sx={{ typography: "subtitle2" }}>
              {fShortenNumber(totalStudents)}
              <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                {polishPlurals("student", "studentów", "studentów", totalStudents)}
              </Box>
            </Stack>
          )}
        </Stack>

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
          {(totalLessons ?? 0) > 0 && (
            <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
              <Iconify icon="carbon:document" sx={{ mr: 1 }} />
              {`${totalLessons} ${polishPlurals("lekcja", "lekcje", "lekcji", totalLessons ?? 0)}`}
            </Stack>
          )}

          {(totalHours ?? 0) > 0 && (
            <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
              <Iconify icon="carbon:time" sx={{ mr: 1 }} />
              {(totalHours ?? 0) < 1
                ? totalHours
                : fShortenNumber(Math.floor(totalHours ?? 0), 0)}+{" "}
              {polishPlurals("godzina", "godziny", "godzin", totalHours ?? 0)}
            </Stack>
          )}
        </Stack>
      </Stack>
    </Card>
  );
}
