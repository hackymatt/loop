import Chip from "@mui/material/Chip";
import Stack, { StackProps } from "@mui/material/Stack";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

interface Props extends StackProps {
  value: IQueryParamValue;
  options: IQueryParamValue[];
  onChangeTag: (newValue: IQueryParamValue) => void;
}

export default function FilterTag({ options, value, onChangeTag, ...other }: Props) {
  const currentValue = value
    ? (value as string).split(",").map((filterTag: string) => options?.find((t) => t === filterTag))
    : [];
  return (
    <Stack direction="row" flexWrap="wrap" spacing={1} {...other}>
      {options.map((option) => {
        const selected = currentValue.includes(option as string);

        return (
          <Chip
            key={option}
            size="small"
            label={option}
            variant="outlined"
            onClick={() => {
              if (selected) {
                onChangeTag(currentValue.filter((t: IQueryParamValue) => t !== option).join(","));
              } else {
                onChangeTag([...currentValue, option].join(","));
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
    </Stack>
  );
}
