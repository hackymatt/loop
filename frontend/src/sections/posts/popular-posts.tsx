import { Fragment } from "react";

import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { useResponsive } from "src/hooks/use-responsive";

import Iconify from "src/components/iconify";

import type { IPostProps } from "src/types/blog";

import { PostItem } from "./posts";
import { PostItemMobile } from "./post-item-mobile";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  posts: IPostProps[];
};

export function PopularPosts({ posts, sx, ...other }: Props) {
  const mdUp = useResponsive("up", "md");
  return (
    <Box
      component="section"
      sx={{
        py: { xs: 10, md: 15 },
        ...sx,
      }}
      {...other}
    >
      <Container>
        <Box display="flex" alignItems="center" sx={{ mb: { xs: 5, md: 10 } }}>
          <Typography component="h6" variant="h3" sx={{ flexGrow: 1 }}>
            Najczęściej czytane
          </Typography>

          <Button
            component={RouterLink}
            href={paths.posts}
            color="inherit"
            endIcon={<Iconify icon="solar:alt-arrow-right-outline" />}
          >
            Zobacz wszystkie
          </Button>
        </Box>

        <Box
          display="grid"
          gap={{ xs: 3, md: 4 }}
          gridTemplateColumns={{
            xs: "repeat(1, 1fr)",
            md: "repeat(3, 1fr)",
          }}
        >
          {posts.map((post) => (
            <Fragment key={post.id}>
              {mdUp && <PostItem post={post} sx={{ display: { xs: "none", md: "block" } }} />}
              {!mdUp && <PostItemMobile post={post} sx={{ display: { xs: "flex", md: "none" } }} />}
            </Fragment>
          ))}
        </Box>
      </Container>
    </Box>
  );
}
