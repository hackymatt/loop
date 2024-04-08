import Stack from "@mui/material/Stack";

import Scrollbar from "src/components/scrollbar";

import { ICourseLessonProp } from "src/types/course";

import CartItem from "./cart-item";

// ----------------------------------------------------------------------

type Props = {
  lessons: ICourseLessonProp[];
  wishlist?: boolean;
};

export default function CartList({ lessons, wishlist = false }: Props) {
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
        <Stack sx={{ width: 120 }}>Ilość</Stack>
        <Stack sx={{ width: 120 }}>Cena</Stack>
        <Stack sx={{ width: 36 }} />
        {wishlist && <Stack sx={{ width: 36 }} />}
      </Stack>

      {lessons.map((lesson) => (
        <CartItem key={lesson.id} lesson={lesson} wishlist={wishlist} />
      ))}
    </Scrollbar>
  );
}
