import * as Yup from "yup";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import { InputAdornment } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useEditLesson } from "src/api/lesson/lesson";
import { useTechnologies } from "src/api/technologies/technologies";

import FormProvider, { RHFSwitch, RHFTextField, RHFAutocomplete } from "src/components/hook-form";

import { ICourseLessonProp, ICourseByCategoryProps } from "src/types/course";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  lesson: ICourseLessonProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function LessonEditForm({ lesson, onClose, ...other }: Props) {
  const { data: availableTechnologies, isLoading: isLoadingTechnologies } = useTechnologies({
    sort_by: "name",
  });

  const { mutateAsync: editLesson } = useEditLesson(lesson.id);

  const defaultValues = {
    active: false,
    title: "",
    description: "",
    price: 0,
    duration: 15,
    github_url: "",
    technologies: [],
  };

  const NewLessonSchema = Yup.object().shape({
    active: Yup.boolean().required("Status jest wymagany"),
    title: Yup.string().required("Nazwa jest wymagana"),
    description: Yup.string().required("Opis jest wymagany"),
    price: Yup.number().required("Cena jest wymagana").min(0, "Cena musi być większa bądź równa 0"),
    duration: Yup.number()
      .required("Czas trwania jest wymagany")
      .min(15, "Czas trwania musi być większa bądź równa 15 minut")
      .test(
        "by15minutes",
        "Czas trwania musi być wielokrotnością 15 minut",
        (number) => number % 15 === 0,
      ),
    github_url: Yup.string().url().required("Link dla repozytorium jest wymagany"),
    technologies: Yup.array()
      .required("Technologie są wymagane")
      .min(1, "Wymagana przynajmniej jedna technologia"),
  });

  const methods = useForm({
    resolver: yupResolver(NewLessonSchema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (lesson && availableTechnologies) {
      reset({
        ...lesson,
        github_url: lesson.githubUrl,
        technologies: lesson.category.map((category: string) =>
          availableTechnologies.find(
            (technology: ICourseByCategoryProps) => technology.name === category,
          ),
        ),
      });
    }
  }, [availableTechnologies, lesson, reset]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editLesson(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>Dodaj nową lekcję</DialogTitle>
          <RHFSwitch name="active" label="Status" />
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            <RHFTextField name="title" label="Nazwa" />

            <RHFTextField name="description" label="Opis" multiline rows={5} />

            <RHFTextField
              name="price"
              label="Cena"
              type="number"
              InputProps={{
                inputProps: { min: 0, step: ".01" },
                endAdornment: <InputAdornment position="end">zł</InputAdornment>,
              }}
            />

            <RHFTextField
              name="duration"
              label="Czas trwania"
              type="number"
              InputProps={{
                inputProps: { min: 15 },
                endAdornment: <InputAdornment position="end">min</InputAdornment>,
              }}
            />

            <RHFTextField name="github_url" label="Repozytorium" type="url" />

            <RHFAutocomplete
              name="technologies"
              label="Technologie"
              multiple
              options={availableTechnologies}
              getOptionLabel={(option) => (option as ICourseByCategoryProps).name}
              loading={isLoadingTechnologies}
              isOptionEqualToValue={(a, b) => a.name === b.name}
            />
          </Stack>
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
