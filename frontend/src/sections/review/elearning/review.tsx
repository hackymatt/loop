import { useState, useCallback } from "react";

import Container from "@mui/material/Container";
import Grid from "@mui/material/Unstable_Grid2";

import { useBoolean } from "src/hooks/use-boolean";

import { useReviews, useReviewsPageCount } from "src/api/reviews/reviews";
import { useReviewsStatistics } from "src/api/reviews/reviews-statistics";

import { SplashScreen } from "src/components/loading-screen";

import { IQueryParamValue } from "src/types/query-params";
import { ICourseLessonProp, ICourseTeacherProp } from "src/types/course";

import ReviewList from "./review-list";
import ReviewSummary from "./review-summary";
import ReviewToolbar from "./review-toolbar";
import ReviewNewForm from "../common/review-new-form";

// ----------------------------------------------------------------------

type Props = {
  courseId: string;
  ratingNumber: number;
  reviewNumber: number;
  lessons: ICourseLessonProp[];
  teachers: ICourseTeacherProp[];
};

export default function Review({ courseId, ratingNumber, reviewNumber, lessons, teachers }: Props) {
  const [query, setQuery] = useState({
    course_id: courseId,
    lesson_id: "",
    lecturer_id: "",
    rating: "",
    sort_by: "-created_at",
  });

  const { data: pagesCount, isLoading: isLoadingReviewsPageCount } = useReviewsPageCount(query);
  const { data: reviews, isLoading: isLoadingReviews } = useReviews(query);
  const { data: reviewStatistics, isLoading: isLoadingReviewsStatistics } =
    useReviewsStatistics(query);

  const isLoading = isLoadingReviewsPageCount || isLoadingReviews || isLoadingReviewsStatistics;

  const formOpen = useBoolean();

  const handleChange = useCallback((name: string, value: IQueryParamValue) => {
    setQuery((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  }, []);

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <>
      {reviewNumber > 0 && (
        <Container sx={{ overflow: "hidden", pt: 10, pb: 10 }}>
          <Grid xs={12} md={7} lg={8} sx={{ maxWidth: 750 }}>
            <ReviewToolbar
              lesson={query.lesson_id ?? ""}
              lessonOptions={lessons}
              teacher={query.lecturer_id ?? ""}
              teacherOptions={teachers}
              sort={query.sort_by}
              onChangeLesson={(value) => handleChange("lesson_id", value)}
              onChangeTeacher={(value) => handleChange("lecturer_id", value)}
              onChangeSort={(event) => handleChange("sort_by", event.target.value)}
            />
          </Grid>

          <Grid container spacing={8} direction="row-reverse">
            <Grid xs={12} md={5} lg={4}>
              <ReviewSummary
                ratingNumber={ratingNumber}
                reviewNumber={reviewNumber}
                rating={query.rating ?? ""}
                reviewStatistics={reviewStatistics}
                onRatingChange={(value) => handleChange("rating", value)}
                onOpenForm={formOpen.onTrue}
              />
            </Grid>

            <Grid xs={12} md={7} lg={8}>
              <ReviewList reviews={reviews} pagesCount={pagesCount} />
            </Grid>
          </Grid>
        </Container>
      )}

      <ReviewNewForm open={formOpen.value} onClose={formOpen.onFalse} />
    </>
  );
}
