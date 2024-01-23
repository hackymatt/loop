import { polishPlurals } from "polish-plurals";

import Paper from "@mui/material/Paper";
import Stack from "@mui/material/Stack";
import Rating from "@mui/material/Rating";
import Button from "@mui/material/Button";
import RadioGroup from "@mui/material/RadioGroup";
import Typography from "@mui/material/Typography";

import { fShortenNumber } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { IReviewStatistic } from "src/types/review";

import ReviewProgress from "../common/review-progress";

// ----------------------------------------------------------------------

const REVIEWS_RATINGS = ["5", "4.5", "4", "3.5", "3", "2.5", "2", "1.5", "1"] as const;

// ----------------------------------------------------------------------

type Props = {
  reviewNumber: number;
  ratingNumber: number;
  rating: string;
  reviewStatistics: IReviewStatistic[];
  onRatingChange: (value: string) => void;
  onOpenForm: VoidFunction;
};

export default function ReviewSummary({
  reviewNumber,
  ratingNumber,
  rating,
  reviewStatistics,
  onRatingChange,
  onOpenForm,
}: Props) {
  const reviewOptions = REVIEWS_RATINGS.map(
    (r: string) =>
      reviewStatistics?.find(
        (reviewStatistic: IReviewStatistic) => reviewStatistic.rating === r,
      ) ?? { rating: r, count: 0 },
  );

  return (
    <Paper variant="outlined" sx={{ p: 4, pr: 3, borderRadius: 2 }}>
      <Stack spacing={3}>
        <Stack spacing={3} direction="row" alignItems="center">
          <Typography variant="h1">
            {Number.isInteger(ratingNumber) ? `${ratingNumber}.0` : ratingNumber}
          </Typography>

          <Stack spacing={0.5}>
            <Rating value={ratingNumber} readOnly precision={0.1} />
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              {fShortenNumber(reviewNumber)}{" "}
              {polishPlurals("recenzja", "recenzje", "recenzji", reviewNumber)}
            </Typography>
          </Stack>
        </Stack>

        <RadioGroup>
          <ReviewProgress
            value={rating}
            options={reviewOptions}
            onChange={(value) => onRatingChange(value)}
          />
          {rating && (
            <Button
              variant="text"
              size="small"
              color="primary"
              onClick={() => onRatingChange("")}
              sx={{ p: 3, mt: 1 }}
            >
              Wyczyść
            </Button>
          )}
        </RadioGroup>

        <Button
          size="large"
          fullWidth
          startIcon={<Iconify icon="carbon:edit" width={24} />}
          onClick={onOpenForm}
          sx={{ textTransform: "none" }}
        >
          Napisz recenzje
        </Button>
      </Stack>
    </Paper>
  );
}
