import { Control, useController } from "react-hook-form";

import { InputAdornment } from "@mui/material";

import { RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { PaymentMethod, PaymentStatus, PaymentCurrency } from "src/types/payment";

export const usePaymentFields = (control: Control<any>) => {
  const currencySymbol: { [key: string]: string } = { PLN: "zł", USD: "$", EUR: "€" } as const;

  const {
    field: { value: currency },
  } = useController({ name: "currency", control });

  const fields: { [key: string]: JSX.Element } = {
    amount: (
      <RHFTextField
        key="amount"
        name="amount"
        label="Kwota"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
          endAdornment: (
            <InputAdornment position="end">
              {currencySymbol[(currency as string) ?? "PLN"]}
            </InputAdornment>
          ),
        }}
      />
    ),
    currency: (
      <RHFAutocomplete
        key="currency"
        name="currency"
        label="Waluta"
        options={Object.values(PaymentCurrency)}
        isOptionEqualToValue={(option, value) => option === value}
      />
    ),
    method: (
      <RHFAutocomplete
        key="method"
        name="method"
        label="Metoda"
        options={Object.values(PaymentMethod)}
        isOptionEqualToValue={(option, value) => option === value}
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
    notes: <RHFTextField name="notes" multiline rows={3} label="Uwagi" />,
  };
  return { fields };
};
