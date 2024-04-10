import { useForm } from "react-hook-form";

import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useDeleteCourse } from "src/api/courses/course";

import FormProvider from "src/components/hook-form";

import { ICourseProps } from "src/types/course";

import { defaultValues } from "./course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  course: ICourseProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CourseDeleteForm({ course, onClose, ...other }: Props) {
  const { mutateAsync: deleteCourse } = useDeleteCourse();

  const methods = useForm({
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async () => {
    try {
      await deleteCourse({ id: course.id });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Usuń kurs</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Typography>{`Czy na pewno chcesz usunąć kurs ${course.slug}?`}</Typography>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="error" type="submit" variant="contained" loading={isSubmitting}>
            Usuń
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
