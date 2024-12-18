"use client";

import { useMemo, useCallback } from "react";

import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";

import { paths } from "src/routes/paths";

import { useResponsive } from "src/hooks/use-responsive";
import { useQueryParams } from "src/hooks/use-query-params";

import { useTags } from "src/api/tags/tags";
import { usePosts, usePostsPagesCount } from "src/api/posts/posts";
import { usePostCategories } from "src/api/post-categories/post-categories";

import { SplashScreen } from "src/components/loading-screen";

import { ITagProps } from "src/types/tags";
import { IPostProps } from "src/types/blog";
import { IQueryParamValue } from "src/types/query-params";

import { Posts } from "../posts/posts";
import Advertisement from "../advertisement";
import Newsletter from "../newsletter/newsletter";
import NotFoundView from "../error/not-found-view";
import { PostSidebar } from "../posts/post-sidebar";
import { FeaturedPost } from "../posts/featured-post";
import { PostSearchMobile } from "../posts/post-search-mobile";

// ----------------------------------------------------------------------

export function PostsView() {
  const mdUp = useResponsive("up", "md");

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();
  const query = useMemo(() => getQueryParams(), [getQueryParams]);

  const { data: pagesCount, isLoading: isLoadingPagesCount } = usePostsPagesCount({
    ...query,
    sort_by: "-publication_date",
  });
  const { data: recentPosts, isLoading: isLoadingFeaturedPost } = usePosts({
    ...query,
    sort_by: "-publication_date",
  });
  const { data: popularPosts } = usePosts({
    page_size: 4,
    sort_by: "-visits",
  });
  const { data: availableTags } = useTags({
    post_count_gt: 0,
    sort_by: "-post_count",
    page_size: -1,
  });
  const { data: availableCategories } = usePostCategories({
    page_size: -1,
    posts_count_from: 1,
    sort_by: "name",
  });

  const featuredPost = useMemo(() => recentPosts?.[0], [recentPosts]);
  const posts = useMemo(
    () => recentPosts?.filter((post: IPostProps) => post.id !== featuredPost?.id),
    [featuredPost?.id, recentPosts],
  );

  const isLoading = isLoadingPagesCount || isLoadingFeaturedPost;

  const handleChange = useCallback(
    (name: string, value: IQueryParamValue) => {
      if (value) {
        setQueryParam(name, value);
      } else {
        removeQueryParam(name);
      }
    },
    [removeQueryParam, setQueryParam],
  );

  if (isLoading) {
    return <SplashScreen />;
  }

  if (pagesCount === 0) {
    return <NotFoundView />;
  }

  return (
    <>
      {!mdUp && (
        <PostSearchMobile
          value={query?.search ?? ""}
          onChange={(value) => handleChange("search", value)}
        />
      )}

      {featuredPost && <FeaturedPost post={featuredPost} />}

      <Container sx={{ pt: 10 }}>
        <Grid disableEqualOverflow container spacing={{ md: 8 }}>
          <Grid xs={12} md={8}>
            <Posts
              posts={posts}
              pagesCount={pagesCount}
              page={parseInt(query.page ?? "1", 10) ?? 1}
              onPageChange={(selectedPage: number) => handleChange("page", selectedPage)}
            />
          </Grid>

          <Grid xs={12} md={4}>
            <PostSidebar
              category={query?.category ?? ""}
              onChangeCategory={(value) => handleChange("category", value)}
              categoryOptions={availableCategories ?? []}
              searchValue={query?.search ?? ""}
              onChangeSearch={(value) => handleChange("search", value)}
              tags={query?.tags_in ?? ""}
              onChangeTags={(value) => handleChange("tags_in", value)}
              tagsOptions={availableTags?.map((tag: ITagProps) => tag.name) ?? []}
              popularPosts={popularPosts}
              slots={{
                bottomNode: (
                  <Advertisement
                    advertisement={{
                      title: "Wejdź do IT",
                      description: "Sprawdź nasze kursy przygotowujące do pracy programisty",
                      imageUrl: "/assets/images/general/course-8.webp",
                      path: paths.courses,
                    }}
                  />
                ),
              }}
            />
          </Grid>
        </Grid>
      </Container>

      <Newsletter />
    </>
  );
}
