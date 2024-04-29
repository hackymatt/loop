"use client";

import { useState, useEffect, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";

import { useBoolean } from "src/hooks/use-boolean";

import { lessonFAQ, accountFAQ, paymentFAQ, reservationFAQ } from "src/consts/faq";

import Iconify from "src/components/iconify";

import SupportNav from "../support/support-nav";
import SupportContent from "../support/support-content";

// ----------------------------------------------------------------------

const TOPICS = [
  {
    title: "Konto",
    icon: "/assets/icons/faq/ic_account.svg",
    content: <SupportContent contents={accountFAQ} />,
  },
  {
    title: "Lekcje",
    icon: "/assets/icons/faq/ic_lesson.svg",
    content: <SupportContent contents={lessonFAQ} />,
  },
  {
    title: "Rezerwacje",
    icon: "/assets/icons/faq/ic_booking.svg",
    content: <SupportContent contents={reservationFAQ} />,
  },
  {
    title: "Płatność",
    icon: "/assets/icons/faq/ic_payment.svg",
    content: <SupportContent contents={paymentFAQ} />,
  },
];

// ----------------------------------------------------------------------

export default function SupportView() {
  const [topic, setTopic] = useState("Konto");

  const mobileOpen = useBoolean();

  const handleChangeTopic = useCallback((event: React.SyntheticEvent, newValue: string) => {
    setTopic(newValue);
  }, []);

  useEffect(() => {
    if (mobileOpen.value) {
      mobileOpen.onFalse();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topic]);

  return (
    <>
      <Stack
        alignItems="flex-end"
        sx={{
          py: 1.5,
          px: 2.5,
          display: { md: "none" },
          borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
        }}
      >
        <IconButton onClick={mobileOpen.onTrue}>
          <Iconify icon="carbon:menu" />
        </IconButton>
      </Stack>

      <Container>
        <Typography variant="h3" sx={{ py: { xs: 3, md: 10 } }}>
          Często zadawane pytania
        </Typography>

        <Stack direction="row" sx={{ pb: { xs: 10, md: 15 } }}>
          <SupportNav
            data={TOPICS}
            topic={topic}
            open={mobileOpen.value}
            onChangeTopic={handleChangeTopic}
            onClose={mobileOpen.onFalse}
          />

          {TOPICS.map((item) => item.title === topic && <div key={item.title}>{item.content}</div>)}
        </Stack>
      </Container>
    </>
  );
}
