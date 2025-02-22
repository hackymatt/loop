import { Controller } from "react-hook-form";

import { DatePicker } from "@mui/x-date-pickers";

import { Gender } from "src/consts/gender";
import { countries } from "src/assets/data";
import { UserType } from "src/consts/user-type";

import {
  RHFSelect,
  RHFAvatar,
  RHFTextField,
  RHFAutocompleteCountry,
} from "src/components/hook-form";

import { IGender } from "src/types/user";

// ----------------------------------------------------------------------

export const useUserFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    image: <RHFAvatar name="image" sx={{ mr: 3 }} />,

    firstName: <RHFTextField name="firstName" label="Imię" />,

    lastName: <RHFTextField name="lastName" label="Nazwisko" />,

    email: <RHFTextField name="email" label="Adres e-mail" />,

    userType: (
      <RHFSelect
        name="userType"
        label="Typ"
        options={Object.values(UserType).map((userType: string) => ({
          label: userType,
          value: userType,
        }))}
        placeholder="Wybierz typ"
      />
    ),

    phoneNumber: <RHFTextField name="phoneNumber" label="Numer telefonu" />,

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
      <RHFSelect
        name="gender"
        label="Płeć"
        options={Object.values(Gender).map((gender: IGender) => ({ label: gender, value: gender }))}
        placeholder="Wybierz płeć"
      />
    ),

    streetAddress: <RHFTextField name="streetAddress" label="Ulica, numer budynku, numer lokalu" />,

    zipCode: <RHFTextField name="zipCode" label="Kod pocztowy" />,

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
