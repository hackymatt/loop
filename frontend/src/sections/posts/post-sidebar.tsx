import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Avatar from "@mui/material/Avatar";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import type { Theme, SxProps } from "@mui/material/styles";
import { Chip, Checkbox, FormControlLabel } from "@mui/material";

import { useResponsive } from "src/hooks/use-responsive";

import { IAuthorProps } from "src/types/author";
import { IQueryParamValue } from "src/types/query-params";
import { IPostProps, IPostCategoryProps } from "src/types/blog";

import { PostItemMobile } from "./post-item-mobile";
import FilterSearch from "../filters/filter-search";

// ----------------------------------------------------------------------

type PostSidebarProps = Omit<BoxProps, "onChange"> & {
  category: string;
  onChangeCategory: (category: IQueryParamValue) => void;
  categoryOptions?: IPostCategoryProps[];
  searchValue: string;
  onChangeSearch: (search: IQueryParamValue) => void;
  tags: string;
  onChangeTags: (tags: IQueryParamValue) => void;
  tagsOptions?: string[];
  author?: IAuthorProps;
  popularPosts?: IPostProps[];
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
  category,
  onChangeCategory,
  categoryOptions,
  searchValue,
  onChangeSearch,
  tags,
  onChangeTags,
  tagsOptions,
  sx,
  slots,
  author,
  slotProps,
  popularPosts,
  ...other
}: PostSidebarProps) {
  const mdUp = useResponsive("up", "md");

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

  const renderCategories = !!categoryOptions?.length && (
    <Stack spacing={1} sx={slotProps?.categories}>
      <Typography variant="h5">Kategorie</Typography>

      <Stack spacing={2} alignItems="flex-start">
        {categoryOptions.map((c) => (
          <FormControlLabel
            key={c.id}
            value={c.name}
            control={
              <Checkbox
                checked={category === c.name}
                onClick={() =>
                  c.name !== category ? onChangeCategory(c.name) : onChangeCategory(null)
                }
                sx={{ display: "none" }}
              />
            }
            label={
              <Box key={c.name} gap={2} display="flex" alignItems="center">
                <Box
                  component="span"
                  sx={{ width: 6, height: 6, borderRadius: "50%", bgcolor: "primary.main" }}
                />

                {c.name}
              </Box>
            }
            sx={{
              m: 0,
              fontWeight: "fontWeightSemiBold",
              "&:hover": { color: "primary.main" },
              ...(category === c.name && {
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

  const currentTags = tags
    ? (tags as string)
        .split(",")
        .map((filterTag: string) => tagsOptions?.find((t) => t === filterTag))
    : [];
  const renderTags = !!tagsOptions?.length && (
    <Stack spacing={2} sx={slotProps?.tags}>
      <Typography variant="h5">Tagi</Typography>

      <Box gap={1} display="flex" flexWrap="wrap">
        {tagsOptions.map((option) => {
          const selected = currentTags.includes(option as string);

          return (
            <Chip
              key={option}
              size="small"
              label={option}
              variant="outlined"
              onClick={() => {
                if (selected) {
                  onChangeTags(currentTags.filter((t: IQueryParamValue) => t !== option).join(","));
                } else {
                  onChangeTags([...currentTags, option].join(","));
                }
              }}
              sx={{
                ...(selected && {
                  bgcolor: "action.selected",
                  fontWeight: "fontWeightBold",
                }),
              }}
            />
          );
        })}
      </Box>
    </Stack>
  );

  return (
    <>
      {slots?.topNode}

      {renderAuthor}

      {mdUp && <FilterSearch value={searchValue} onChangeSearch={onChangeSearch} size="medium" />}

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

        {renderTags}

        {slots?.bottomNode}
      </Box>
    </>
  );
}
