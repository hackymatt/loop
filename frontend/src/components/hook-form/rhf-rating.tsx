import { Controller, useFormContext } from "react-hook-form";

import { Box, Rating, Typography, RatingProps, FormHelperText } from "@mui/material";

// ----------------------------------------------------------------------

type Props = RatingProps & {
  name: string;
  label: string;
};

export default function RHFRating({ name, label, ...other }: Props) {
  const { control } = useFormContext();

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <Box>
          <Typography variant="subtitle2" gutterBottom>
            {label}
          </Typography>
          <Rating
            {...field}
            value={Number(field.value)}
            onChange={(event, newValue) => {
              field.onChange(newValue as number);
            }}
            {...other}
          />
          {!!error && (
            <FormHelperText error={!!error}>{error ? error?.message : null}</FormHelperText>
          )}
        </Box>
      )}
    />
  );
}
