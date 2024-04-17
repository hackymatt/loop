import { Control, Controller, useController } from "react-hook-form";

import { DatePicker } from "@mui/x-date-pickers";
import { Stack, InputAdornment } from "@mui/material";

import { useUsers } from "src/api/users/users";

import { RHFSwitch, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { IUserDetailsProps } from "src/types/user";

// ----------------------------------------------------------------------

export const useCouponFields = (control: Control<any>) => {
  const { data: availableUsers, isLoading: isLoadingUsers } = useUsers({
    sort_by: "email",
    user_type: "S",
    page_size: -1,
  });

  const {
    field: { value: isPercentage },
  } = useController({ name: "is_percentage", control });

  const {
    field: { value: isAllUsers },
  } = useController({ name: "all_users", control });

  const {
    field: { value: isInfinite },
  } = useController({ name: "is_infinite", control });

  const fields: { [key: string]: JSX.Element } = {
    code: <RHFTextField key="code" name="code" label="Kod" />,
    discount_with_type: (
      <Stack spacing={1} direction="row" alignItems="center">
        <RHFTextField
          key="discount"
          name="discount"
          label="Zniżka"
          type="number"
          InputProps={{
            inputProps: { min: 0 },
            endAdornment: (
              <InputAdornment position="end">{isPercentage ? "%" : "zł"}</InputAdornment>
            ),
          }}
        />
        <RHFSwitch name="is_percentage" label="Procentowa" />
      </Stack>
    ),
    all_users: <RHFSwitch name="all_users" label="Wszyscy użytkownicy" />,
    users: (
      <RHFAutocomplete
        key="users"
        name="users"
        label="Wybrani użytkownicy"
        multiple
        options={availableUsers}
        getOptionLabel={(option) => (option as IUserDetailsProps).email}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        loading={isLoadingUsers}
        disabled={isAllUsers}
      />
    ),
    is_infinite: <RHFSwitch name="is_infinite" label="Nieograniczona ilość" />,
    max_uses: (
      <RHFTextField
        key="max_uses"
        name="max_uses"
        label="Maksymalna liczba wykorzystań"
        type="number"
        InputProps={{
          inputProps: { min: 0 },
        }}
        disabled={isInfinite}
      />
    ),
    uses_per_user: (
      <RHFTextField
        key="uses_per_user"
        name="uses_per_user"
        label="Maksymalna liczba wykorzystań przez użytkownika"
        type="number"
        InputProps={{
          inputProps: { min: 1 },
        }}
      />
    ),
    expiration_date: (
      <Controller
        name="expiration_date"
        render={({ field, fieldState: { error } }) => (
          <DatePicker
            label="Data ważności"
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
    min_total: (
      <RHFTextField
        key="min_total"
        name="min_total"
        label="Minimalna wartość"
        type="number"
        InputProps={{
          inputProps: { min: 1, step: "0.01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
      />
    ),
    active: <RHFSwitch name="active" label="Status" />,
  };
  return { fields };
};
