import { polishPlurals } from "polish-plurals";

import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";

import { fCurrency } from "src/utils/format-number";

import Iconify from "src/components/iconify";

import { ICourseLessonProp, ICourseTeacherProp } from "src/types/course";

// ----------------------------------------------------------------------

type Props = {
  lesson: ICourseLessonProp;
  wishlist: boolean;
};

export default function CartItem({ lesson, wishlist }: Props) {
  return (
    <Stack
      direction="row"
      alignItems="center"
      sx={{
        py: 1,
        minWidth: 720,
        borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
      }}
    >
      <Stack direction="row" alignItems="center" flexGrow={1}>
        <Stack spacing={0.5} sx={{ p: 2 }}>
          <Typography variant="subtitle2">{lesson.title}</Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Czas trwania: {lesson.duration}{" "}
            {polishPlurals("minuta", "minuty", "minut", lesson.duration)}
          </Typography>
          {lesson.category && lesson.category.length > 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              Technologie: {lesson.category.join(", ")}{" "}
            </Typography>
          )}
          {lesson.teachers && lesson.teachers.length > 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              Nauczyciele:{" "}
              {lesson.teachers?.map((teacher: ICourseTeacherProp) => teacher.name).join(", ")}{" "}
            </Typography>
          )}
        </Stack>
      </Stack>

      <Stack sx={{ width: 120 }}>
        <TextField
          select
          size="small"
          variant="outlined"
          SelectProps={{
            native: true,
          }}
          sx={{ width: 80 }}
        >
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </TextField>
      </Stack>

      <Stack sx={{ width: 120, typography: "subtitle2" }}> {fCurrency(lesson.price)} </Stack>

      <IconButton>
        <Iconify icon="carbon:trash-can" />
      </IconButton>

      {wishlist && (
        <IconButton>
          <Iconify icon="carbon:shopping-cart-plus" />
        </IconButton>
      )}
    </Stack>
  );
}
