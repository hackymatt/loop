import { useState, useEffect } from "react";

import { TextField, InputAdornment, TextFieldProps } from "@mui/material";

import { useDebounce } from "src/hooks/use-debounce";

import Iconify from "src/components/iconify";

import { IQueryParamValue } from "src/types/query-params";

type Props = TextFieldProps & {
  value: IQueryParamValue;
  onChangeSearch: (search: IQueryParamValue) => void;
  placeholder?: string;
};

export default function FilterSearch({
  value,
  onChangeSearch,
  placeholder,
  size = "small",
}: Props) {
  const [internalValue, setInternalValue] = useState<IQueryParamValue>(value);
  const debouncedValue = useDebounce<IQueryParamValue>(internalValue);

  const handleChange = (event: { target: { value: string } }) => {
    setInternalValue(event.target.value);
  };

  useEffect(() => {
    if (debouncedValue !== value) {
      onChangeSearch(debouncedValue);
    }
  }, [debouncedValue, value, onChangeSearch]);

  return (
    <TextField
      fullWidth
      hiddenLabel
      size={size}
      placeholder={placeholder ?? "Szukaj..."}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <Iconify icon="carbon:search" width={24} sx={{ color: "text.disabled" }} />
          </InputAdornment>
        ),
      }}
      value={internalValue}
      onChange={handleChange}
    />
  );
}
