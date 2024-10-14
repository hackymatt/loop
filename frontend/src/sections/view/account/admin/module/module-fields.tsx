import { useLessons } from "src/api/lessons/lessons";

import { RHFTextField, RHFAutocompleteDnd } from "src/components/hook-form";

import { ICourseLessonProp } from "src/types/course";

export const useModuleFields = () => {
  const { data: availableLessons, isLoading: isLoadingLessons } = useLessons({
    sort_by: "title",
    page_size: -1,
  });
  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    lessons: (
      <RHFAutocompleteDnd
        key="lessons"
        name="lessons"
        label="Lekcje"
        multiple
        options={availableLessons ?? []}
        getOptionLabel={(option) => (option as ICourseLessonProp)?.title ?? ""}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingLessons}
      />
    ),
  };
  return { fields };
};
