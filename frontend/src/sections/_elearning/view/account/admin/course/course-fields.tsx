import { useSkills } from "src/api/skills/skills";
import { useTopics } from "src/api/topics/topics";
import { useLessons } from "src/api/lessons/lessons";

import {
  RHFSwitch,
  RHFTextField,
  RHFImageUpload,
  RHFVideoUpload,
  RHFAutocomplete,
  RHFAutocompleteDnd,
} from "src/components/hook-form";

import { ICourseLessonProp, ICourseBySkillProps, ICourseByTopicProps } from "src/types/course";

// ----------------------------------------------------------------------

const LEVEL_OPTIONS = ["Podstawowy", "Średniozaawansowany", "Zaawansowany", "Ekspert"];

// ----------------------------------------------------------------------

export const useCourseFields = () => {
  const { data: availableLessons, isLoading: isLoadingLessons } = useLessons({
    sort_by: "title",
  });
  const { data: availableSkills, isLoading: isLoadingSkills } = useSkills({
    sort_by: "name",
  });
  const { data: availableTopics, isLoading: isLoadingTopics } = useTopics({
    sort_by: "name",
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
    lessons: (
      <RHFAutocompleteDnd
        key="lessons"
        name="lessons"
        label="Lekcje"
        multiple
        options={availableLessons}
        getOptionLabel={(option) => (option as ICourseLessonProp).title}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingLessons}
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
