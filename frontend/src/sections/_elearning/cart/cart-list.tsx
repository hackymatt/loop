import Stack from "@mui/material/Stack";

import Scrollbar from "src/components/scrollbar";

import { ICartProp } from "src/types/cart";

import CartItem from "./cart-item";

// ----------------------------------------------------------------------

type Props = {
  cartItems: ICartProp[];
  wishlist?: boolean;
};

export default function CartList({ cartItems, wishlist = false }: Props) {
  return (
    <Scrollbar>
      <Stack
        direction="row"
        alignItems="center"
        sx={{
          py: 2,
          minWidth: 720,
          typography: "subtitle2",
          borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
        }}
      >
        <Stack flexGrow={1}>Lekcja</Stack>
        <Stack sx={{ width: 120 }}>Cena</Stack>
        <Stack sx={{ width: 36 }} />
        {wishlist && <Stack sx={{ width: 36 }} />}
      </Stack>

      {cartItems?.map((cartItem) => (
        <CartItem key={cartItem.id} cartItem={cartItem} wishlist={wishlist} />
      ))}
    </Scrollbar>
  );
}
