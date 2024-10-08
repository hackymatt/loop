import { useMemo } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import { Link, Paper } from "@mui/material";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { encodeUrl } from "src/utils/url-utils";

import type { IAuthorProps } from "src/types/author";

// ----------------------------------------------------------------------

type PostAuthorsProps = BoxProps & {
  authors: IAuthorProps[];
};

export function PostAuthors({ authors, sx, ...other }: PostAuthorsProps) {
  return (
    <Box
      sx={{
        display: "grid",
        gap: { xs: 1, md: 2 },
        gridTemplateColumns: {
          xs: "repeat(1, 1fr)",
          lg: "repeat(2, 1fr)",
        },
        py: { xs: 2.5, md: 5 },
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
    <Link
      component={RouterLink}
      href={`${paths.teacher}/${encodeUrl(path)}`}
      color="inherit"
      underline="none"
    >
      <Paper variant="outlined" sx={{ p: 3, borderRadius: 2 }}>
        <Stack direction="row" spacing={2} justifyContent="space-between">
          <Stack spacing={2} direction="row">
            <Avatar src={avatarUrl} sx={{ width: 56, height: 56 }} />
            <Stack spacing={2}>
              <Stack
                spacing={2}
                alignItems={{ md: "center" }}
                direction={{ xs: "column", md: "row" }}
                justifyContent={{ md: "space-between" }}
              >
                <Stack spacing={0.5}>
                  <Typography variant="h5">{author?.name}</Typography>

                  <Typography variant="body2" sx={{ color: "text.secondary" }}>
                    {author?.role}
                  </Typography>
                </Stack>
              </Stack>
            </Stack>
          </Stack>
        </Stack>
      </Paper>
    </Link>
  );
}
