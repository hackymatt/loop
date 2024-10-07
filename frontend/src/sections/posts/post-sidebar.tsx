import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import TextField from "@mui/material/TextField";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import InputAdornment from "@mui/material/InputAdornment";
import type { Theme, SxProps } from "@mui/material/styles";

import Iconify from "src/components/iconify";

import { IAuthorProps } from "src/types/author";
import { IPostProps, IPostCategoryProps } from "src/types/blog";

import { PostItemMobile } from "./post-item-mobile";

// ----------------------------------------------------------------------

type PostSidebarProps = BoxProps & {
  author?: IAuthorProps;
  recentPosts?: IPostProps[];
  categories?: IPostCategoryProps[];
  slots?: {
    topNode?: React.ReactNode;
    bottomNode?: React.ReactNode;
  };
  slotProps?: {
    tags?: SxProps<Theme>;
    author?: SxProps<Theme>;
    categories?: SxProps<Theme>;
    recentPosts?: SxProps<Theme>;
  };
};

export function PostSidebar({
  sx,
  slots,
  author,
  slotProps,
  categories,
  recentPosts,
  ...other
}: PostSidebarProps) {
  const renderAuthor = author && (
    <Box
      sx={{
        gap: 2,
        mb: { md: 5 },
        display: { xs: "none", md: "flex" },
        ...slotProps?.author,
      }}
    >
      <Avatar src={author.avatarUrl} sx={{ width: 64, height: 64 }} />
      <div>
        <Typography component="span" variant="h6">
          {author.name}
        </Typography>
        <Typography
          component="span"
          variant="body2"
          sx={{ mb: 1, mt: 0.5, display: "block", color: "text.secondary" }}
        >
          {author.title}
        </Typography>
      </div>
    </Box>
  );

  const renderCategories = !!categories?.length && (
    <Stack spacing={1} sx={slotProps?.categories}>
      <Typography variant="h5">Kategorie</Typography>

      {categories.map((category) => (
        <Box key={category.label} gap={2} display="flex" alignItems="center">
          <Box
            component="span"
            sx={{ width: 6, height: 6, borderRadius: "50%", bgcolor: "primary.main" }}
          />

          <Link variant="body2" href={category.path} color="inherit">
            {category.label}
          </Link>
        </Box>
      ))}
    </Stack>
  );

  const renderRecentPosts = !!recentPosts?.length && (
    <Stack spacing={2} sx={slotProps?.recentPosts}>
      <Typography variant="h5">Ostatnie wpisy</Typography>

      {recentPosts.map((post) => (
        <PostItemMobile key={post.id} post={post} onSiderbar />
      ))}
    </Stack>
  );

  return (
    <>
      {slots?.topNode}

      {renderAuthor}

      <TextField
        fullWidth
        hiddenLabel
        placeholder="Search..."
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Iconify width={24} icon="carbon:search" sx={{ color: "text.disabled" }} />
            </InputAdornment>
          ),
        }}
        sx={{ display: { xs: "none", md: "inline-flex" } }}
      />

      <Box
        gap={5}
        display="flex"
        flexDirection="column"
        sx={{
          pt: { md: 5 },
          pb: { xs: 10, md: 0 },
          ...sx,
        }}
        {...other}
      >
        {renderCategories}

        {renderRecentPosts}

        {slots?.bottomNode}
      </Box>
    </>
  );
}
