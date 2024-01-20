import { useState, useEffect } from "react";

import TextField from "@mui/material/TextField";
import Stack, { StackProps } from "@mui/material/Stack";

import { useDebounce } from "src/hooks/use-debounce";

import { IQueryParamValue } from "src/types/queryParams";

// ----------------------------------------------------------------------

interface Props extends StackProps {
  filterPriceFrom: IQueryParamValue;
  filterPriceTo: IQueryParamValue;
  onChangeStartPrice: (priceFrom: IQueryParamValue) => void;
  onChangeEndPrice: (priceTo: IQueryParamValue) => void;
}

// ----------------------------------------------------------------------

export default function FilterPrice({
  filterPriceFrom,
  filterPriceTo,
  onChangeStartPrice,
  onChangeEndPrice,
  ...other
}: Props) {
  return (
    <Stack spacing={2} direction="row" alignItems="center" divider={<div> - </div>} {...other}>
      <PriceInput
        label="od"
        price={filterPriceFrom === 0 ? "" : filterPriceFrom}
        onChange={(price) => onChangeStartPrice(price)}
      />
      <PriceInput
        label="do"
        price={filterPriceTo === 0 ? "" : filterPriceTo}
        onChange={(price) => onChangeEndPrice(price)}
      />
    </Stack>
  );
}

interface PriceInputProps {
  label: string;
  price: IQueryParamValue;
  onChange: (price: IQueryParamValue) => void;
}

function PriceInput({ label, price, onChange }: PriceInputProps) {
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
      size="small"
      label={label}
      type="number"
      value={value === 0 ? "" : value}
      onChange={(event) => handleChange(event)}
    />
  );
}
