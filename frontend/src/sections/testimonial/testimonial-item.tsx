import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import { Box, BoxProps } from "@mui/material";
import Typography from "@mui/material/Typography";

import Iconify from "src/components/iconify";

import { ITestimonialProps } from "src/types/testimonial";

// ----------------------------------------------------------------------

type TestimonialItemContentProps = {
  testimonial: ITestimonialProps;
};

export function TestimonialItemContent({ testimonial }: TestimonialItemContentProps) {
  const { review } = testimonial;

  return (
    <Stack alignItems="center">
      <Iconify
        icon="carbon:quotes"
        sx={{ width: 48, height: 48, opacity: 0.48, color: "primary.main" }}
      />

      <Typography
        sx={{
          mt: 2,
          mb: 5,
          lineHeight: 1.75,
          fontSize: { xs: 20, md: 24 },
          fontFamily: (theme) => theme.typography.h1.fontFamily,
        }}
      >
        {review}
      </Typography>
    </Stack>
  );
}

// ----------------------------------------------------------------------

type TestimonialItemThumbnailProps = BoxProps & {
  selected: boolean;
  testimonial: ITestimonialProps;
};

export function TestimonialItemThumbnail({
  sx,
  selected,
  testimonial,
  ...other
}: TestimonialItemThumbnailProps) {
  const genderAvatarUrl =
    testimonial.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = testimonial.avatarUrl || genderAvatarUrl;

  return (
    <Box
      display="flex"
      alignItems="center"
      justifyContent="center"
      sx={{ width: 96, height: 96, ...sx }}
      {...other}
    >
      <Avatar
        src={avatarUrl}
        sx={{
          width: 48,
          height: 48,
          opacity: 0.48,
          cursor: "pointer",
          transition: (theme) => theme.transitions.create(["width", "height"]),
          ...(selected && { width: 1, height: 1, opacity: 1 }),
        }}
      />
    </Box>
  );
}
