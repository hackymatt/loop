import { TextField, Autocomplete } from "@mui/material";

import Label, { LabelColor } from "src/components/label";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: { value: string; label: string; color: string }[];
  onChange: (value: IQueryParamValue) => void;
};

export default function FilterStatus({ value, options, onChange }: Props) {
  const currentValue = options.find((o) => o.value === value);
  return (
    <Autocomplete
      sx={{ width: 1 }}
      options={options}
      getOptionLabel={(option) => option?.label ?? ""}
      value={currentValue}
      noOptionsText="Brak opcji"
      size="small"
      onChange={(event, selectedValue) => onChange(selectedValue?.value)}
      renderInput={(params) => (
        <TextField
          {...params}
          hiddenLabel
          placeholder="Wszystkie statusy"
          InputProps={{
            ...params.InputProps,
            autoComplete: "search",
            sx: { pb: 1 },
          }}
        />
      )}
      renderOption={(props, option) => (
        <li {...props} key={option.value}>
          <Label color={option.color as LabelColor}>{option.label}</Label>
        </li>
      )}
    />
  );
}
