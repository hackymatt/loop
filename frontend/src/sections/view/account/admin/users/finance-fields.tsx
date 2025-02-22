import { InputAdornment } from "@mui/material";

import { RHFTextField } from "src/components/hook-form";

// ----------------------------------------------------------------------

export const useFinanceFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    commission: (
      <RHFTextField
        name="commission"
        label="Prowizja"
        type="number"
        InputProps={{
          inputProps: { min: 0, max: 100, step: "1" },
          endAdornment: <InputAdornment position="end">%</InputAdornment>,
        }}
      />
    ),

    rate: (
      <RHFTextField
        name="rate"
        label="Stawka godzinowa"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
      />
    ),

    account: <RHFTextField name="account" label="Nr konta" />,
  };

  return { fields };
};
