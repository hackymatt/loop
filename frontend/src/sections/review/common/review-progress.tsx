import Stack from "@mui/material/Stack";
import RadioGroup from "@mui/material/RadioGroup";

import ReviewProgressItem from "./review-progress-item";

// ----------------------------------------------------------------------

const RATINGS = [
  { value: "5", number: 5212 },
  { value: "4", number: 2442 },
  { value: "3", number: 523 },
  { value: "2", number: 423 },
  { value: "1", number: 80 },
];

// ----------------------------------------------------------------------
type Props = {
  value: string;
  onChange: (rating: string) => void;
};

export default function ReviewProgress({ value, onChange }: Props) {
  const totals = RATINGS.map((rating) => rating.number).reduce(
    (accumulator: number, curr: number) => accumulator + curr,
  );

  return (
    <RadioGroup onChange={(event) => onChange(event.target.value)}>
      <Stack spacing={2}>
        {RATINGS.map((rating, index) => (
          <ReviewProgressItem
            key={rating.value}
            rating={rating}
            index={index}
            totals={totals}
            selected={rating.value === value}
          />
        ))}
      </Stack>
    </RadioGroup>
  );
}
