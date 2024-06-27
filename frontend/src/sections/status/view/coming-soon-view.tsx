"use client";

import { polishPlurals } from "polish-plurals";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";

import { useCountdown } from "src/hooks/use-countdown";

import Image from "src/components/image";

import { NewsletterEmail } from "src/sections/newsletter/newsletter";

// ----------------------------------------------------------------------

export default function ComingSoonView({ startDate }: { startDate?: Date }) {
  const { days, hours, minutes, seconds } = useCountdown(startDate ?? new Date("10/01/2024 00:00"));

  return (
    <>
      <Typography variant="h3" paragraph>
        Już wkrótce!
      </Typography>

      <Typography sx={{ color: "text.secondary" }}>
        Obecnie ciężko pracujemy nad tą stroną!
      </Typography>

      <Image
        alt="comingsoon"
        src="/assets/illustrations/illustration_comingsoon.svg"
        sx={{
          my: 3,
          mx: "auto",
          maxWidth: 320,
        }}
      />

      <Stack
        direction="row"
        justifyContent="center"
        divider={<Box sx={{ mx: { xs: 1, sm: 2.5 } }}>:</Box>}
        sx={{ typography: "h2" }}
      >
        <TimeBlock label={polishPlurals("Dzień", "Dni", "Dni", parseInt(days, 10))} value={days} />

        <TimeBlock
          label={polishPlurals("Godzina", "Godziny", "Godzin", parseInt(hours, 10))}
          value={hours}
        />

        <TimeBlock
          label={polishPlurals("Minuta", "Minuty", "Minut", parseInt(minutes, 10))}
          value={minutes}
        />

        <TimeBlock
          label={polishPlurals("Sekunda", "Sekundy", "Sekund", parseInt(seconds, 10))}
          value={seconds}
        />
      </Stack>

      <Stack sx={{ mt: 3 }}>
        <NewsletterEmail buttonLabel="Powiadom" sx={{ mt: 0.3 }} />
      </Stack>
    </>
  );
}

// ----------------------------------------------------------------------

type TimeBlockProps = {
  label: string;
  value: string;
};

function TimeBlock({ label, value }: TimeBlockProps) {
  return (
    <div>
      <Box> {value} </Box>
      <Box sx={{ color: "text.secondary", typography: "body1" }}>{label}</Box>
    </div>
  );
}
