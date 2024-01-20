import { useState, useEffect } from "react";

import { TextField, InputAdornment } from "@mui/material";

import { useDebounce } from "src/hooks/use-debounce";

import Iconify from "src/components/iconify";

import { IQueryParamValue } from "src/types/queryParams";

type Props = {
  filterSearch: IQueryParamValue;
  onChangeSearch: (search: IQueryParamValue) => void;
};

export default function FilterSearch({ filterSearch, onChangeSearch }: Props) {
  const [value, setValue] = useState<IQueryParamValue>(filterSearch);
  const debouncedValue = useDebounce<IQueryParamValue>(value);

  const handleChange = (event: { target: { value: string } }) => {
    setValue(event.target.value);
  };

  useEffect(() => {
    onChangeSearch(debouncedValue);
  }, [debouncedValue, onChangeSearch]);

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
