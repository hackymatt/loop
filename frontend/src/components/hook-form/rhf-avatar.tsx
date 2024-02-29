import { Controller, useFormContext } from "react-hook-form";

import { Avatar, AvatarProps, FormHelperText } from "@mui/material";

// ----------------------------------------------------------------------

type Props = AvatarProps & {
  name: string;
};

export default function RHFAvatar({ name, ...other }: Props) {
  const { control } = useFormContext();

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <div>
          <Avatar {...field} src={field.value} {...other} />

          {!!error && (
            <FormHelperText error={!!error}>{error ? error?.message : null}</FormHelperText>
          )}
        </div>
      )}
    />
  );
}
