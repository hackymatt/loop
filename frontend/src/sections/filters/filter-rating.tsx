import Stack from "@mui/material/Stack";
import { Checkbox } from "@mui/material";
import Rating from "@mui/material/Rating";
import FormControlLabel from "@mui/material/FormControlLabel";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: IQueryParamValue[];
  onChangeRating: (rating: IQueryParamValue) => void;
};

export default function FilterRating({ value, options, onChangeRating }: Props) {
  return (
    <Stack spacing={2} alignItems="flex-start">
      {options.map((rating) => (
        <FormControlLabel
          key={rating}
          value={rating}
          control={
            <Checkbox
              checked={value === rating}
              onClick={() => (rating !== value ? onChangeRating(rating) : onChangeRating(null))}
              sx={{ display: "none" }}
            />
          }
          label={
            <Stack
              direction="row"
              alignItems="center"
              sx={{
                ...(value === rating && {
                  fontWeight: "fontWeightSemiBold",
                }),
              }}
            >
              <Rating
                size="small"
                value={Number(rating)}
                readOnly
                sx={{
                  mr: 1,
                  ...(value === rating && {
                    opacity: 1,
                  }),
                }}
              />
              i więcej
            </Stack>
          }
          sx={{
            m: 0,
            opacity: 0.48,
            "&:hover": { opacity: 1 },
            ...(value === rating && {
              opacity: 1,
              fontWeight: "fontWeightSemiBold",
            }),
          }}
        />
      ))}
    </Stack>
  );
}
