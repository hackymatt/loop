import { useMemo } from "react";

import Box from "@mui/material/Box";
import { Button } from "@mui/material";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";

import { fDate } from "src/utils/format-time";
import { encodeUrl } from "src/utils/url-utils";

import TextMaxLine from "src/components/text-max-line";

import type { IAuthorProps } from "src/types/author";

// ----------------------------------------------------------------------

type PostAuthorsProps = BoxProps & {
  authors: IAuthorProps[];
};

export function PostAuthors({ authors, sx, ...other }: PostAuthorsProps) {
  return (
    <Box
      display="flex"
      flexDirection="column"
      gap={{ xs: 3, md: 4 }}
      sx={{
        py: { xs: 5, md: 10 },
        ...sx,
      }}
      {...other}
    >
      {authors.map((author) => (
        <PostAuthorItem key={author.id} author={author} />
      ))}
    </Box>
  );
}

// ----------------------------------------------------------------------

type PostAuthorItemProps = {
  author: IAuthorProps;
};

function PostAuthorItem({ author }: PostAuthorItemProps) {
  const genderAvatarUrl =
    author?.gender === "Kobieta"
      ? "/assets/images/avatar/avatar_female.jpg"
      : "/assets/images/avatar/avatar_male.jpg";

  const avatarUrl = author?.avatarUrl || genderAvatarUrl;

  const path = useMemo(() => `${author.name.toLowerCase()}-${author.id}`, [author.id, author.name]);

  return (
    <Box display="flex" gap={{ xs: 3, md: 4 }}>
      <Avatar src={avatarUrl} sx={{ width: 96, height: 96 }} />
      <Stack spacing={2}>
        <Stack
          spacing={2}
          alignItems={{ md: "center" }}
          direction={{ xs: "column", md: "row" }}
          justifyContent={{ md: "space-between" }}
        >
          <Stack spacing={0.5}>
            <Typography variant="h5">{author.name}</Typography>

            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              {author.role}
            </Typography>
          </Stack>

          <Box display="flex">
            <Button href={`${paths.teacher}/${encodeUrl(path)}`} variant="text" color="primary">
              Zobacz profil
            </Button>
          </Box>
        </Stack>

        <TextMaxLine line={2} variant="body2" sx={{ color: "text.secondary" }}>
          {author.description}
        </TextMaxLine>

        <Typography variant="caption" sx={{ color: "text.disabled" }}>
          {`Uczy w loop od ${fDate(author.dateJoined, "d MMMM yyyy")}`}
        </Typography>
      </Stack>
    </Box>
  );
}
