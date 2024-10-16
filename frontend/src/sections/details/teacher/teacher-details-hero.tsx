import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

import { useBoolean } from "src/hooks/use-boolean";

import { fNumber, fShortenNumber } from "src/utils/format-number";

import Image from "src/components/image";
import Iconify from "src/components/iconify";
import { useUserContext } from "src/components/user";
import CustomBreadcrumbs from "src/components/custom-breadcrumbs";

import { UserType } from "src/types/user";
import { ITeamMemberProps } from "src/types/team";

import MessageForm from "./message-form";

// ----------------------------------------------------------------------

type Props = {
  teacher: ITeamMemberProps;
};

export default function TeacherDetailsHero({ teacher }: Props) {
  const {
    name,
    description,
    role,
    linkedinUrl,
    avatarUrl,
    totalHours,
    totalReviews,
    ratingNumber,
    totalStudents,
    lessons,
  } = teacher;

  const sendMessageFormOpen = useBoolean();

  const { isLoggedIn, userType } = useUserContext();

  const genderAvatarUrl =
    teacher.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";
  const photoUrl = avatarUrl || genderAvatarUrl;

  return (
    <Box
      sx={{
        bgcolor: "background.neutral",
        pb: { xs: 5, md: 10 },
      }}
    >
      <Container sx={{ overflow: "hidden" }}>
        <CustomBreadcrumbs
          links={[
            { name: "Strona główna", href: "/" },
            { name: "Instruktorzy", href: paths.teachers },
            { name: name || "" },
          ]}
          sx={{
            pt: 5,
            mb: { xs: 5, md: 10 },
          }}
        />

        <Grid container spacing={{ xs: 5, md: 10 }} direction="row-reverse">
          <Grid xs={12} md={5}>
            <Stack
              alignItems="center"
              justifyContent="center"
              sx={{
                position: "relative",
                borderRadius: 2,
                overflow: "hidden",
              }}
            >
              <Image alt="hero" src={photoUrl} />
            </Stack>
          </Grid>

          <Grid xs={12} md={7}>
            <Stack spacing={3}>
              <Stack spacing={2} alignItems="flex-start">
                <Typography variant="overline" sx={{ color: "primary.main" }}>
                  {role}
                </Typography>

                <Typography variant="h3" component="h1">
                  {name}
                </Typography>

                <Typography sx={{ color: "text.secondary", textAlign: "justify" }}>
                  {description}
                </Typography>
              </Stack>

              <Stack spacing={2}>
                <Stack
                  direction="row"
                  flexWrap="wrap"
                  sx={{
                    "& > *": { my: 0.5, mr: 3 },
                  }}
                >
                  {linkedinUrl && (
                    <Stack spacing={1}>
                      <Stack direction="row" alignItems="center" sx={{ typography: "subtitle2" }}>
                        <Iconify
                          icon="carbon:logo-linkedin"
                          width={24}
                          sx={{ mr: 1 }}
                          color="#007EBB"
                        />
                        LinkedIn
                      </Stack>

                      <Link color="inherit" variant="body2" href={linkedinUrl} target="_blank">
                        Zobacz profil
                      </Link>
                    </Stack>
                  )}

                  <Stack spacing={1}>
                    <Stack direction="row" alignItems="center" sx={{ typography: "subtitle2" }}>
                      <Iconify icon="carbon:email" width={24} sx={{ mr: 1 }} />
                      Kontakt
                    </Stack>

                    {isLoggedIn ? (
                      <Link
                        color="inherit"
                        variant="body2"
                        onClick={() => {
                          if (userType === UserType.Student) {
                            sendMessageFormOpen.onToggle();
                          }
                        }}
                        sx={{ cursor: "pointer" }}
                      >
                        Napisz do mnie
                      </Link>
                    ) : (
                      <Link
                        color="inherit"
                        variant="body2"
                        href={paths.login}
                        sx={{ cursor: "pointer" }}
                      >
                        Napisz do mnie
                      </Link>
                    )}
                  </Stack>
                </Stack>
              </Stack>

              <Divider sx={{ borderStyle: "dashed" }} />

              <Stack
                spacing={1.5}
                direction="row"
                alignItems="center"
                divider={<Divider orientation="vertical" sx={{ height: 20 }} />}
              >
                {ratingNumber && totalReviews && (
                  <Stack spacing={0.5} direction="row" alignItems="center">
                    <Iconify icon="carbon:star-filled" sx={{ color: "warning.main" }} />
                    <Box sx={{ typography: "h6" }}>
                      {Number.isInteger(ratingNumber)
                        ? `${ratingNumber}.0`
                        : fNumber(ratingNumber, 1)}
                    </Box>

                    {totalReviews && (
                      <Typography variant="body2" sx={{ color: "text.secondary" }}>
                        ({fShortenNumber(totalReviews)}{" "}
                        {polishPlurals("recenzja", "recenzje", "recenzji", totalReviews)})
                      </Typography>
                    )}
                  </Stack>
                )}

                {totalStudents && (
                  <Stack direction="row" sx={{ typography: "subtitle2" }}>
                    {fShortenNumber(totalStudents)}
                    <Box component="span" typography="body2" sx={{ ml: 0.5 }}>
                      {polishPlurals("student", "studentów", "studentów", totalStudents)}
                    </Box>
                  </Stack>
                )}
              </Stack>

              <Stack spacing={2}>
                <Stack
                  direction="row"
                  flexWrap="wrap"
                  sx={{
                    "& > *": { my: 0.5, mr: 3 },
                  }}
                >
                  <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                    <Iconify icon="carbon:time" sx={{ mr: 1 }} />{" "}
                    {(totalHours ?? 0) < 1
                      ? totalHours
                      : fShortenNumber(Math.floor(totalHours ?? 0), 0)}
                    + {polishPlurals("godzina", "godziny", "godzin", totalHours ?? 0)}
                  </Stack>

                  {lessons && lessons.length > 0 && (
                    <Stack direction="row" alignItems="center" sx={{ typography: "body2" }}>
                      <Iconify icon="carbon:document" sx={{ mr: 1 }} />
                      {`${lessons.length} ${polishPlurals(
                        "lekcja",
                        "lekcje",
                        "lekcji",
                        lessons.length,
                      )}`}
                    </Stack>
                  )}
                </Stack>
              </Stack>
            </Stack>
          </Grid>
        </Grid>
      </Container>

      <MessageForm
        teacher={teacher}
        open={sendMessageFormOpen.value}
        onClose={sendMessageFormOpen.onFalse}
      />
    </Box>
  );
}
