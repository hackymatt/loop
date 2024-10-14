import { useLecturers } from "src/api/lecturers/lecturers";
import { usePostCategories } from "src/api/post-categories/post-categories";

import {
  RHFSwitch,
  RHFTextField,
  RHFImageUpload,
  RHFMarkdownField,
  RHFAutocompleteDnd,
} from "src/components/hook-form";

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
        getOptionLabel={(option) => (option as IPostCategoryProps).name}
        loading={isLoadingCategories}
        isOptionEqualToValue={(a, b) => a.name === b.name}
      />
    ),
    authors: (
      <RHFAutocompleteDnd
        key="authors"
        name="authors"
        label="Autorzy"
        multiple
        options={availableLecturers ?? []}
        getOptionLabel={(option) => (option as ITeamMemberProps).name}
        loading={isLoadingLecturers}
        isOptionEqualToValue={(a, b) => a.name === b.name}
      />
    ),
    image: <RHFImageUpload key="image" name="image" label="" />,
    active: <RHFSwitch name="active" label="Status" />,
  };
  return { fields };
};
