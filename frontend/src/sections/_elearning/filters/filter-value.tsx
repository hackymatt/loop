import { useState, useEffect } from "react";

import TextField from "@mui/material/TextField";
import Stack, { StackProps } from "@mui/material/Stack";

import { useDebounce } from "src/hooks/use-debounce";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

interface Props extends StackProps {
  valueFrom: IQueryParamValue;
  valueTo: IQueryParamValue;
  onChangeStart: (from: IQueryParamValue) => void;
  onChangeEnd: (to: IQueryParamValue) => void;
}

// ----------------------------------------------------------------------

export default function FilterValue({
  valueFrom,
  valueTo,
  onChangeStart,
  onChangeEnd,
  ...other
}: Props) {
  return (
    <Stack spacing={1} direction="row" alignItems="center" divider={<div> - </div>} {...other}>
      <PriceInput
        placeholder="od"
        inputValue={valueFrom === 0 ? "" : valueFrom}
        onChange={(value) => onChangeStart(value)}
      />
      <PriceInput
        placeholder="do"
        inputValue={valueTo === 0 ? "" : valueTo}
        onChange={(value) => onChangeEnd(value)}
      />
    </Stack>
  );
}

interface InputProps {
  placeholder: string;
  inputValue: IQueryParamValue;
  onChange: (value: IQueryParamValue) => void;
}

function PriceInput({ placeholder, inputValue, onChange }: InputProps) {
  const [value, setValue] = useState<IQueryParamValue>(inputValue);
  const debouncedValue = useDebounce<IQueryParamValue>(value);

  const handleChange = (event: { target: { value: string } }) => {
    setValue(event.target.value);
  };

  useEffect(() => {
    if (debouncedValue !== inputValue) {
      onChange(debouncedValue);
    }
  }, [debouncedValue, onChange, inputValue]);

  return (
    <TextField
      hiddenLabel
      size="small"
      placeholder={placeholder}
      type="number"
      value={value === 0 ? "" : value}
      onChange={(event) => handleChange(event)}
    />
  );
}
