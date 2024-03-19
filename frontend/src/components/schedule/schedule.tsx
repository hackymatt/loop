"use client";

import React, { useCallback } from "react";
import { format, parseISO } from "date-fns";

import { StaticDatePicker } from "@mui/x-date-pickers";
import { Box, Tab, Tabs, Stack, Theme, Avatar, Typography } from "@mui/material";

// ----------------------------------------------------------------------

const MAX_WIDTH: number = 325 as const;

const TABS_STYLE = {
  "& .MuiTab-root": {
    "&:not(:last-of-type)": { marginRight: (theme: Theme) => theme.spacing(1) },
  },
};

// ----------------------------------------------------------------------

type User = { id: number; image: string; name: string };
type Props = {
  availableUsers: User[];
  currentUser: User;
  onUserChange: (event: React.SyntheticEvent, userId: number) => void;
  availableDates: string[];
  currentDate: string;
  onDateChange: (value: Date) => void;
  availableTimeSlots: string[];
  currentSlot: string;
  onSlotChange: (event: React.SyntheticEvent, slot: string) => void;
};

export default function Schedule({
  availableUsers,
  currentUser,
  onUserChange,
  availableDates,
  currentDate,
  onDateChange,
  availableTimeSlots,
  currentSlot,
  onSlotChange,
}: Props) {
  const handleDisableDates = useCallback(
    (date: Date | null) => {
      if (date) {
        return !availableDates.includes(format(date, "yyyy-MM-dd"));
      }
      return false;
    },
    [availableDates],
  );

  return (
    <Stack direction="column" alignItems="center">
      <Box sx={{ maxWidth: MAX_WIDTH }}>
        <Tabs
          value={currentUser?.id ?? ""}
          scrollButtons="auto"
          variant="scrollable"
          allowScrollButtonsMobile
          onChange={onUserChange}
          sx={TABS_STYLE}
        >
          {availableUsers?.map((u: User) => (
            <Tab
              key={u.id}
              value={u.id}
              icon={<Avatar key={u.id} src={u.image} />}
              label={
                <Typography
                  sx={{
                    fontSize: 12,
                    maxWidth: 50,
                    overflow: "hidden",
                  }}
                >
                  {u.name}
                </Typography>
              }
              iconPosition="top"
            />
          ))}
        </Tabs>
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
        shouldDisableDate={(value: Date | null) => handleDisableDates(value)}
      />

      <Box sx={{ maxWidth: MAX_WIDTH }}>
        <Tabs
          value={currentSlot}
          scrollButtons="auto"
          variant="scrollable"
          allowScrollButtonsMobile
          onChange={onSlotChange}
          sx={TABS_STYLE}
        >
          {availableTimeSlots?.map((ts: string) => <Tab key={ts} value={ts} label={ts} />)}
        </Tabs>
      </Box>
    </Stack>
  );
}
