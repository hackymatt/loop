import Box from "@mui/material/Box";
import type { Theme, SxProps } from "@mui/material/styles";

import { IQueryParamValue } from "src/types/query-params";

import FilterSearch from "../filters/filter-search";

// ----------------------------------------------------------------------

type PostSearchMobileProps = {
  sx?: SxProps<Theme>;
  value: string;
  onChange: (search: IQueryParamValue) => void;
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
      <FilterSearch value={value} onChangeSearch={onChange} size="medium" />
    </Box>
  );
}
