import {
  Stack,
  Avatar,
  TextField,
  Typography,
  Autocomplete,
  checkboxClasses,
  autocompleteClasses,
} from "@mui/material";

import { ICourseTeacherProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type IOption = {
  value: string;
  label: string;
};

type Props = {
  value: IQueryParamValue;
  options: ICourseTeacherProp[];
  onChange: (newValue: IQueryParamValue) => void;
};

export default function FilterTeacher({ value, options, onChange }: Props) {
  const modifiedOptions = options?.map((option: ICourseTeacherProp) => ({
    value: option.id,
    label: option.name,
    gender: option.gender,
    avatarUrl: option.avatarUrl,
  }));
  const currentValue = modifiedOptions.find((option: IOption) => option.value === value);
  return (
    <Autocomplete
      limitTags={2}
      fullWidth
      size="small"
      options={modifiedOptions}
      getOptionLabel={(option) => option.label}
      value={currentValue}
      noOptionsText="Brak opcji"
      onChange={(event, selectedValue) => onChange(selectedValue?.value)}
      slotProps={{
        paper: {
          sx: {
            [`& .${autocompleteClasses.listbox}`]: {
              [`& .${autocompleteClasses.option}`]: {
                [`& .${checkboxClasses.root}`]: {
                  p: 0,
                  mr: 1,
                },
              },
            },
          },
        },
      }}
      renderInput={(params) => (
        <TextField
          {...params}
          hiddenLabel
          placeholder="Wszyscy instruktorzy"
          InputProps={{
            ...params.InputProps,
            autoComplete: "search",
          }}
        />
      )}
      renderOption={(props, option, { selected }) => {
        const genderAvatarUrl =
          option.gender === "Kobieta"
            ? "/assets/images/avatar/avatar_female.jpg"
            : "/assets/images/avatar/avatar_male.jpg";

        const avatarUrl = option.avatarUrl || genderAvatarUrl;
        return (
          <li {...props} key={option.value}>
            <Stack direction="row" alignItems="center">
              <Avatar src={avatarUrl} />
              <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                {option.label}
              </Typography>
            </Stack>
          </li>
        );
      }}
    />
  );
}
