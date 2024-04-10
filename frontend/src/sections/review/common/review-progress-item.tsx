import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import { Checkbox } from "@mui/material";
import { alpha } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import LinearProgress from "@mui/material/LinearProgress";
import FormControlLabel, { formControlLabelClasses } from "@mui/material/FormControlLabel";

import { fShortenNumber } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { IReviewStatistic } from "src/types/review";

// ----------------------------------------------------------------------

type Props = {
  rating: IReviewStatistic;
  totals: number;
  value: string;
  onChange: (rating: string) => void;
};

export default function ReviewProgressItem({ rating, totals, value, onChange }: Props) {
  return (
    <FormControlLabel
      value={rating.rating}
      control={
        <Checkbox
          checked={value === rating.rating}
          onClick={() => (rating.rating !== value ? onChange(rating.rating) : onChange(""))}
          sx={{ display: "none" }}
        />
      }
      label={
        <Stack alignItems="center" direction="row">
          <Stack direction="row" alignItems="center">
            <Box
              sx={{
                width: 12,
                typography: "subtitle1",
                textAlign: "center",
                mr: 2,
              }}
            >
              {rating.rating.length === 1 ? `${rating.rating}.0` : rating.rating}
            </Box>
            <Iconify width={16} icon="carbon:star" sx={{ mb: 0.5 }} />
          </Stack>

          <LinearProgress
            color="inherit"
            variant="determinate"
            value={totals !== 0 ? (rating.count / totals) * 100 : 0}
            sx={{
              mx: 2,
              width: 1,
              height: 6,
              "&:before": {
                opacity: 1,
                bgcolor: (theme) => alpha(theme.palette.grey[500], 0.12),
              },
              ...(value === rating.rating && {
                opacity: 0.48,
              }),
            }}
          />

          <Typography
            variant="body2"
            sx={{
              minWidth: 40,
              color: "text.disabled",
            }}
          >
            {rating.count === 0 ? 0 : fShortenNumber(rating.count)}
          </Typography>
        </Stack>
      }
      sx={{
        mx: 0,
        "&:hover": { opacity: 0.48 },
        [`& .${formControlLabelClasses.label}`]: {
          width: 1,
        },
      }}
    />
  );
}
