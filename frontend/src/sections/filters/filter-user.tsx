import {
  Stack,
  Avatar,
  TextField,
  Typography,
  Autocomplete,
  checkboxClasses,
  autocompleteClasses,
} from "@mui/material";

import { getGenderAvatar } from "src/utils/get-gender-avatar";

import { IUserDetailsProps } from "src/types/user";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type IOption = {
  value: string;
  label: string;
};

type Props = {
  value: IQueryParamValue;
  options: IUserDetailsProps[];
  onChange: (newValue: IQueryParamValue) => void;
};

export default function FilterUser({ value, options, onChange }: Props) {
  const modifiedOptions = options?.map((option: IUserDetailsProps) => ({
    value: option.id,
    label: option.email,
    gender: option.gender,
    avatarUrl: option.image,
  }));
  const currentValue = modifiedOptions.find((option: IOption) => option.value === value);
  return (
    <Autocomplete
      limitTags={2}
      fullWidth
      size="small"
      options={modifiedOptions}
      getOptionLabel={(option) => option?.label ?? ""}
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
          placeholder="Wszyscy użytkownicy"
          InputProps={{
            ...params.InputProps,
            autoComplete: "search",
          }}
        />
      )}
      renderOption={(props, option, { selected }) => {
        const genderAvatarUrl = getGenderAvatar(option.gender);

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
