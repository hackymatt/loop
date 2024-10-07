"use client";

import Fab from "@mui/material/Fab";
import Box from "@mui/material/Box";
import { alpha } from "@mui/system";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import Divider from "@mui/material/Divider";
import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";

import { paths } from "src/routes/paths";

import { fDate } from "src/utils/format-time";

import { _coursePosts } from "src/_mock";

import Iconify from "src/components/iconify";
import { Markdown } from "src/components/markdown";
import CustomBreadcrumbs from "src/components/custom-breadcrumbs";

import { PostAuthor } from "../posts/post-author";
import Newsletter from "../newsletter/newsletter";
import { LatestPosts } from "../posts/latest-posts";
import { PrevNextButton } from "../posts/post-prev-and-next";

// ----------------------------------------------------------------------

const post = _coursePosts[0];
const prevPost = _coursePosts[1];
const nextPost = _coursePosts[2];
const latestPosts = _coursePosts.slice(3, 6);

export function PostView() {
  const renderToolbar = (
    <Box
      gap={1.5}
      display="flex"
      sx={(theme) => ({
        py: 3,
        my: 5,
        borderTop: `solid 1px ${theme.palette.divider}`,
        borderBottom: `solid 1px ${theme.palette.divider}`,
      })}
    >
      <Avatar src={post.author.avatarUrl} sx={{ width: 48, height: 48 }} />

      <Stack spacing={0.5} flexGrow={1}>
        <Typography variant="subtitle2">{post.author.name}</Typography>
        <Typography variant="caption" sx={{ color: "text.secondary" }}>
          {fDate(post.createdAt)}
        </Typography>
      </Stack>

      <Box display="flex" alignItems="center">
        <IconButton>
          <Iconify icon="solar:share-outline" />
        </IconButton>
      </Box>
    </Box>
  );

  return (
    <>
      <Divider />

      <Container>
        <CustomBreadcrumbs
          links={[
            { name: "Home", href: "/" },
            { name: "Blog", href: paths.posts },
            { name: post.title },
          ]}
          sx={{ my: { xs: 3, md: 5 } }}
        />

        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          sx={(theme) => ({
            borderRadius: 2,
            overflow: "hidden",
            position: "relative",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            aspectRatio: { xs: "16/9", md: "21/9" },
            backgroundImage: `linear-gradient(to bottom, ${alpha(theme.palette.common.black, 0)} 0%, ${theme.palette.common.black} 75%), url(${post.heroUrl})`,
          })}
        >
          <Fab color="primary" sx={{ zIndex: 9, position: "absolute" }}>
            <Iconify width={22} icon="solar:play-outline" />
          </Fab>
        </Box>

        <Grid container disableEqualOverflow spacing={3} justifyContent={{ md: "center" }}>
          <Grid xs={12} md={8}>
            <Stack
              spacing={3}
              sx={{
                textAlign: "center",
                mt: { xs: 5, md: 10 },
              }}
            >
              <Typography variant="body2" sx={{ color: "text.disabled" }}>
                {post.duration}
              </Typography>

              <Typography variant="h2" component="h1">
                {post.title}
              </Typography>

              <Typography variant="h5">{post.description}</Typography>
            </Stack>

            {renderToolbar}

            <Markdown content={post.content} firstLetter />

            <Divider sx={{ mt: 10 }} />

            <PostAuthor author={post.author} />

            <Divider />

            <Box
              gap={5}
              display="grid"
              gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
              sx={{ py: 10 }}
            >
              <PrevNextButton title={prevPost?.title} coverUrl={prevPost?.coverUrl} href="#" />
              <PrevNextButton
                isNext
                title={nextPost?.title}
                coverUrl={nextPost?.coverUrl}
                href="#"
              />
            </Box>
          </Grid>
        </Grid>
      </Container>

      <Divider />

      <LatestPosts posts={latestPosts} />

      <Newsletter />
    </>
  );
}
