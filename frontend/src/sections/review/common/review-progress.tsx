import Stack from "@mui/material/Stack";
import RadioGroup from "@mui/material/RadioGroup";

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
    <RadioGroup onChange={(event) => onChange(event.target.value)}>
      <Stack spacing={2}>
        {options.map((option, index) => (
          <ReviewProgressItem
            key={option.rating}
            rating={option}
            index={index}
            totals={totals}
            selected={option.rating === value}
          />
        ))}
      </Stack>
    </RadioGroup>
  );
}
