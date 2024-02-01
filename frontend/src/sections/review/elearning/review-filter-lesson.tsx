import { TextField, Autocomplete, checkboxClasses, autocompleteClasses } from "@mui/material";

import { ICourseLessonProp } from "src/types/course";
import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type IOption = {
  value: string;
  label: string;
};

type Props = {
  value: IQueryParamValue;
  options: ICourseLessonProp[];
  onChange: (newValue: IQueryParamValue) => void;
};

export default function FilterLesson({ value, options, onChange }: Props) {
  const modifiedOptions = options?.map((option: ICourseLessonProp) => ({
    value: option.id,
    label: option.title,
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
          placeholder="Wszystkie lekcje"
          InputProps={{
            ...params.InputProps,
            autoComplete: "search",
          }}
        />
      )}
    />
  );
}
