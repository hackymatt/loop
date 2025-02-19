import { Typography, InputAdornment } from "@mui/material";

import { GITHUB_REPO } from "src/config-global";
import { useTechnologies } from "src/api/technologies/technologies";

import { RHFSwitch, RHFTextField, RHFAutocompleteDnd } from "src/components/hook-form";

import { ITechnologyProps } from "src/types/technology";

export const useLessonFields = () => {
  const { data: availableTechnologies, isLoading: isLoadingTechnologies } = useTechnologies({
    sort_by: "name",
    page_size: -1,
  });

  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} />
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
      />
    ),
    github_url: (
      <RHFTextField
        key="github_url"
        name="github_url"
        label="Repozytorium"
        type="url"
        InputLabelProps={{ shrink: true }}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <Typography variant="body2">{GITHUB_REPO}</Typography>
            </InputAdornment>
          ),
        }}
      />
    ),
    technologies: (
      <RHFAutocompleteDnd
        key="technologies"
        name="technologies"
        label="Technologie"
        multiple
        options={availableTechnologies ?? []}
        getOptionLabel={(option) => (option as ITechnologyProps)?.name ?? ""}
        loading={isLoadingTechnologies}
        isOptionEqualToValue={(a, b) => a.name === b.name}
      />
    ),
    active: <RHFSwitch name="active" label="Status" labelPlacement="start" sx={{ pr: 3 }} />,
  };
  return { fields };
};
