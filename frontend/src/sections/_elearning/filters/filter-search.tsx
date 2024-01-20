import { useState } from "react";
import { debounce } from "lodash-es";

import { TextField, InputAdornment } from "@mui/material";

import Iconify from "src/components/iconify";

import { IQueryParamValue } from "src/types/queryParams";

type Props = {
  filterSearch: IQueryParamValue;
  onChangeSearch: (search: IQueryParamValue) => void;
};

export default function FilterSearch({ filterSearch, onChangeSearch }: Props) {
  const [value, setValue] = useState(filterSearch ?? "");

  const handleDebounceFn = (inputValue: string) => {
    onChangeSearch(inputValue);
  };

  const debounceFn = debounce(handleDebounceFn, 10000);

  const handleChange = (event: { target: { value: string } }) => {
    setValue(event.target.value);
    debounceFn(event.target.value);
  };

  return (
    <TextField
      fullWidth
      hiddenLabel
      placeholder="Szukaj..."
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <Iconify icon="carbon:search" width={24} sx={{ color: "text.disabled" }} />
          </InputAdornment>
        ),
      }}
      value={value}
      onChange={handleChange}
    />
  );
}
