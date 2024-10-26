import { EventClickArg } from "@fullcalendar/core";
import React, { useMemo, useState, useCallback } from "react";

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
  IconButton,
  DialogTitle,
  ListItemText,
  ListItemAvatar,
} from "@mui/material";

import { useBoolean } from "src/hooks/use-boolean";

import { getGenderAvatar } from "src/utils/get-gender-avatar";

import Iconify from "src/components/iconify";

import { IScheduleStudentProp } from "src/types/course";

import MessageForm from "./message-form";
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
  const sendMessageFormOpen = useBoolean();

  const [messageStudents, setMessageStudents] = useState<IScheduleStudentProp[]>();

  const handleLessonCancel = useCallback(async () => {
    confirmCancellationFormOpen.onFalse();
    onConfirm(eventDetails);
  }, [confirmCancellationFormOpen, eventDetails, onConfirm]);

  const handleMessage = useCallback(
    async (students: IScheduleStudentProp[]) => {
      setMessageStudents(students);
      sendMessageFormOpen.onToggle();
    },
    [sendMessageFormOpen],
  );

  const isReady = useMemo(
    () => eventDetails.event.extendedProps.ready,
    [eventDetails.event.extendedProps.ready],
  );

  const canBeCancelled = useMemo(
    () => new Date() > eventDetails.event.start!,
    [eventDetails.event.start],
  );

  const students: IScheduleStudentProp[] = useMemo(
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
            rel="noopener"
            startIcon={<Iconify icon="logos:google-meet" />}
            sx={{ mr: 3 }}
            disabled={eventDetails.event.url === ""}
          >
            Dołącz
          </Button>
        </Stack>

        <DialogContent sx={{ py: 0 }}>
          <Stack direction="row" spacing={1}>
            <Typography>Minimalna ilość zapisów:</Typography>
            <Typography color={isReady ? "primary" : "error"}>
              {isReady ? "osiągnięta" : "nieosiągnięta"}
            </Typography>
          </Stack>

          <Stack direction="row" spacing={1}>
            <Typography>Aktualna liczba studentów:</Typography>
            <Typography color={isReady ? "primary" : "error"}>{students?.length ?? 0}</Typography>
          </Stack>

          {(students?.length ?? 0) > 0 && (
            <Stack
              direction="row"
              alignItems="center"
              justifyContent="space-between"
              spacing={1}
              paddingTop={2}
            >
              <Typography>Studenci:</Typography>
              <Button
                size="small"
                variant="text"
                endIcon={<Iconify icon="carbon:email" />}
                onClick={() => handleMessage(students)}
              >
                Napisz do wszystkich
              </Button>
            </Stack>
          )}

          <List
            sx={{
              width: "100%",
            }}
          >
            {students?.map((student: IScheduleStudentProp) => {
              const genderImageUrl = getGenderAvatar(student.gender);
              return (
                <ListItem
                  key={student.id}
                  alignItems="center"
                  secondaryAction={
                    <IconButton edge="end" onClick={() => handleMessage([student])}>
                      <Iconify icon="carbon:email" />
                    </IconButton>
                  }
                  sx={{ border: (t) => `solid 1px ${t.palette.divider}` }}
                >
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
            disabled={canBeCancelled}
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

      {messageStudents && (
        <MessageForm
          students={messageStudents}
          info={eventDetails.event}
          open={sendMessageFormOpen.value}
          onClose={sendMessageFormOpen.onFalse}
        />
      )}
    </>
  );
}
