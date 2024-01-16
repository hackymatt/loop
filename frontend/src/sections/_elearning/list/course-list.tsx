import Stack from "@mui/material/Stack";
import Pagination, { paginationClasses } from "@mui/material/Pagination";

import { ICourseProps } from "src/types/course";

import CourseItem from "./course-item";
import CourseItemSkeleton from "./course-item-skeleton";

// ----------------------------------------------------------------------

type Props = {
  courses: ICourseProps[];
  loading?: boolean;
  pagesCount?: number;
  page: number;
  onPageChange: (selectedPage: number) => void;
};

export default function CourseList({ courses, loading, pagesCount, page, onPageChange }: Props) {
  console.log(page);
  return (
    <>
      <Stack spacing={4}>
        {(loading ? [...Array(9)] : courses).map((course, index) =>
          course ? (
            <CourseItem key={course.id} course={course} />
          ) : (
            <CourseItemSkeleton key={index} />
          ),
        )}
      </Stack>

      <Pagination
        count={pagesCount ?? 0}
        page={page}
        color="primary"
        sx={{
          my: 10,
          [`& .${paginationClasses.ul}`]: {
            justifyContent: "center",
          },
        }}
        onChange={(event, selectedPage: number) => onPageChange(selectedPage)}
      />
    </>
  );
}
