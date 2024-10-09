import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { usePostCategory, useEditPostCategory } from "src/api/post-categories/post-category";

import FormProvider from "src/components/hook-form";

import { IPostCategoryProps } from "src/types/blog";

import { schema, defaultValues } from "./category";
import { useCategoryFields } from "./category-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  category: IPostCategoryProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function CategoryEditForm({ category, onClose, ...other }: Props) {
  const { data: categoryData } = usePostCategory(category.id);
  const { mutateAsync: editCategory } = useEditPostCategory(category.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (categoryData) {
      reset(categoryData);
    }
  }, [reset, categoryData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editCategory(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useCategoryFields();

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj kategorię</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>{fields.name}</Stack>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="inherit" type="submit" variant="contained" loading={isSubmitting}>
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
