"use client";

import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";

import { paths } from "src/routes/paths";

import { _coursePosts } from "src/_mock";

import { Posts } from "../posts/posts";
import Advertisement from "../advertisement";
import Newsletter from "../newsletter/newsletter";
import { PostSidebar } from "../posts/post-sidebar";
import { FeaturedPost } from "../posts/featured-post";
import { PostSearchMobile } from "../posts/post-search-mobile";

// ----------------------------------------------------------------------

const posts = _coursePosts.slice(0, 8);
const featuredPost = _coursePosts[3];
const recentPosts = _coursePosts.slice(-4);

export function PostsView() {
  return (
    <>
      <PostSearchMobile />

      <FeaturedPost post={featuredPost} />

      <Container sx={{ pt: 10 }}>
        <Grid disableEqualOverflow container spacing={{ md: 8 }}>
          <Grid xs={12} md={8}>
            <Posts posts={posts} />
          </Grid>

          <Grid xs={12} md={4}>
            <PostSidebar
              categories={[
                { label: "Marketing", path: "" },
                { label: "Community", path: "" },
                { label: "Tutorials", path: "" },
                { label: "Business", path: "" },
                { label: "Management", path: "" },
              ]}
              recentPosts={recentPosts}
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
