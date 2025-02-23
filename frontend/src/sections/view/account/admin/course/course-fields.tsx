import { useTags } from "src/api/tags/tags";
import { useTopics } from "src/api/topics/topics";
import { useModules } from "src/api/modules/modules";
import { useCandidates } from "src/api/candidates/candidates";

import {
  RHFSwitch,
  RHFTextField,
  RHFImageUpload,
  RHFVideoUpload,
  RHFAutocomplete,
  RHFAutocompleteDnd,
} from "src/components/hook-form";

import { ITagProps } from "src/types/tags";
import { ITopicProps } from "src/types/topic";
import { IModuleProps } from "src/types/module";
import { ICandidateProps } from "src/types/candidate";

// ----------------------------------------------------------------------

const LEVEL_OPTIONS = ["Podstawowy", "Średniozaawansowany", "Zaawansowany", "Ekspert"];

// ----------------------------------------------------------------------

export const useCourseFields = () => {
  const { data: availableModules, isLoading: isLoadingModules } = useModules({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableTags, isLoading: isLoadingTags } = useTags({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableTopics, isLoading: isLoadingTopics } = useTopics({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableCandidates, isLoading: isLoadingCandidates } = useCandidates({
    sort_by: "name",
    page_size: -1,
  });
  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} />
    ),
    overview: (
      <RHFTextField key="overview" name="overview" label="Podsumowanie" multiline rows={10} />
    ),
    level: (
      <RHFAutocomplete
        key="level"
        name="level"
        label="Poziom"
        options={LEVEL_OPTIONS}
        isOptionEqualToValue={(option, value) => option === value}
      />
    ),
    image: <RHFImageUpload key="image" name="image" label="" />,
    video: <RHFVideoUpload key="video" name="video" label="" />,
    modules: (
      <RHFAutocompleteDnd
        key="modules"
        name="modules"
        label="Moduły"
        multiple
        options={availableModules ?? []}
        getOptionLabel={(option) => (option as IModuleProps)?.title ?? ""}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingModules}
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
    topics: (
      <RHFAutocompleteDnd
        key="topics"
        name="topics"
        label="Tematy"
        multiple
        options={availableTopics ?? []}
        getOptionLabel={(option) => (option as ITopicProps)?.name ?? ""}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingTopics}
      />
    ),
    candidates: (
      <RHFAutocompleteDnd
        key="candidates"
        name="candidates"
        label="Kandydaci"
        multiple
        options={availableCandidates ?? []}
        getOptionLabel={(option) => (option as ICandidateProps)?.name ?? ""}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingCandidates}
      />
    ),
    active: <RHFSwitch name="active" label="Status" labelPlacement="start" sx={{ pr: 3 }} />,
  };
  return { fields };
};
