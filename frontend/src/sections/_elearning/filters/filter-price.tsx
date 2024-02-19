import { useState, useEffect } from "react";

import { InputAdornment } from "@mui/material";
import TextField from "@mui/material/TextField";
import Stack, { StackProps } from "@mui/material/Stack";

import { useDebounce } from "src/hooks/use-debounce";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

interface Props extends StackProps {
  valuePriceFrom: IQueryParamValue;
  valuePriceTo: IQueryParamValue;
  onChangeStartPrice: (priceFrom: IQueryParamValue) => void;
  onChangeEndPrice: (priceTo: IQueryParamValue) => void;
}

// ----------------------------------------------------------------------

export default function FilterPrice({
  valuePriceFrom,
  valuePriceTo,
  onChangeStartPrice,
  onChangeEndPrice,
  ...other
}: Props) {
  return (
    <Stack spacing={1} direction="row" alignItems="center" divider={<div> - </div>} {...other}>
      <PriceInput
        placeholder="od"
        price={valuePriceFrom === 0 ? "" : valuePriceFrom}
        onChange={(price) => onChangeStartPrice(price)}
      />
      <PriceInput
        placeholder="do"
        price={valuePriceTo === 0 ? "" : valuePriceTo}
        onChange={(price) => onChangeEndPrice(price)}
      />
    </Stack>
  );
}

interface PriceInputProps {
  placeholder: string;
  price: IQueryParamValue;
  onChange: (price: IQueryParamValue) => void;
}

function PriceInput({ placeholder, price, onChange }: PriceInputProps) {
  const [value, setValue] = useState<IQueryParamValue>(price);
  const debouncedValue = useDebounce<IQueryParamValue>(value);

  const handleChange = (event: { target: { value: string } }) => {
    setValue(event.target.value);
  };

  useEffect(() => {
    if (debouncedValue !== price) {
      onChange(debouncedValue);
    }
  }, [debouncedValue, onChange, price]);

  return (
    <TextField
      hiddenLabel
      size="small"
      placeholder={placeholder}
      type="number"
      value={value === 0 ? "" : value}
      onChange={(event) => handleChange(event)}
      InputProps={{
        inputProps: { min: 0, step: ".01" },
        endAdornment: <InputAdornment position="end">zł</InputAdornment>,
      }}
    />
  );
}
