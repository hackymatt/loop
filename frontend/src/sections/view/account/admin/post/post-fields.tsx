import { Controller } from "react-hook-form";

import { DatePicker } from "@mui/x-date-pickers";

import { useTags } from "src/api/tags/tags";
import { useLecturers } from "src/api/lecturers/lecturers";
import { usePostCategories } from "src/api/post-categories/post-categories";

import {
  RHFSwitch,
  RHFTextField,
  RHFImageUpload,
  RHFMarkdownField,
  RHFAutocompleteDnd,
} from "src/components/hook-form";

import { ITagProps } from "src/types/tags";
import { ITeamMemberProps } from "src/types/team";
import { IPostCategoryProps } from "src/types/blog";

export const usePostFields = () => {
  const { data: availableCategories, isLoading: isLoadingCategories } = usePostCategories({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableLecturers, isLoading: isLoadingLecturers } = useLecturers({
    sort_by: "full_name",
    page_size: -1,
  });
  const { data: availableTags, isLoading: isLoadingTags } = useTags({
    sort_by: "name",
    page_size: -1,
  });

  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} />
    ),
    content: <RHFMarkdownField key="content" name="content" />,
    category: (
      <RHFAutocompleteDnd
        key="category"
        name="category"
        label="Kategoria"
        multiple
        options={availableCategories ?? []}
        getOptionLabel={(option) => (option as IPostCategoryProps)?.name ?? ""}
        loading={isLoadingCategories}
        isOptionEqualToValue={(a, b) => a.name === b.name}
      />
    ),
    tags: (
      <RHFAutocompleteDnd
        key="tags"
        name="tags"
        label="Tagi"
        multiple
        options={availableTags ?? []}
        getOptionLabel={(option) => (option as ITagProps)?.name ?? ""}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingTags}
      />
    ),
    authors: (
      <RHFAutocompleteDnd
        key="authors"
        name="authors"
        label="Autorzy"
        multiple
        options={availableLecturers ?? []}
        getOptionLabel={(option) => (option as ITeamMemberProps)?.name ?? ""}
        loading={isLoadingLecturers}
        isOptionEqualToValue={(a, b) => a.name === b.name}
      />
    ),
    publication_date: (
      <Controller
        name="publication_date"
        render={({ field, fieldState: { error } }) => (
          <DatePicker
            label="Data publikacji"
            slotProps={{
              textField: {
                helperText: error?.message,
                error: !!error?.message,
              },
              popper: {
                disablePortal: true,
              },
            }}
            {...field}
            value={field.value}
          />
        )}
      />
    ),
    image: <RHFImageUpload key="image" name="image" label="" />,
    active: <RHFSwitch name="active" label="Status" labelPlacement="start" sx={{ pr: 3 }} />,
  };
  return { fields };
};
