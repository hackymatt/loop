import Stack from "@mui/material/Stack";

import Scrollbar from "src/components/scrollbar";

import { ICartProp } from "src/types/cart";
import { IPurchaseError } from "src/types/purchase";

import CartItem from "./cart-item";

// ----------------------------------------------------------------------

type Props = {
  cartItems: ICartProp[];
  error?: Pick<IPurchaseError, "lessons">;
  wishlist?: boolean;
};

export default function CartList({ cartItems, error, wishlist = false }: Props) {
  return (
    <Scrollbar sx={{ maxHeight: { md: 600 } }}>
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
        <Stack sx={{ width: wishlist ? 200 : 175 }}>Cena</Stack>
        <Stack sx={{ width: 36 }} />
        {wishlist && <Stack sx={{ width: 36 }} />}
      </Stack>

      {cartItems?.map((cartItem, index) => (
        <CartItem
          key={cartItem.id}
          cartItem={cartItem}
          error={error?.lessons?.[index].lesson}
          wishlist={wishlist}
        />
      ))}
    </Scrollbar>
  );
}
