import Stack from "@mui/material/Stack";
import Pagination, { paginationClasses } from "@mui/material/Pagination";

import { ITeamMemberProps } from "src/types/team";

import TeacherItem from "./teacher-item";
import TeacherItemSkeleton from "./teacher-item-skeleton";

// ----------------------------------------------------------------------

type Props = {
  teachers: ITeamMemberProps[];
  loading?: boolean;
  pagesCount?: number;
  page: number;
  onPageChange: (selectedPage: number) => void;
};

export default function TeacherList({ teachers, loading, pagesCount, page, onPageChange }: Props) {
  return (
    <>
      <Stack spacing={4}>
        {(loading ? [...Array(9)] : teachers).map((teacher, index) =>
          teacher ? (
            <TeacherItem key={teacher.id} teacher={teacher} />
          ) : (
            <TeacherItemSkeleton key={index} />
          ),
        )}
      </Stack>

      {teachers?.length > 0 && (
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
      )}
    </>
  );
}
