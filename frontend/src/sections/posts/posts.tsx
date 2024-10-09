import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Paper from "@mui/material/Paper";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import { AvatarGroup } from "@mui/material";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import type { PaperProps } from "@mui/material/Paper";
import Pagination, { paginationClasses } from "@mui/material/Pagination";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fDate } from "src/utils/format-time";

import Image from "src/components/image";
import TextMaxLine from "src/components/text-max-line/text-max-line";

import { IAuthorProps } from "src/types/author";
import type { IPostProps } from "src/types/blog";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  posts: IPostProps[];
  pagesCount?: number;
  page: number;
  onPageChange: (selectedPage: number) => void;
};

export function Posts({ posts, pagesCount, page, onPageChange, sx, ...other }: Props) {
  return (
    <>
      <Box
        display="grid"
        columnGap={4}
        rowGap={{ xs: 4, md: 5 }}
        gridTemplateColumns={{
          xs: "repeat(1, 1fr)",
          sm: "repeat(2, 1fr)",
        }}
        sx={sx}
        {...other}
      >
        {posts.map((post) => (
          <PostItem key={post.id} post={post} />
        ))}
      </Box>

      {posts?.length > 0 && (
        <Pagination
          count={pagesCount ?? 0}
          page={page}
          sx={{
            my: 10,
            [`& .${paginationClasses.ul}`]: {
              justifyContent: "center",
            },
          }}
          onChange={(event, selectedPage: number) => onPageChange(selectedPage)}
        />
      )}
    </>
  );
}

// ----------------------------------------------------------------------

type PostItemProps = PaperProps & {
  post: IPostProps;
};

export function PostItem({ post, sx, ...other }: PostItemProps) {
  return (
    <Link component={RouterLink} href={paths.post} color="inherit" underline="none">
      <Paper
        variant="outlined"
        sx={{
          borderRadius: 2,
          overflow: "hidden",
          bgcolor: "transparent",
          ...sx,
        }}
        {...other}
      >
        <Image src={post.coverUrl} alt={post.title} ratio="1/1" />

        <Box display="flex" gap={3} sx={{ p: 3 }}>
          <Box sx={{ textAlign: "center" }}>
            <Typography variant="subtitle2" component="span">
              {fDate(post.createdAt, "MMM")}
            </Typography>
            <Divider sx={{ mt: 1, mb: 0.5 }} />
            <Typography variant="h3" component="span">
              {fDate(post.createdAt, "dd")}
            </Typography>
          </Box>

          <Box gap={1} display="flex" flexDirection="column" flex="1 1 auto">
            <TextMaxLine variant="h6" line={2}>
              {post.title}
            </TextMaxLine>

            <TextMaxLine variant="body2" line={2}>
              {post.description}
            </TextMaxLine>

            <Box gap={1.5} display="flex" alignItems="center" sx={{ pt: 1.5 }}>
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
              <Box gap={0.5} display="flex" flexDirection="column">
                <Box component="span" sx={{ typography: "body2" }}>
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
                <Typography variant="caption" sx={{ color: "text.disabled" }}>
                  {post.duration}
                </Typography>
              </Box>
            </Box>
          </Box>
        </Box>
      </Paper>
    </Link>
  );
}
