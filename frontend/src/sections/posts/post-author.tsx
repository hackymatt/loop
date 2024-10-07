import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import type { IAuthorProps } from "src/types/author";

// ----------------------------------------------------------------------

type PostAuthorProps = BoxProps & {
  author?: IAuthorProps;
};

export function PostAuthor({ author, sx, ...other }: PostAuthorProps) {
  return (
    <Box
      display="flex"
      gap={{ xs: 3, md: 4 }}
      sx={{
        py: { xs: 5, md: 10 },
        ...sx,
      }}
      {...other}
    >
      <Avatar src={author?.avatarUrl} sx={{ width: 96, height: 96 }} />

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
              {author?.title}
            </Typography>
          </Stack>
        </Stack>
      </Stack>
    </Box>
  );
}
