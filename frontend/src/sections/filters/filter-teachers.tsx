import {
  Chip,
  Stack,
  Avatar,
  TextField,
  Typography,
  Autocomplete,
  checkboxClasses,
  autocompleteClasses,
} from "@mui/material";

import { ITeamMemberProps } from "src/types/team";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: ITeamMemberProps[];
  onChangeTeacher: (newValue: IQueryParamValue) => void;
};

export default function FilterTeachers({ value, options, onChangeTeacher }: Props) {
  const currentValue = value
    ? (value as string)
        .split(",")
        .map((filterTeacher: string) => options?.find((t) => t.id.toString() === filterTeacher))
    : [];
  return (
    <Autocomplete
      multiple
      limitTags={2}
      disableCloseOnSelect
      size="small"
      options={options ?? []}
      getOptionLabel={(option: ITeamMemberProps) => option.name}
      value={currentValue as ITeamMemberProps[]}
      noOptionsText="Brak opcji"
      onChange={(event, selectedValue) => {
        const selectedTeachers = selectedValue
          .map((teacher: ITeamMemberProps) => teacher.id)
          .join(",");
        onChangeTeacher(selectedTeachers);
      }}
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
          hiddenLabel={!currentValue.length}
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
          <li {...props} key={option.id}>
            <Stack direction="row" alignItems="center">
              <Avatar src={avatarUrl} />
              <Typography variant="body2" sx={{ ml: 1, mr: 0.5 }}>
                {option.name}
              </Typography>
            </Stack>
          </li>
        );
      }}
      renderTags={(selected, getTagProps) =>
        selected.map((option, index) => (
          <Chip
            {...getTagProps({ index })}
            key={index}
            label={option?.name}
            size="small"
            color="primary"
            variant="filled"
          />
        ))
      }
    />
  );
}
