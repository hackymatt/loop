import { EventClickArg } from "@fullcalendar/core";
import React, { useMemo, useCallback } from "react";

import { LoadingButton } from "@mui/lab";
import Button from "@mui/material/Button";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import {
  List,
  Stack,
  Avatar,
  ListItem,
  Typography,
  DialogTitle,
  ListItemText,
  ListItemAvatar,
} from "@mui/material";

import { useBoolean } from "src/hooks/use-boolean";

import Iconify from "src/components/iconify";

import { IScheduleStudentProp } from "src/types/course";

import LessonCancelForm from "./lesson-cancel-form";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  eventDetails: EventClickArg;
  isLoading: boolean;
  onConfirm: (eventInfo: EventClickArg) => void;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function DetailsForm({
  eventDetails,
  isLoading,
  onConfirm,
  onClose,
  ...other
}: Props) {
  const confirmCancellationFormOpen = useBoolean();

  const handleLessonCancel = useCallback(async () => {
    confirmCancellationFormOpen.onFalse();
    onConfirm(eventDetails);
  }, [confirmCancellationFormOpen, eventDetails, onConfirm]);

  const isReady = useMemo(
    () => eventDetails.event.extendedProps.ready,
    [eventDetails.event.extendedProps.ready],
  );

  const students = useMemo(
    () => eventDetails.event.extendedProps.students,
    [eventDetails.event.extendedProps.students],
  );

  return (
    <>
      <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <DialogTitle sx={{ typography: "h3", pb: 3 }}>{eventDetails.event.title}</DialogTitle>
          <Button
            size="medium"
            variant="outlined"
            component="a"
            href={eventDetails.event.url}
            target="_blank"
            startIcon={<Iconify icon="logos:google-meet" />}
            sx={{ mr: 3 }}
            disabled={!isReady}
          >
            Dołącz
          </Button>
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack direction="row" spacing={1}>
            <Typography>Minimalna ilość zapisów:</Typography>
            <Typography color={isReady ? "success" : "error"}>
              {isReady ? "osiągnięta" : "nieosiągnięta"}
            </Typography>
          </Stack>

          <Stack direction="row" spacing={1}>
            <Typography>Aktualna liczba studentów:</Typography>
            <Typography color={isReady ? "success" : "error"}>{students?.length ?? 0}</Typography>
          </Stack>

          <List sx={{ width: "100%" }}>
            {students?.map((student: IScheduleStudentProp) => {
              const genderImageUrl =
                student.gender === "Kobieta"
                  ? "/assets/images/avatar/avatar_female.jpg"
                  : "/assets/images/avatar/avatar_male.jpg";
              return (
                <ListItem key={student.id} alignItems="center">
                  <ListItemAvatar>
                    <Avatar src={student.image || genderImageUrl} />
                  </ListItemAvatar>
                  <ListItemText primary={student.name} />
                </ListItem>
              );
            })}
          </List>
        </DialogContent>

        <DialogActions>
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton
            color="error"
            type="submit"
            variant="contained"
            onClick={confirmCancellationFormOpen.onToggle}
          >
            Odwołaj
          </LoadingButton>
        </DialogActions>
      </Dialog>

      <LessonCancelForm
        loading={isLoading}
        open={confirmCancellationFormOpen.value}
        onConfirm={handleLessonCancel}
        onClose={confirmCancellationFormOpen.onFalse}
      />
    </>
  );
}
