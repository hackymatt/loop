import { Controller } from "react-hook-form";

import { DatePicker } from "@mui/x-date-pickers";

import { countries } from "src/assets/data";

import { RHFSelect, RHFAvatar, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

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
    image: <RHFAvatar name="image" />,

    first_name: <RHFTextField name="first_name" label="Imię" disabled />,

    last_name: <RHFTextField name="last_name" label="Nazwisko" disabled />,

    email: <RHFTextField name="email" label="Adres e-mail" disabled />,

    user_title: <RHFTextField name="user_title" label="Tytuł zawodowy" disabled />,

    user_type: (
      <RHFSelect
        name="user_type"
        label="Typ"
        options={Object.keys(UserType).map((userType: string) => ({
          label: userType,
          value: userType,
        }))}
        placeholder="Wybierz typ"
      />
    ),

    phone_number: <RHFTextField name="phone_number" label="Numer telefonu" disabled />,

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
            disabled
          />
        )}
      />
    ),

    gender: (
      <RHFSelect
        name="gender"
        label="Płeć"
        options={GENDER_OPTIONS}
        placeholder="Wybierz płeć"
        disabled
      />
    ),

    street_address: (
      <RHFTextField name="street_address" label="Ulica, numer budynku, numer lokalu" disabled />
    ),

    zip_code: <RHFTextField name="zip_code" label="Kod pocztowy" disabled />,

    city: <RHFTextField name="city" label="Miasto" disabled />,

    country: (
      <RHFAutocomplete
        name="country"
        type="country"
        label="Państwo"
        placeholder="Wybierz państwo"
        fullWidth
        options={countries.map((option) => option.label)}
        getOptionLabel={(option) => option}
        disabled
      />
    ),
  };
  return { fields };
};
