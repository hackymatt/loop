import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import type { Theme, SxProps } from "@mui/material/styles";
import { Checkbox, FormControlLabel } from "@mui/material";

import { IAuthorProps } from "src/types/author";
import { IQueryParamValue } from "src/types/query-params";
import { IPostProps, IPostCategoryProps } from "src/types/blog";

import { PostItemMobile } from "./post-item-mobile";
import FilterSearch from "../filters/filter-search";

// ----------------------------------------------------------------------

type PostSidebarProps = Omit<BoxProps, "onChange"> & {
  value: string;
  onChange: (category: IQueryParamValue) => void;
  searchValue: string;
  onChangeSearch: (search: IQueryParamValue) => void;
  author?: IAuthorProps;
  popularPosts?: IPostProps[];
  categories?: IPostCategoryProps[];
  slots?: {
    topNode?: React.ReactNode;
    bottomNode?: React.ReactNode;
  };
  slotProps?: {
    tags?: SxProps<Theme>;
    author?: SxProps<Theme>;
    categories?: SxProps<Theme>;
    popularPosts?: SxProps<Theme>;
  };
};

export function PostSidebar({
  value,
  onChange,
  searchValue,
  onChangeSearch,
  sx,
  slots,
  author,
  slotProps,
  categories,
  popularPosts,
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
          {author.role}
        </Typography>
      </div>
    </Box>
  );

  const renderCategories = !!categories?.length && (
    <Stack spacing={1} sx={slotProps?.categories}>
      <Typography variant="h5">Kategorie</Typography>

      <Stack spacing={2} alignItems="flex-start">
        {categories.map((category) => (
          <FormControlLabel
            key={category.label}
            value={category.label}
            control={
              <Checkbox
                checked={value === category.label}
                onClick={() =>
                  category.label !== value ? onChange(category.label) : onChange(null)
                }
                sx={{ display: "none" }}
              />
            }
            label={
              <Box key={category.label} gap={2} display="flex" alignItems="center">
                <Box
                  component="span"
                  sx={{ width: 6, height: 6, borderRadius: "50%", bgcolor: "primary.main" }}
                />

                {category.label}
              </Box>
            }
            sx={{
              m: 0,
              fontWeight: "fontWeightSemiBold",
              "&:hover": { color: "primary.main" },
              ...(value === category.label && {
                color: "primary.main",
              }),
            }}
          />
        ))}
      </Stack>
    </Stack>
  );

  const renderRecentPosts = !!popularPosts?.length && (
    <Stack spacing={2} sx={slotProps?.popularPosts}>
      <Typography variant="h5">Najczęściej czytane</Typography>

      {popularPosts.map((post: IPostProps) => (
        <PostItemMobile key={post.id} post={post} onSiderbar />
      ))}
    </Stack>
  );

  return (
    <>
      {slots?.topNode}

      {renderAuthor}

      <FilterSearch value={searchValue} onChangeSearch={onChangeSearch} size="medium" />

      <Box
        gap={5}
        display="flex"
        flexDirection="column"
        sx={{
          pt: { md: 5 },
          pb: { xs: 10, md: 0 },
          py: { md: 5 },
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
