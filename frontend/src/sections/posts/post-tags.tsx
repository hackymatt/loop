import Box from "@mui/material/Box";
import { Link } from "@mui/material";
import Chip from "@mui/material/Chip";
import type { BoxProps } from "@mui/material/Box";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

// ----------------------------------------------------------------------

type PostTagsProps = BoxProps & {
  tags: string[];
};

export function PostTags({ tags, sx, ...other }: PostTagsProps) {
  return (
    <Box display="flex" alignItems="center" flexWrap="wrap" sx={{ mt: 5, ...sx }} {...other}>
      <Typography variant="subtitle2" sx={{ mr: 1 }}>
        Tagi:
      </Typography>

      <Box gap={1} display="flex" flexWrap="wrap">
        {tags.map((tag) => (
          <Link component={RouterLink} key={tag} href={`${paths.posts}?tags_in=${tag}`}>
            <Chip key={tag} size="small" variant="soft" label={tag} />
          </Link>
        ))}
      </Box>
    </Box>
  );
}
