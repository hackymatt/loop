import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import type { Theme, SxProps } from "@mui/material/styles";

import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

type PostSearchMobileProps = {
  sx?: SxProps<Theme>;
  value?: string;
  onChange?: (newValue: string) => void;
};

export function PostSearchMobile({ sx, value, onChange }: PostSearchMobileProps) {
  return (
    <Box
      sx={{
        px: 2,
        pb: 3,
        display: { md: "none" },
        ...sx,
      }}
    >
      <TextField
        fullWidth
        hiddenLabel
        placeholder="Szukaj..."
        value={value}
        onChange={(event) => onChange?.(event.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Iconify width={24} icon="carbon:search" sx={{ color: "text.disabled" }} />
            </InputAdornment>
          ),
        }}
      />
    </Box>
  );
}
