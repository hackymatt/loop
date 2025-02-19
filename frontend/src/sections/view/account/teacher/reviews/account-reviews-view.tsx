"use client";

import { useMemo, useCallback } from "react";

import { Grid, Stack } from "@mui/material";

import { useQueryParams } from "src/hooks/use-query-params";

import { useUserDetails } from "src/api/auth/details";
import { useTeachings } from "src/api/teaching/teachings";
import { useLecturers } from "src/api/lecturers/lecturers";
import { useReviews, useReviewsPageCount } from "src/api/reviews/reviews";
import { useReviewsStatistics } from "src/api/reviews/reviews-statistics";

import ReviewList from "src/sections/review/review-list";
import ReviewSummary from "src/sections/review/review-summary";
import ReviewToolbar from "src/sections/review/review-toolbar";

import { ITeachingProp } from "src/types/teaching";
import { ICourseLessonProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

export default function AccountReviewsView() {
  const { data: userDetails } = useUserDetails();
  const { data: teachings } = useTeachings({ teaching: "True" });
  const { data: lecturerStats } = useLecturers(
    userDetails
      ? {
          uuid: userDetails.id,
        }
      : {},
  );

  const { setQueryParam, removeQueryParam, getQueryParams } = useQueryParams();

  const filters = useMemo(() => getQueryParams(), [getQueryParams]);

  const query = useMemo(
    () => ({ ...filters, lecturer_uuid: userDetails?.id }),
    [filters, userDetails?.id],
  );

  const { data: pagesCount } = useReviewsPageCount(query);
  const { data: reviews } = useReviews(query);
  const { data: reviewStatistics } = useReviewsStatistics(query);

  const handleChange = useCallback(
    (name: string, value: IQueryParamValue) => {
      if (value) {
        setQueryParam(name, value);
      } else {
        removeQueryParam(name);
      }
    },
    [removeQueryParam, setQueryParam],
  );

  return (
    <Stack direction="column" spacing={8}>
      <Grid xs={12} md={7} lg={8} sx={{ maxWidth: 750 }}>
        <ReviewToolbar
          lesson={filters?.lesson_id ?? ""}
          lessonOptions={(teachings ?? []).map(
            (teaching: ITeachingProp) =>
              ({
                id: teaching.id,
                title: teaching.title,
                duration: teaching.duration,
                price: teaching.price,
                githubUrl: teaching.githubUrl,
                active: teaching.active,
              }) as ICourseLessonProp,
          )}
          teacher={query.lecturer_uuid ?? ""}
          teacherOptions={[]}
          sort={filters.sort_by}
          onChangeLesson={(value) => handleChange("lesson_id", value)}
          onChangeTeacher={() => {}}
          onChangeSort={(event) => handleChange("sort_by", event.target.value)}
        />
      </Grid>
      <Grid container spacing={8} direction="row-reverse" sx={{ pl: 8 }}>
        <Grid xs={12} md={5} lg={4}>
          <ReviewSummary
            ratingNumber={lecturerStats?.[0]?.ratingNumber ?? 0}
            reviewNumber={lecturerStats?.[0]?.totalReviews ?? 0}
            rating={filters.rating ?? ""}
            reviewStatistics={reviewStatistics}
            onRatingChange={(value) => handleChange("rating", value)}
          />
        </Grid>

        <Grid xs={12} md={7} lg={8} sx={{ pr: 2 }}>
          <ReviewList
            reviews={reviews}
            showTeacher={false}
            pagesCount={pagesCount}
            page={parseInt(filters.page ?? "1", 10) ?? 1}
            onPageChange={(selectedPage: number) => handleChange("page", selectedPage)}
          />
        </Grid>
      </Grid>
    </Stack>
  );
}
