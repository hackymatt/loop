import Stack from "@mui/material/Stack";

import { IReviewStatistic } from "src/types/review";

import ReviewProgressItem from "./review-progress-item";

// ----------------------------------------------------------------------
type Props = {
  value: string;
  options: IReviewStatistic[];
  onChange: (rating: string) => void;
};

export default function ReviewProgress({ value, options, onChange }: Props) {
  const totals = options
    ?.map((option) => option.count)
    .reduce((accumulator: number, curr: number) => accumulator + curr);

  return (
    <Stack spacing={2}>
      {options.map((option, index) => (
        <ReviewProgressItem
          key={option.rating}
          rating={option}
          totals={totals}
          value={value}
          onChange={onChange}
        />
      ))}
    </Stack>
  );
}
