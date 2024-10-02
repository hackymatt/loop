import Box from "@mui/material/Box";
import Pagination, { paginationClasses } from "@mui/material/Pagination";

import { IReviewItemProp } from "src/types/review";

import ReviewItem from "./review-item";

// ----------------------------------------------------------------------

type Props = {
  reviews: IReviewItemProp[];
  showTeacher?: boolean;
  pagesCount?: number;
  page: number;
  onPageChange: (selectedPage: number) => void;
};

export default function ReviewList({
  reviews,
  showTeacher = true,
  pagesCount,
  page,
  onPageChange,
}: Props) {
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
              showTeacher={showTeacher}
            />
          </Box>
        );
      })}

      {reviews?.length > 0 && (
        <Pagination
          count={pagesCount ?? 0}
          page={page}
          sx={{
            mt: 5,
            mb: 10,
            [`& .${paginationClasses.ul}`]: {
              justifyContent: "center",
            },
          }}
          onChange={(event, selectedPage: number) => onPageChange(selectedPage)}
        />
      )}
    </>
  );
}
