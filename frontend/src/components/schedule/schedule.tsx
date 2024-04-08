"use client";

import React from "react";
import { parseISO } from "date-fns";

import styled from "@mui/system/styled";
import { StaticDatePicker } from "@mui/x-date-pickers";
import {
  Box,
  Tab,
  Tabs,
  Stack,
  Theme,
  Badge,
  Avatar,
  Tooltip,
  Typography,
  BadgeProps,
  CircularProgress,
} from "@mui/material";

import { ITeamMemberProps } from "src/types/team";

// ----------------------------------------------------------------------

const MAX_WIDTH: number = 325 as const;

const TABS_STYLE = {
  "& .MuiTab-root": {
    color: (theme: Theme) => theme.palette.text.primary,
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
  availableTimeSlots: { time: string; studentsCount: number }[];
  currentSlot: string;
  onSlotChange?: (event: React.SyntheticEvent, slot: string) => void;
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
  isLoadingUsers,
  isLoadingTimeSlots,
  error,
}: Props) {
  const StyledBadge = styled(Badge)<BadgeProps>(({ theme }) => ({
    "& .MuiBadge-badge": {
      right: 4,
      border: `2px solid ${theme.palette.background.paper}`,
      padding: "4px",
    },
  }));

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
      />

      <Box sx={{ maxWidth: MAX_WIDTH }}>
        {isLoadingTimeSlots ? (
          <Box sx={{ p: 0.7 }}>
            <CircularProgress size={30} />
          </Box>
        ) : (
          <Tabs
            value={currentSlot ?? false}
            scrollButtons="auto"
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
            {availableTimeSlots.length > 0 ? (
              availableTimeSlots?.map((ts: { time: string; studentsCount: number }) => (
                <Tab
                  key={ts.time}
                  value={ts.time}
                  label={
                    <Tooltip title={`Liczba zapisów: ${ts.studentsCount}`} placement="top">
                      <StyledBadge badgeContent={ts.studentsCount} color="primary">
                        <Typography
                          variant="body2"
                          sx={{
                            border: (theme) => `solid 1px ${theme.palette.grey[500]}`,
                            p: 1,
                            borderRadius: 1,
                          }}
                        >
                          {ts.time}
                        </Typography>
                      </StyledBadge>
                    </Tooltip>
                  }
                  sx={{ p: 1 }}
                />
              ))
            ) : (
              <Typography variant="body2">Brak dostępnych terminów</Typography>
            )}
          </Tabs>
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
