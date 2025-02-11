import { InputAdornment } from "@mui/material";

import { RHFSwitch, RHFTextField } from "src/components/hook-form";

export const useServiceFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    title: <RHFTextField key="title" name="title" label="Nazwa" />,
    description: (
      <RHFTextField key="description" name="description" label="Opis" multiline rows={5} />
    ),
    price: (
      <RHFTextField
        key="price"
        name="price"
        label="Cena"
        type="number"
        InputProps={{
          inputProps: { min: 0, step: ".01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
      />
    ),
    active: <RHFSwitch name="active" label="Status" labelPlacement="start" sx={{ pr: 3 }} />,
  };
  return { fields };
};
