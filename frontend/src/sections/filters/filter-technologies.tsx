import Chip from "@mui/material/Chip";
import TextField from "@mui/material/TextField";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";
import Autocomplete, { autocompleteClasses } from "@mui/material/Autocomplete";

import Iconify, { isIconExists } from "src/components/iconify";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: IQueryParamValue[];
  onChangeTechnology: (newValue: IQueryParamValue) => void;
};

const autocompleteProps = {
  root: {
    limitTags: 2,
    multiple: true,
    disableCloseOnSelect: true,
  },
  chip: {
    size: "small",
    variant: "soft",
  },
  paper: {
    sx: {
      [`& .${autocompleteClasses.option}`]: {
        [`& .${checkboxClasses.root}`]: {
          p: 0,
          mr: 1,
        },
      },
    },
  },
} as const;

export default function FilterTechnologies({ value, options, onChangeTechnology }: Props) {
  const currentValue = value ? (value as string).split(",") : [];
  return (
    <Autocomplete
      multiple
      limitTags={2}
      size="small"
      disableCloseOnSelect
      options={options ?? []}
      getOptionLabel={(option) => option as string}
      value={currentValue}
      noOptionsText="Brak opcji"
      onChange={(event, selectedValue) => onChangeTechnology(selectedValue.join(","))}
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
      renderOption={(props, option, { selected }) => {
        const defaultIcon = `bxl:${(option as string)?.toLowerCase()}`;
        const icon = isIconExists(defaultIcon) ? defaultIcon : "carbon:code";
        return (
          <li {...props} key={option}>
            <Checkbox key={option} size="small" disableRipple checked={selected} />
            <Iconify icon={icon} sx={{ width: 16, height: 16, color: "primary.main", mr: 0.5 }} />
            {option}
          </li>
        );
      }}
      renderTags={(selected, getTagProps) =>
        selected.map((option, index) => (
          <Chip
            {...getTagProps({ index })}
            {...autocompleteProps.chip}
            key={option}
            label={option}
          />
        ))
      }
    />
  );
}
