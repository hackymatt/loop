import Stack from "@mui/material/Stack";
import Radio from "@mui/material/Radio";
import Rating from "@mui/material/Rating";
import RadioGroup from "@mui/material/RadioGroup";
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
    <RadioGroup value={value} onChange={(event) => onChangeRating(event.target.value)}>
      <Stack spacing={2} alignItems="flex-start">
        {options.map((rating) => (
          <FormControlLabel
            key={rating}
            value={rating}
            control={<Radio sx={{ display: "none" }} />}
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
                      opacity: 0.48,
                    }),
                  }}
                />
                i więcej
              </Stack>
            }
            sx={{
              m: 0,
              "&:hover": { opacity: 0.48 },
            }}
          />
        ))}
      </Stack>
    </RadioGroup>
  );
}
