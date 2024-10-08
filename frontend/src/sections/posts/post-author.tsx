import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import { Link, Paper, IconButton } from "@mui/material";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { encodeUrl } from "src/utils/url-utils";

import Iconify from "src/components/iconify";

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
      gap={{ xs: 1.5, md: 2 }}
      sx={{
        py: { xs: 2.5, md: 5 },
        ...sx,
      }}
      {...other}
    >
      {authors.map((author: IAuthorProps) => {
        const path = `${author.name.toLowerCase()}-${author.id}`;
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
                  <Avatar src={author?.avatarUrl} sx={{ width: 56, height: 56 }} />
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
                <IconButton component="a" href={author.linkedinUrl} target="_blank">
                  <Iconify icon="carbon:logo-linkedin" color="#007EBB" />
                </IconButton>
              </Stack>
            </Paper>
          </Link>
        );
      })}
    </Box>
  );
}
