import Box from "@mui/material/Box";
import Pagination, { paginationClasses } from "@mui/material/Pagination";

import { IReviewItemProp } from "src/types/review";

import ReviewItem from "./review-item";

// ----------------------------------------------------------------------

type Props = {
  reviews: IReviewItemProp[];
  pagesCount: number;
};

export default function Reviews({ reviews, pagesCount }: Props) {
  return (
    <>
      {reviews?.map((review) => {
        const {
          id,
          name,
          gender,
          rating,
          message,
          createdAt,
          avatarUrl,
          lessonTitle,
          teacherName,
        } = review;

        return (
          <Box key={id}>
            <ReviewItem
              name={name}
              gender={gender}
              avatarUrl={avatarUrl}
              createdAt={createdAt}
              message={message}
              rating={rating}
              lessonTitle={lessonTitle}
              teacherName={teacherName}
            />
          </Box>
        );
      })}

      {reviews?.length > 0 && (
        <Pagination
          count={pagesCount}
          color="primary"
          sx={{
            mt: 5,
            mb: 10,
            [`& .${paginationClasses.ul}`]: {
              justifyContent: "center",
            },
          }}
        />
      )}
    </>
  );
}
