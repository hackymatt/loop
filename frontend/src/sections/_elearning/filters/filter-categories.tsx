import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";
import Autocomplete, { autocompleteClasses } from "@mui/material/Autocomplete";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: IQueryParamValue[];
  onChangeCategory: (newValue: IQueryParamValue) => void;
};

export default function FilterCategories({ value, options, onChangeCategory }: Props) {
  const currentValue = value ? (value as string).split(",") : [];
  return (
    <Autocomplete
      multiple
      limitTags={2}
      disableCloseOnSelect
      options={options ?? []}
      getOptionLabel={(option) => option as string}
      value={currentValue}
      noOptionsText="Brak opcji"
      onChange={(event, selectedValue) => onChangeCategory(selectedValue.join(","))}
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
          placeholder="Wszystkie technologie"
          InputProps={{
            ...params.InputProps,
            autoComplete: "search",
          }}
        />
      )}
      renderOption={(props, option, { selected }) => (
        <li {...props} key={option}>
          <Checkbox key={option} size="small" disableRipple checked={selected} />
          {option}
        </li>
      )}
      renderTags={(selected, getTagProps) =>
        selected.map((option, index) => (
          <Chip
            {...getTagProps({ index })}
            key={option}
            label={option}
            size="small"
            color="primary"
            variant="filled"
          />
        ))
      }
    />
  );
}
