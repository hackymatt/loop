import TextField from "@mui/material/TextField";
import Stack, { StackProps } from "@mui/material/Stack";

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
      <TextField
        size="small"
        label="od"
        type="number"
        value={filterPriceFrom === 0 ? "" : filterPriceFrom}
        onChange={(event) => onChangeStartPrice(event.target.value)}
      />
      <TextField
        size="small"
        label="do"
        type="number"
        value={filterPriceTo === 0 ? "" : filterPriceTo}
        onChange={(event) => onChangeEndPrice(event.target.value)}
      />
    </Stack>
  );
}
