import { InputAdornment } from "@mui/material";

import { useTechnologies } from "src/api/technologies/technologies";

import { RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { ICourseByTechnologyProps } from "src/types/course";

export const useTeachingFields = () => {
  const { data: availableTechnologies, isLoading: isLoadingTechnologies } = useTechnologies({
    sort_by: "name",
  });

  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" disabled />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} disabled />
    ),
    price: (
      <RHFTextField
        key="price"
        name="price"
        label="Cena"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
        disabled
      />
    ),
    duration: (
      <RHFTextField
        key="duration"
        name="duration"
        label="Czas trwania"
        type="number"
        InputProps={{
          inputProps: { min: 30 },
          endAdornment: <InputAdornment position="end">min</InputAdornment>,
        }}
        disabled
      />
    ),
    github_url: (
      <RHFTextField key="github_url" name="github_url" label="Repozytorium" type="url" disabled />
    ),
    technologies: (
      <RHFAutocomplete
        key="technologies"
        name="technologies"
        label="Technologie"
        multiple
        options={availableTechnologies ?? []}
        getOptionLabel={(option) => (option as ICourseByTechnologyProps)?.name ?? ""}
        loading={isLoadingTechnologies}
        isOptionEqualToValue={(a, b) => a.name === b.name}
        disabled
      />
    ),
  };
  return { fields };
};
