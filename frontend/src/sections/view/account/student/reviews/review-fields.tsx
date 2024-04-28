import { RHFRating, RHFTextField } from "src/components/hook-form";

export const useReviewFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    rating: <RHFRating key="rating" name="rating" label="Twoja ocena:" precision={0.5} />,
    review: <RHFTextField multiline rows={3} name="review" label="Recenzja (opcjonalnie)" />,
  };
  return { fields };
};
