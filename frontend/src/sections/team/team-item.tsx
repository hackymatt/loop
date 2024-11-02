import { useMemo } from "react";

import Box from "@mui/material/Box";
import { Link } from "@mui/material";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { encodeUrl } from "src/utils/url-utils";
import { getGenderAvatar } from "src/utils/get-gender-avatar";

import Image from "src/components/image";

import { ITeamMemberProps } from "src/types/team";

// ----------------------------------------------------------------------

type Props = {
  member: ITeamMemberProps;
};

export default function TeamItem({ member }: Props) {
  const { id, name, role, avatarUrl, gender } = member;

  const genderAvatarUrl = getGenderAvatar(gender);

  const photoUrl = avatarUrl || genderAvatarUrl;

  const path = useMemo(() => `${name}-${id}`, [id, name]);

  return (
    <Link
      component={RouterLink}
      href={`${paths.teacher}/${encodeUrl(path)}`}
      color="inherit"
      underline="none"
    >
      <Card>
        <Stack spacing={0.5} sx={{ textAlign: "center", pt: 3, pb: 1.5 }}>
          <Typography variant="h6">{name}</Typography>

          <Typography variant="body2" sx={{ color: "text.disabled" }}>
            {role}
          </Typography>
        </Stack>

        <Box sx={{ position: "relative" }}>
          <Shape />

          <Image src={photoUrl} alt={name} ratio="1/1" />
        </Box>
      </Card>
    </Link>
  );
}

// ----------------------------------------------------------------------

function Shape() {
  return (
    <Box
      sx={{
        top: 0,
        width: 1,
        height: 8,
        zIndex: 9,
        position: "absolute",
        color: "background.paper",
      }}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="1080" height="32" viewBox="0 0 1080 32">
        <path fill="currentColor" d="M1080 32L0 0h1080v32z" />
      </svg>
    </Box>
  );
}
