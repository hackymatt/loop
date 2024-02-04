import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";
import Typography from "@mui/material/Typography";
import FormControl from "@mui/material/FormControl";
import Checkbox, { checkboxClasses } from "@mui/material/Checkbox";

import { IQueryParamValue } from "src/types/query-params";

// ----------------------------------------------------------------------

const LEVELS = [
  { value: "P", label: "Początkujący" },
  { value: "Ś", label: "Średniozaawansowany" },
  { value: "Z", label: "Zaawansowany" },
  { value: "E", label: "Ekspert" },
];

// ----------------------------------------------------------------------

type Props = {
  filterLevel: IQueryParamValue;
  onChangeLevel: (levels: IQueryParamValue) => void;
};

export default function FilterLevel({ filterLevel, onChangeLevel }: Props) {
  const currentValue = filterLevel
    ? (filterLevel as string)
        .split(",")
        .map((level: string) => LEVELS.find((levelConfig) => levelConfig.value === level)?.label)
    : [];
  return (
    <FormControl fullWidth hiddenLabel>
      <Select
        multiple
        displayEmpty
        value={currentValue}
        onChange={(event) => {
          const levels = (event.target.value as string[])
            .map(
              (level: string) => LEVELS.find((levelConfig) => levelConfig.label === level)?.value,
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
        {LEVELS.map(({ value, label }) => (
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
