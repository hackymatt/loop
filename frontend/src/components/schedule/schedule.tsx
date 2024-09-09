"use client";

import React from "react";
import { parseISO } from "date-fns";
import { polishPlurals } from "polish-plurals";

import { StaticDatePicker } from "@mui/x-date-pickers";
import {
  Box,
  Tabs,
  Chip,
  Stack,
  Theme,
  Alert,
  Avatar,
  Typography,
  CircularProgress,
} from "@mui/material";

import { fDate } from "src/utils/format-time";

import { ITeamMemberProps } from "src/types/team";

// ----------------------------------------------------------------------

const MAX_WIDTH: number = 325 as const;

const TABS_STYLE = {
  "& .MuiTab-root": {
    color: (theme: Theme) => theme.palette.text.primary,
    "&:not(:last-of-type)": { marginRight: (theme: Theme) => theme.spacing(1) },
  },
  "& .MuiTabs-scrollButtons.Mui-disabled": {
    opacity: 0.3,
  },
};

const CHIP_STYLE = { p: 1, mt: 1, ml: 0.25, mr: 0.25 };

// ----------------------------------------------------------------------

type Props = {
  availableUsers: ITeamMemberProps[];
  currentUser: ITeamMemberProps;
  onUserChange: (event: React.SyntheticEvent, userId: string) => void;
  currentDate: string;
  onDateChange: (value: Date) => void;
  availableTimeSlots: { time: string; studentsRequired: number }[];
  currentSlot: string;
  onSlotChange?: (event: React.SyntheticEvent, slot: string) => void;
  availableDates: string[];
  onMonthChange: (month: string) => void;
  isLoadingUsers?: boolean;
  isLoadingTimeSlots?: boolean;
  error?: string;
};

export default function Schedule({
  availableUsers,
  currentUser,
  onUserChange,
  currentDate,
  onDateChange,
  availableTimeSlots,
  currentSlot,
  onSlotChange,
  availableDates,
  onMonthChange,
  isLoadingUsers,
  isLoadingTimeSlots,
  error,
}: Props) {
  const selectedTimeSlot = availableTimeSlots?.find(
    (ts: { time: string; studentsRequired: number }) => ts.time === currentSlot,
  );

  const isDisabledDate = (date: string) => !availableDates.includes(date);

  return (
    <Stack direction="column" alignItems="center">
      <Box sx={{ maxWidth: MAX_WIDTH }}>
        {isLoadingUsers ? (
          <Box sx={{ p: 0.7 }}>
            <CircularProgress size={30} />
          </Box>
        ) : (
          <Tabs
            value={currentUser?.id ?? ""}
            scrollButtons="auto"
            variant="scrollable"
            allowScrollButtonsMobile
            onChange={onUserChange}
            sx={TABS_STYLE}
          >
            {availableUsers?.map((u: ITeamMemberProps) => (
              <Chip
                key={u.id}
                avatar={<Avatar alt={u.name} src={u.avatarUrl} />}
                label={u.name}
                size="medium"
                sx={CHIP_STYLE}
                variant={currentUser.id === u.id ? "filled" : "outlined"}
                color="primary"
                onClick={(event) => onUserChange && onUserChange(event, u.id)}
              />
            ))}
          </Tabs>
        )}
      </Box>
      <StaticDatePicker
        defaultValue={parseISO(currentDate)}
        value={parseISO(currentDate) ?? new Date()}
        disablePast
        onChange={(value: Date | null) => {
          if (value) {
            onDateChange(value);
          }
        }}
        slotProps={{ actionBar: { actions: [] }, toolbar: { hidden: true } }}
        views={["day"]}
        shouldDisableDate={(date) => isDisabledDate(fDate(date, "yyyy-MM-dd"))}
        onMonthChange={(date) => {
          onMonthChange(fDate(date, "yyyy-MM"));
        }}
      />

      <Box sx={{ maxWidth: MAX_WIDTH }}>
        {!isLoadingTimeSlots && availableTimeSlots.length === 0 && (
          <Alert severity="info" variant="outlined">
            Brak dostępnych terminów
          </Alert>
        )}

        {isLoadingTimeSlots && (
          <Box sx={{ p: 0.7 }}>
            <CircularProgress size={30} />
          </Box>
        )}

        {!isLoadingTimeSlots && availableTimeSlots.length > 0 && (
          <>
            <Tabs
              value={currentSlot ?? false}
              scrollButtons
              variant="scrollable"
              allowScrollButtonsMobile
              onChange={onSlotChange}
              sx={
                onSlotChange
                  ? TABS_STYLE
                  : {
                      ...TABS_STYLE,
                      "& .MuiTabs-indicator": {
                        display: "none",
                      },
                    }
              }
            >
              {availableTimeSlots?.map((ts: { time: string; studentsRequired: number }) => (
                <Chip
                  key={ts.time}
                  label={ts.time}
                  sx={CHIP_STYLE}
                  variant={currentSlot === ts.time ? "filled" : "outlined"}
                  color="primary"
                  onClick={(event) => onSlotChange && onSlotChange(event, ts.time)}
                />
              ))}
            </Tabs>
            {(selectedTimeSlot?.studentsRequired ?? 0) === 0 ? (
              <Alert severity="success" variant="outlined">
                Osiągnięto limit zgłoszeń
              </Alert>
            ) : (
              <Alert severity="warning" variant="outlined">
                Nie osiągnięto limitu zgłoszeń, wymagane jeszcze{" "}
                {selectedTimeSlot?.studentsRequired ?? 0}{" "}
                {polishPlurals(
                  "zapis",
                  "zapisy",
                  "zapisów",
                  selectedTimeSlot?.studentsRequired ?? 0,
                )}
              </Alert>
            )}
          </>
        )}
      </Box>

      {error && (
        <Typography variant="body2" color="error">
          {error}
        </Typography>
      )}
    </Stack>
  );
}
