import { InputAdornment } from "@mui/material";

import { RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { PaymentStatus } from "src/types/payment";

export const usePaymentFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    amount: (
      <RHFTextField
        key="amount"
        name="amount"
        label="Kwota"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
      />
    ),
    status: (
      <RHFAutocomplete
        key="status"
        name="status"
        label="Status"
        options={Object.values(PaymentStatus)}
        isOptionEqualToValue={(option, value) => option === value}
      />
    ),
  };
  return { fields };
};
