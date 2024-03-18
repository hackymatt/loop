import Box from "@mui/system/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Rating from "@mui/material/Rating";
import Divider from "@mui/material/Divider";
import Typography from "@mui/material/Typography";

import { fDate } from "src/utils/format-time";

import { IReviewItemProp } from "src/types/review";

// ----------------------------------------------------------------------

const AVATAR_SIZE = 64;

const WIDTH = `calc(100% - ${AVATAR_SIZE + 20}px)`;

type IProps = Partial<IReviewItemProp> & { showTeacher?: boolean };

export default function ReviewItem({
  name,
  gender,
  rating,
  message,
  createdAt,
  avatarUrl,
  lessonTitle,
  teacherName,
  showTeacher = true,
}: IProps) {
  const genderAvatarUrl =
    gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const studentAvatarUrl = avatarUrl || genderAvatarUrl;

  return (
    <>
      <Stack
        direction="row"
        sx={{
          py: 3,
          alignItems: "flex-start",
        }}
      >
        <Avatar
          alt={name}
          src={studentAvatarUrl}
          sx={{ width: AVATAR_SIZE, height: AVATAR_SIZE, mr: 2.5 }}
        />

        <Stack sx={{ width: 1 }}>
          <Stack
            spacing={1}
            alignItems={{ sm: "center" }}
            direction={{ xs: "column", sm: "row" }}
            justifyContent={{ sm: "space-between" }}
          >
            <Typography variant="subtitle2">{name}</Typography>
            <Rating size="small" value={rating} precision={0.5} readOnly />
          </Stack>

          <Stack direction="row" alignItems="center" spacing={2}>
            <Typography
              variant="body2"
              sx={{
                mb: 1,
                mt: { xs: 1, sm: 0.5 },
                color: "text.disabled",
              }}
            >
              {lessonTitle}
            </Typography>

            {showTeacher && (
              <>
                <Box
                  sx={{
                    width: 4,
                    height: 4,
                    bgcolor: "text.disabled",
                    borderRadius: "50%",
                  }}
                />
                <Typography
                  variant="body2"
                  sx={{
                    mb: 1,
                    mt: { xs: 1, sm: 0.5 },
                    color: "text.disabled",
                  }}
                >
                  {teacherName}
                </Typography>
              </>
            )}

            <Box
              sx={{
                width: 4,
                height: 4,
                bgcolor: "text.disabled",
                borderRadius: "50%",
              }}
            />

            <Typography
              variant="body2"
              sx={{
                mb: 1,
                mt: { xs: 1, sm: 0.5 },
                color: "text.disabled",
              }}
            >
              {fDate(createdAt)}
            </Typography>
          </Stack>

          <Typography variant="body2">{message}</Typography>
        </Stack>
      </Stack>

      <Divider sx={{ ml: "auto", width: WIDTH }} />
    </>
  );
}
