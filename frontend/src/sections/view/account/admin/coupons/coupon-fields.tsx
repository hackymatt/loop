import { Control, Controller, useController } from "react-hook-form";

import { DateTimePicker } from "@mui/x-date-pickers";
import { Stack, Button, InputAdornment } from "@mui/material";

import { generateCode } from "src/utils/generateCode";

import { useUsers } from "src/api/users/users";

import { RHFSwitch, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { UserType, IUserDetailsProps } from "src/types/user";

// ----------------------------------------------------------------------

export const useCouponFields = (control: Control<any>) => {
  const { data: availableUsers, isLoading: isLoadingUsers } = useUsers({
    sort_by: "email",
    user_type: UserType.Student[0],
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

  const {
    field: { onChange: setCode },
  } = useController({ name: "code", control });

  const handleGenerateCode = () => {
    const code = generateCode(16);
    setCode(code);
  };

  const fields: { [key: string]: JSX.Element } = {
    code: (
      <RHFTextField
        key="code"
        name="code"
        label="Kod"
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Button onClick={handleGenerateCode}>Wygeneruj</Button>
            </InputAdornment>
          ),
        }}
      />
    ),
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
        options={availableUsers ?? []}
        getOptionLabel={(option) => (option as IUserDetailsProps).email}
        isOptionEqualToValue={(a, b) => a.email === b.email}
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
          <DateTimePicker
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
          inputProps: { min: 0, step: "0.01" },
          endAdornment: <InputAdornment position="end">zł</InputAdornment>,
        }}
      />
    ),
    active: <RHFSwitch name="active" label="Status" />,
  };
  return { fields };
};
