import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Stack, { StackProps } from "@mui/material/Stack";
import InputAdornment from "@mui/material/InputAdornment";

import { paths } from "src/routes/paths";
import { RouterLink } from "src/routes/components";

import { fCurrency } from "src/utils/format-number";

// ----------------------------------------------------------------------

type Props = {
  total: number;
  subtotal: number;
  discount: number;
};

export default function CartSummary({ total, subtotal, discount }: Props) {
  return (
    <Stack
      spacing={3}
      sx={{
        p: 5,
        borderRadius: 2,
        border: (theme) => `solid 1px ${alpha(theme.palette.grey[500], 0.24)}`,
      }}
    >
      <Typography variant="h6">Podsumowanie</Typography>

      <Stack spacing={2}>
        <Row label="Wartość koszyka" value={fCurrency(subtotal)} />

        {discount !== 0 && <Row label="Zniżka" value={`-${fCurrency(discount)}`} />}
      </Stack>

      <TextField
        hiddenLabel
        placeholder="Kod zniżkowy"
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Button>Zastosuj</Button>
            </InputAdornment>
          ),
        }}
      />

      <Divider sx={{ borderStyle: "dashed" }} />

      <Row
        label="Razem"
        value={fCurrency(total)}
        sx={{
          typography: "h6",
          "& span": { typography: "h6" },
        }}
      />

      <Button
        component={RouterLink}
        href={paths.eCommerce.checkout}
        size="large"
        variant="contained"
        color="inherit"
      >
        Przejdź do kasy
      </Button>
    </Stack>
  );
}

// ----------------------------------------------------------------------

type RowProps = StackProps & {
  label: string;
  value: string;
};

function Row({ label, value, sx, ...other }: RowProps) {
  return (
    <Stack
      direction="row"
      alignItems="center"
      justifyContent="space-between"
      sx={{ typography: "subtitle2", ...sx }}
      {...other}
    >
      <Box component="span" sx={{ typography: "body2" }}>
        {label}
      </Box>
      {value}
    </Stack>
  );
}
