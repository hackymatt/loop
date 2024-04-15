import { useState } from "react";

import Box from "@mui/material/Box";
import { LoadingButton } from "@mui/lab";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Stack, { StackProps } from "@mui/material/Stack";
import InputAdornment from "@mui/material/InputAdornment";

import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

type Props = {
  total: number;
  onPurchase: (coupon: string) => void;
  isLoading?: boolean;
  error?: string;
};

type IDiscount = {
  discount: number;
  is_percentage: boolean;
};

export default function CartSummary({ total, onPurchase, isLoading, error }: Props) {
  const [coupon, setCoupon] = useState<string>();
  const [selectedCoupon, setSelectedCoupon] = useState<string>();

  const [discount, setDiscount] = useState<IDiscount>();
  const [discountedValue, setDiscountedValue] = useState<number>(total);

  const handleApplyCoupon = async () => {
    if (coupon) {
      setSelectedCoupon(coupon);
      setCoupon("");
      const discountReturn: IDiscount = { discount: 10, is_percentage: false };
      setDiscount(discountReturn);
      setDiscountedValue(
        discountReturn.is_percentage
          ? total * (1 - discountReturn.discount / 100)
          : total - (discountReturn.discount ?? 0),
      );
    }
  };

  const handleDeleteCoupon = () => {
    setSelectedCoupon("");
    setDiscount({ discount: 0, is_percentage: false });
    setDiscountedValue(total);
  };

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
        <Row label="Wartość koszyka" value={fCurrency(total)} />

        {discount?.discount !== 0 && (
          <Row
            label="Zniżka"
            value={
              discount?.is_percentage
                ? `-${discount?.discount}%`
                : `-${fCurrency(discount?.discount ?? 0)}`
            }
          />
        )}
      </Stack>

      <TextField
        value={coupon ?? ""}
        onChange={(event) => setCoupon(event.target.value)}
        hiddenLabel
        placeholder="Kod zniżkowy"
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <LoadingButton disabled={coupon === ""} onClick={handleApplyCoupon} loading={false}>
                Zastosuj
              </LoadingButton>
            </InputAdornment>
          ),
        }}
      />

      {selectedCoupon && (
        <>
          <LoadingButton
            size="small"
            color="primary"
            variant="text"
            onClick={handleDeleteCoupon}
            endIcon={<Iconify icon="carbon:trash-can" />}
          >
            {selectedCoupon}
          </LoadingButton>
          <Typography variant="body2" sx={{ color: "error.main" }}>
            {error}
          </Typography>
        </>
      )}

      <Divider sx={{ borderStyle: "dashed" }} />

      <Row
        label="Razem"
        value={fCurrency(discountedValue)}
        sx={{
          typography: "h6",
          "& span": { typography: "h6" },
        }}
      />

      <LoadingButton
        size="large"
        variant="contained"
        color="inherit"
        onClick={() => onPurchase(selectedCoupon ?? "")}
        loading={isLoading}
      >
        Przejdź do płatności
      </LoadingButton>
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
