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

import { useTopic, useEditTopic } from "src/api/topics/topic";

import FormProvider from "src/components/hook-form";

import { ICourseByTopicProps } from "src/types/course";

import { schema, defaultValues } from "./topic";
import { useTopicFields } from "./topic-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  topic: ICourseByTopicProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TopicEditForm({ topic, onClose, ...other }: Props) {
  const { data: topicData } = useTopic(topic.id);
  const { mutateAsync: editTopic } = useEditTopic(topic.id);

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
    if (topicData) {
      reset(topicData);
    }
  }, [reset, topicData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    try {
      await editTopic(data);
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useTopicFields();

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onClose}
      {...other}
      sx={{
        zIndex: (theme) => theme.zIndex.modal + 1,
        display: "flex",
        flexDirection: "column",
      }}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj temat</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>{fields.name}</Stack>
        </DialogContent>

        <DialogActions
          sx={{
            position: "fixed",
            bottom: 0,
            left: 0,
            right: 0,
            zIndex: (theme) => theme.zIndex.modal + 2,
            bgcolor: "background.paper",
            boxShadow: (theme) => theme.shadows[4],
            p: 2,
          }}
        >
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
