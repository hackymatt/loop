"use client";

import React from "react";
import { parseISO } from "date-fns";

import { StaticDatePicker } from "@mui/x-date-pickers";
import { Box, Tab, Tabs, Stack, Theme, Avatar, Typography } from "@mui/material";

import { ITeamMemberProps } from "src/types/team";

// ----------------------------------------------------------------------

const MAX_WIDTH: number = 325 as const;

const TABS_STYLE = {
  "& .MuiTab-root": {
    "&:not(:last-of-type)": { marginRight: (theme: Theme) => theme.spacing(1) },
  },
};

// ----------------------------------------------------------------------

type Props = {
  availableUsers: ITeamMemberProps[];
  currentUser: ITeamMemberProps;
  onUserChange: (event: React.SyntheticEvent, userId: string) => void;
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
  currentDate,
  onDateChange,
  availableTimeSlots,
  currentSlot,
  onSlotChange,
}: Props) {
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
          {availableUsers?.map((u: ITeamMemberProps) => (
            <Tab
              key={u.id}
              value={u.id}
              icon={<Avatar key={u.id} src={u.avatarUrl} />}
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
      />

      <Box sx={{ maxWidth: MAX_WIDTH }}>
        {availableTimeSlots.length > 0 ? (
          <Tabs
            value={currentSlot ?? availableTimeSlots[0]}
            scrollButtons="auto"
            variant="scrollable"
            allowScrollButtonsMobile
            onChange={onSlotChange}
            sx={TABS_STYLE}
          >
            {availableTimeSlots?.map((ts: string) => <Tab key={ts} value={ts} label={ts} />)}
          </Tabs>
        ) : (
          <Typography variant="body2">Brak dostępnych terminów</Typography>
        )}
      </Box>
    </Stack>
  );
}
