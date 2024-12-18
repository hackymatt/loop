"use client";

import { useMemo } from "react";
import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";
import Typography from "@mui/material/Typography";
import { Avatar, IconButton, AvatarGroup } from "@mui/material";

import { paths } from "src/routes/paths";

import { fDate } from "src/utils/format-time";
import { decodeUrl, encodeUrl } from "src/utils/url-utils";
import { createMetadata } from "src/utils/create-metadata";
import { getGenderAvatar } from "src/utils/get-gender-avatar";

import { usePost } from "src/api/posts/post";
import { usePosts } from "src/api/posts/posts";

import Iconify from "src/components/iconify";
import { Markdown } from "src/components/markdown";
import { SplashScreen } from "src/components/loading-screen";
import CustomBreadcrumbs from "src/components/custom-breadcrumbs";

import { IAuthorProps } from "src/types/author";

import { PostTags } from "../posts/post-tags";
import Newsletter from "../newsletter/newsletter";
import { PostAuthors } from "../posts/post-author";
import NotFoundView from "../error/not-found-view";
import { LatestPosts } from "../posts/latest-posts";
import { PrevNextButton } from "../posts/post-prev-and-next";

// ----------------------------------------------------------------------

export function PostView({ id }: { id: string }) {
  const decodedId = decodeUrl(id);
  const recordId = decodedId.slice(decodedId.lastIndexOf("-") + 1);

  const { data: post, isLoading: isLoadingPost } = usePost(recordId);

  const { data: recentPosts } = usePosts({
    sort_by: "-publication_date",
    page_size: 3,
  });

  const prevPost = useMemo(() => post?.previousPost, [post?.previousPost]);
  const nextPost = useMemo(() => post?.nextPost, [post?.nextPost]);

  const isLoading = isLoadingPost;

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
      <AvatarGroup total={post?.authors?.length ?? 0} max={1}>
        {post?.authors?.map((author: IAuthorProps) => {
          const genderAvatarUrl = getGenderAvatar(author?.gender);

          const avatarUrl = author?.avatarUrl || genderAvatarUrl;
          return <Avatar key={author.id} src={avatarUrl} />;
        })}
      </AvatarGroup>

      <Stack spacing={0.5} flexGrow={1} typography="subtitle2">
        <Stack direction="row" spacing={0.5}>
          {post?.authors?.[0].name}
          {(post?.authors?.length ?? 0) > 1 && (
            <Typography
              color="text.secondary"
              variant="subtitle2"
              sx={{ textDecoration: "underline" }}
            >
              + {(post?.authors?.length ?? 0) - 1}{" "}
              {polishPlurals("autor", "autorów", "autorów", (post?.authors?.length ?? 0) - 1)}
            </Typography>
          )}
        </Stack>
        <Typography variant="caption" sx={{ color: "text.secondary" }}>
          {fDate(post?.publicationDate, "d MMMM yyyy")}
        </Typography>
      </Stack>

      <Box display="flex" alignItems="center">
        <IconButton
          onClick={() => navigator.share({ url: id, title: post?.title, text: post?.description })}
        >
          <Iconify icon="solar:share-outline" />
        </IconButton>
      </Box>
    </Box>
  );

  const metadata = useMemo(
    () =>
      createMetadata(
        `${post?.title} - przeczytaj artykuł już teraz`,
        `Przeczytaj nasz artykuł o ${post?.title}. ${post?.description} Dowiedz się, jak ${post?.description.toLowerCase()}. Odkryj praktyczne porady i najlepsze praktyki, które pomogą Ci w rozwoju umiejętności programistycznych.`,
        [
          post?.title,
          post?.description,
          "programowanie",
          "nauka programowania",
          "najlepsze praktyki",
          "porady programistyczne",
          "szkoła programowania",
          "loop",
        ],
      ),
    [post?.description, post?.title],
  );

  if (isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(post).length === 0) {
    return <NotFoundView />;
  }

  return (
    <>
      <title>{metadata.title}</title>
      <meta name="description" content={metadata.description} />
      <meta name="keywords" content={metadata.keywords} />

      <Container>
        <CustomBreadcrumbs
          links={[
            { name: "Strona główna", href: "/" },
            { name: "Blog", href: paths.posts },
            { name: post?.title },
          ]}
          sx={{ my: { xs: 3, md: 5 } }}
        />

        <Box
          display="flex"
          alignItems="center"
          justifyContent="center"
          sx={{
            borderRadius: 2,
            overflow: "hidden",
            position: "relative",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            aspectRatio: { xs: "16/9", md: "21/9" },
            backgroundImage: `url(${post?.coverUrl})`,
          }}
        />

        <Grid container disableEqualOverflow spacing={3} justifyContent={{ md: "center" }}>
          <Grid xs={12} md={8}>
            <Stack
              spacing={3}
              sx={{
                textAlign: "center",
                mt: { xs: 5, md: 10 },
              }}
            >
              <Box
                flexWrap="wrap"
                display="flex"
                alignItems="center"
                justifyContent="center"
                sx={{ typography: "caption", color: "text.disabled" }}
              >
                <Typography variant="body2" sx={{ color: "text.disabled" }}>
                  {post?.duration}
                </Typography>

                <>
                  <Box
                    component="span"
                    sx={{
                      mx: 1,
                      width: 4,
                      height: 4,
                      borderRadius: "50%",
                      backgroundColor: "currentColor",
                    }}
                  />

                  <Typography variant="body2" sx={{ color: "text.disabled" }}>
                    {post?.category}
                  </Typography>
                </>
              </Box>

              <Typography variant="h2" component="h1">
                {post?.title}
              </Typography>

              <Typography variant="h5">{post?.description}</Typography>
            </Stack>

            {renderToolbar}

            <Box sx={{ textAlign: "justify" }}>
              <Markdown content={post?.content ?? ""} />
            </Box>

            {!!post.tags?.length && <PostTags tags={post.tags} />}

            <Divider sx={{ mt: 10 }} />

            <PostAuthors authors={post?.authors} />

            <Divider />

            {(prevPost || nextPost) && (
              <Box
                gap={5}
                display="grid"
                gridTemplateColumns={{ xs: "repeat(1, 1fr)", md: "repeat(2, 1fr)" }}
                sx={{ py: 10 }}
              >
                {prevPost ? (
                  <PrevNextButton
                    title={prevPost.title}
                    coverUrl={prevPost.coverUrl}
                    href={`${paths.post}/${encodeUrl(`${prevPost.title}-${prevPost.id}`)}`}
                  />
                ) : (
                  <Box />
                )}

                {nextPost && (
                  <PrevNextButton
                    isNext
                    title={nextPost.title}
                    coverUrl={nextPost.coverUrl}
                    href={`${paths.post}/${encodeUrl(`${nextPost.title}-${nextPost.id}`)}`}
                  />
                )}
              </Box>
            )}
          </Grid>
        </Grid>
      </Container>

      <Divider />

      {recentPosts?.length === 3 && <LatestPosts posts={recentPosts} />}

      <Newsletter />
    </>
  );
}
