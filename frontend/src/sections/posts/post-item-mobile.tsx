import { useMemo } from "react";

import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import type { BoxProps } from "@mui/material/Box";

import { paths } from "src/routes/paths";

import { fDate } from "src/utils/format-time";
import { encodeUrl } from "src/utils/url-utils";

import Image from "src/components/image";
import TextMaxLine from "src/components/text-max-line";

import type { IPostProps } from "src/types/blog";

import { PostTime } from "./post-time";

// ----------------------------------------------------------------------

type Props = BoxProps & {
  post: IPostProps;
  onSiderbar?: boolean;
};

export function PostItemMobile({ post, onSiderbar, sx, ...other }: Props) {
  const path = useMemo(() => `${post.title.toLowerCase()}-${post.id}`, [post.id, post.title]);
  return (
    <Link href={`${paths.post}/${encodeUrl(path)}`} color="inherit" underline="none">
      <Box
        gap={2}
        display="flex"
        alignItems={{ xs: "flex-start", md: "unset" }}
        sx={{ width: 1, ...sx }}
        {...other}
      >
        <Image
          alt={post.title}
          src={post.coverUrl}
          sx={{ width: 64, height: 64, flexShrink: 0, borderRadius: 1.5 }}
        />

        <Stack spacing={onSiderbar ? 0.5 : 1}>
          <TextMaxLine variant={onSiderbar ? "subtitle2" : "subtitle1"} line={2}>
            {post.title}
          </TextMaxLine>

          <PostTime
            createdAt={fDate(post.createdAt, "d MMMM yyyy")}
            duration={post.duration}
            category={post.category}
          />
        </Stack>
      </Box>
    </Link>
  );
}
