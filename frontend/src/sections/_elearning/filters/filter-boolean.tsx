import { Stack, Switch, Typography } from "@mui/material";

// ----------------------------------------------------------------------

type Props = {
  value: boolean;
  leftLabel: string;
  rightLabel: string;
  onChange: (value: boolean) => void;
};

export default function FilterBoolean({ leftLabel, rightLabel, value, onChange }: Props) {
  return (
    <Stack direction="row" spacing={0} alignItems="center">
      <Typography variant="body2">{leftLabel}</Typography>
      <Switch checked={value} onChange={(event) => onChange(event.target.checked)} />
      <Typography variant="body2">{rightLabel}</Typography>
    </Stack>
  );
}
