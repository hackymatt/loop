import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import { AvatarGroup } from "@mui/material";
import Container from "@mui/material/Container";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fDate } from "src/utils/format-time";

import Image from "src/components/image";

import { IAuthorProps } from "src/types/author";
import type { IPostProps } from "src/types/blog";

import { PostTime } from "./post-time";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  post: IPostProps;
};

export function FeaturedPost({ post, sx, ...other }: Props) {
  return (
    <Link component={RouterLink} href={paths.post} color="inherit" variant="h3" underline="none">
      <Box
        component="section"
        sx={{
          py: 10,
          bgcolor: "background.neutral",
          ...sx,
        }}
        {...other}
      >
        <Container>
          <Box display="flex" flexDirection={{ xs: "column", md: "row" }}>
            <Image
              src={post.coverUrl}
              alt={post.title}
              sx={{ flexGrow: 1, height: 560, borderRadius: 2 }}
            />

            <Stack
              spacing={1}
              sx={{
                mx: "auto",
                pl: { md: 8 },
                py: { xs: 3, md: 5 },
                maxWidth: { md: 408 },
              }}
            >
              <PostTime createdAt={fDate(post.createdAt)} duration={post.duration} />

              {post.title}

              <Typography sx={{ color: "text.secondary", flexGrow: 1 }}>
                {post.description}
              </Typography>

              <Box
                gap={1.5}
                display="flex"
                alignItems="center"
                sx={{ pt: 1.5, typography: "body2" }}
              >
                <AvatarGroup total={post.authors.length} max={1}>
                  {post.authors.map((author: IAuthorProps) => {
                    const genderAvatarUrl =
                      author?.gender === "Kobieta"
                        ? "/assets/images/avatar/avatar_female.jpg"
                        : "/assets/images/avatar/avatar_male.jpg";

                    const avatarUrl = author?.avatarUrl || genderAvatarUrl;
                    return <Avatar key={author.id} src={avatarUrl} />;
                  })}
                </AvatarGroup>
                {post.authors[0].name}
                {post.authors.length > 1 && (
                  <Typography
                    color="text.secondary"
                    variant="body2"
                    sx={{ textDecoration: "underline" }}
                  >
                    + {post.authors.length - 1}{" "}
                    {polishPlurals("autor", "autorów", "autorów", post.authors.length - 1)}
                  </Typography>
                )}
              </Box>
            </Stack>
          </Box>
        </Container>
      </Box>
    </Link>
  );
}
