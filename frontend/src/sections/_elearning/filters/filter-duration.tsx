import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";
import FormControl from "@mui/material/FormControl";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";

import { IQueryParamValue } from "src/types/queryParams";

// ----------------------------------------------------------------------

const DURATIONS = [
  { value: "(duration_to=60)", label: "0 - 1 godzin" },
  { value: "(duration_from=60)&(duration_to=180)", label: "1 - 3 godzin" },
  { value: "(duration_from=180)&(duration_to=360)", label: "3 - 6 godzin" },
  { value: "(duration_from=360)&(duration_to=1080)", label: "6 - 18 godzin" },
  { value: "(duration_from=1080)", label: "18+ godzin" },
];

// ----------------------------------------------------------------------

type Props = {
  filterDuration: IQueryParamValue;
  onChangeDuration: (duration: IQueryParamValue) => void;
};

export default function FilterDuration({ filterDuration, onChangeDuration }: Props) {
  const currentValue = filterDuration
    ? (filterDuration as string)
        .split("|")
        .map(
          (level: string) =>
            DURATIONS.find((durationConfig) => durationConfig.value === level)?.label,
        )
    : [];
  return (
    <FormControl fullWidth hiddenLabel>
      <Select
        multiple
        displayEmpty
        value={currentValue}
        onChange={(event) => {
          const durations = (event.target.value as string[])
            .map(
              (duration: string) =>
                DURATIONS.find((durationConfig) => durationConfig.label === duration)?.value,
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
        {DURATIONS.map(({ value, label }) => (
          <MenuItem key={value} value={label}>
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
