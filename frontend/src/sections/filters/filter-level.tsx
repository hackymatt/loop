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
  onChangeLevel: (levels: IQueryParamValue) => void;
};

export default function FilterLevel({ value, options, onChangeLevel }: Props) {
  const currentValue = value
    ? (value as string)
        .split(",")
        .map((level: string) => options.find((levelConfig) => levelConfig.value === level)?.label)
    : [];
  return (
    <FormControl fullWidth hiddenLabel>
      <Select
        multiple
        displayEmpty
        size="small"
        value={currentValue}
        onChange={(event) => {
          const levels = (event.target.value as string[])
            .map(
              (level: string) => options.find((levelConfig) => levelConfig.label === level)?.value,
            )
            .join(",");
          onChangeLevel(levels);
        }}
        renderValue={(selected) => {
          if (!selected.length) {
            return (
              <Typography variant="body2" sx={{ color: "text.disabled" }}>
                Wszystkie poziomy
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
        {options.map(({ value: levelValue, label }) => (
          <MenuItem key={levelValue} value={label}>
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
