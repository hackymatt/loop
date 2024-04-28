import { MenuItem, FormControl } from "@mui/material";
import Select, { SelectChangeEvent } from "@mui/material/Select";

// ----------------------------------------------------------------------

type IOption = {
  value: string;
  label: string;
};

type Props = {
  value: string;
  options: IOption[];
  onChange: (event: SelectChangeEvent) => void;
};

export default function Sorting({ value, options, onChange }: Props) {
  return (
    <FormControl size="small" hiddenLabel>
      <Select value={value} onChange={onChange}>
        {options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
}
