import Box from "@mui/material/Box";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import type { BoxProps } from "@mui/material/Box";

import { fDate } from "src/utils/format-time";

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
  return (
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
        <Link color="inherit">
          <TextMaxLine variant={onSiderbar ? "subtitle2" : "subtitle1"} line={2}>
            {post.title}
          </TextMaxLine>
        </Link>

        <PostTime
          createdAt={fDate(post.createdAt, "d MMMM yyyy")}
          duration={post.duration}
          category={post.category}
        />
      </Stack>
    </Box>
  );
}
