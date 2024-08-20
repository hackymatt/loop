import { useState } from "react";

import Box from "@mui/material/Box";
import { LoadingButton } from "@mui/lab";
import Divider from "@mui/material/Divider";
import { alpha } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import Stack, { StackProps } from "@mui/material/Stack";
import InputAdornment from "@mui/material/InputAdornment";
import { Link, Checkbox, FormHelperText, FormControlLabel } from "@mui/material";

import { paths } from "src/routes/paths";

import { useBoolean } from "src/hooks/use-boolean";

import { fCurrency } from "src/utils/format-number";

import { validateCoupon } from "src/api/coupons/coupon-validation";

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
  const acceptance = useBoolean(false);
  const acceptanceError = useBoolean(false);

  const [couponError, setCouponError] = useState<string>(error ?? "");
  const [coupon, setCoupon] = useState<string>();
  const [selectedCoupon, setSelectedCoupon] = useState<string>();

  const [discount, setDiscount] = useState<IDiscount>();
  const [discountedValue, setDiscountedValue] = useState<number>(total);

  const handleApplyCoupon = async () => {
    setCouponError("");
    if (coupon) {
      const validatedCoupon = await validateCoupon(coupon, total);
      const { status, data } = validatedCoupon;

      if (status !== 200) {
        setCouponError(data.code);
        return;
      }

      setSelectedCoupon(coupon);
      setCoupon("");
      setDiscount(data);
      setDiscountedValue(
        data.is_percentage ? total * (1 - data.discount / 100) : total - (data.discount ?? 0),
      );
    }
  };

  const handleDeleteCoupon = () => {
    setSelectedCoupon("");
    setDiscount({ discount: 0, is_percentage: false });
    setDiscountedValue(total);
  };

  const handleClick = () => {
    acceptanceError.onFalse();

    if (!acceptance.value) {
      acceptanceError.onTrue();
      return;
    }

    onPurchase(selectedCoupon ?? "");

    acceptanceError.onFalse();
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
        error={!!couponError}
        helperText={couponError}
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
        <LoadingButton
          size="small"
          color="primary"
          variant="text"
          onClick={handleDeleteCoupon}
          endIcon={<Iconify icon="carbon:trash-can" />}
        >
          {selectedCoupon}
        </LoadingButton>
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

      <Stack spacing={0.5}>
        <FormControlLabel
          control={<Checkbox checked={acceptance.value} onChange={acceptance.onToggle} />}
          label={
            <Typography variant="caption" align="left" sx={{ color: "text.secondary" }}>
              Akceptuję{" "}
              <Link
                target="_blank"
                rel="noopener"
                href={paths.termsAndConditions}
                color="text.primary"
                underline="always"
              >
                regulamin
              </Link>{" "}
              i{" "}
              <Link
                target="_blank"
                rel="noopener"
                href={paths.privacyPolicy}
                color="text.primary"
                underline="always"
              >
                politykę prywatności.
              </Link>
            </Typography>
          }
        />
        <FormHelperText error={!!acceptanceError.value}>
          {acceptanceError.value ? "To pole jest wymagane." : null}
        </FormHelperText>
      </Stack>

      <LoadingButton
        size="large"
        variant="contained"
        color="inherit"
        onClick={handleClick}
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
