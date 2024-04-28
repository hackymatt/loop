import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";
import FormControl from "@mui/material/FormControl";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

type Props = {
  value: IQueryParamValue;
  options: { value: string; label: string }[];
  onChangeDuration: (duration: IQueryParamValue) => void;
};

export default function FilterDuration({ value, options, onChangeDuration }: Props) {
  const currentValue = value
    ? (value as string)
        .split("|")
        .map(
          (level: string) =>
            options.find((durationConfig) => durationConfig.value === level)?.label,
        )
    : [];
  return (
    <FormControl fullWidth hiddenLabel>
      <Select
        multiple
        displayEmpty
        size="small"
        value={currentValue}
        onChange={(event) => {
          const durations = (event.target.value as string[])
            .map(
              (duration: string) =>
                options.find((durationConfig) => durationConfig.label === duration)?.value,
            )
            .join("|");
          onChangeDuration(durations);
        }}
        renderValue={(selected) => {
          if (!selected.length) {
            return (
              <Typography variant="body2" sx={{ color: "text.disabled" }}>
                Wszystkie czasy trwania
              </Typography>
            );
          }
          return (
            <Typography variant="subtitle2" component="span">
              {selected.join(", ")}
            </Typography>
          );
        }}
      >
        {options.map(({ value: durationValue, label }) => (
          <MenuItem key={durationValue} value={label}>
            <Checkbox
              size="small"
              checked={currentValue.includes(label)}
              sx={{
                [`&.${checkboxClasses.root}`]: {
                  p: 0,
                  mr: 1,
                },
              }}
            />
            {label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
