import { Stack, Button, Typography } from "@mui/material";

import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

type Props = {
  githubUrl: string;
};

export default function Repository({ githubUrl }: Props) {
  return (
    <>
      <Typography variant="subtitle2" sx={{ mt: 0.5, mr: 1.5 }}>
        Materiały:
      </Typography>

      <Stack direction="row" alignItems="center" flexWrap="wrap">
        <Button
          size="small"
          variant="outlined"
          component="a"
          href={githubUrl}
          target="_blank"
          startIcon={<Iconify icon="carbon:logo-github" />}
        >
          GitHub
        </Button>
      </Stack>
    </>
  );
}
