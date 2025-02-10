import { Controller } from "react-hook-form";

import { InputAdornment } from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers";

import { countries } from "src/assets/data";

import {
  RHFSelect,
  RHFAvatar,
  RHFTextField,
  RHFAutocompleteCountry,
} from "src/components/hook-form";

import { UserType } from "src/types/user";

// ----------------------------------------------------------------------

const GENDER_OPTIONS = [
  { label: "Mężczyzna", value: "Mężczyzna" },
  { label: "Kobieta", value: "Kobieta" },
  { label: "Inne", value: "Inne" },
];

// ----------------------------------------------------------------------

export const useUserFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    image: <RHFAvatar name="image" sx={{ mr: 3 }} />,

    first_name: <RHFTextField name="first_name" label="Imię" />,

    last_name: <RHFTextField name="last_name" label="Nazwisko" />,

    email: <RHFTextField name="email" label="Adres e-mail" />,

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

    user_type: (
      <RHFSelect
        name="user_type"
        label="Typ"
        options={Object.values(UserType).map((userType: string) => ({
          label: userType,
          value: userType,
        }))}
        placeholder="Wybierz typ"
      />
    ),

    phone_number: <RHFTextField name="phone_number" label="Numer telefonu" />,

    dob: (
      <Controller
        name="dob"
        render={({ field, fieldState: { error } }) => (
          <DatePicker
            label="Data urodzenia"
            slotProps={{
              textField: {
                helperText: error?.message,
                error: !!error?.message,
              },
            }}
            {...field}
            value={field.value}
          />
        )}
      />
    ),

    gender: (
      <RHFSelect name="gender" label="Płeć" options={GENDER_OPTIONS} placeholder="Wybierz płeć" />
    ),

    street_address: (
      <RHFTextField name="street_address" label="Ulica, numer budynku, numer lokalu" />
    ),

    zip_code: <RHFTextField name="zip_code" label="Kod pocztowy" />,

    city: <RHFTextField name="city" label="Miasto" />,

    country: (
      <RHFAutocompleteCountry
        name="country"
        label="Państwo"
        placeholder="Wybierz państwo"
        fullWidth
        options={countries.map((option) => option.label)}
        getOptionLabel={(option) => option}
      />
    ),
  };
  return { fields };
};
