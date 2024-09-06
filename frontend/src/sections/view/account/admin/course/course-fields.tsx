import { useSkills } from "src/api/skills/skills";
import { useTopics } from "src/api/topics/topics";
import { useModules } from "src/api/modules/modules";

import {
  RHFSwitch,
  RHFTextField,
  RHFImageUpload,
  RHFVideoUpload,
  RHFAutocomplete,
  RHFAutocompleteDnd,
} from "src/components/hook-form";

import { ICourseModuleProp, ICourseBySkillProps, ICourseByTopicProps } from "src/types/course";

// ----------------------------------------------------------------------

const LEVEL_OPTIONS = ["Podstawowy", "Średniozaawansowany", "Zaawansowany", "Ekspert"];

// ----------------------------------------------------------------------

export const useCourseFields = () => {
  const { data: availableModules, isLoading: isLoadingModules } = useModules({
    sort_by: "title",
    page_size: -1,
  });
  const { data: availableSkills, isLoading: isLoadingSkills } = useSkills({
    sort_by: "name",
    page_size: -1,
  });
  const { data: availableTopics, isLoading: isLoadingTopics } = useTopics({
    sort_by: "name",
    page_size: -1,
  });
  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} />
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
        options={availableModules}
        getOptionLabel={(option) => (option as ICourseModuleProp).title}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingModules}
      />
    ),
    skills: (
      <RHFAutocompleteDnd
        key="skills"
        name="skills"
        label="Umiejętności"
        multiple
        options={availableSkills}
        getOptionLabel={(option) => (option as ICourseBySkillProps).name}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingSkills}
      />
    ),
    topics: (
      <RHFAutocompleteDnd
        key="topics"
        name="topics"
        label="Tematy"
        multiple
        options={availableTopics}
        getOptionLabel={(option) => (option as ICourseByTopicProps).name}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingTopics}
      />
    ),
    active: <RHFSwitch name="active" label="Status" />,
  };
  return { fields };
};
