"use client";

import { useState, useEffect, useCallback } from "react";

import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { useBoolean } from "src/hooks/use-boolean";
import { useResponsive } from "src/hooks/use-responsive";

import { lessonFAQ, accountFAQ, paymentFAQ, reservationFAQ, certificateFAQ } from "src/consts/faq";

import SupportHero from "../support/support-hero";
import SupportContent from "../support/support-content";
import SupportNav, { MoreHelp } from "../support/support-nav";

// ----------------------------------------------------------------------

const TOPICS = [
  {
    title: "Konto",
    icon: "/assets/icons/faq/ic_account.svg",
    content: accountFAQ,
  },
  {
    title: "Lekcje",
    icon: "/assets/icons/faq/ic_lesson.svg",
    content: lessonFAQ,
  },
  {
    title: "Rezerwacje",
    icon: "/assets/icons/faq/ic_booking.svg",
    content: reservationFAQ,
  },
  {
    title: "Certyfikat",
    icon: "/assets/icons/faq/ic_certificate.svg",
    content: certificateFAQ,
  },
  {
    title: "Płatność",
    icon: "/assets/icons/faq/ic_payment.svg",
    content: paymentFAQ,
  },
];

// ----------------------------------------------------------------------

export default function SupportView() {
  const mdUp = useResponsive("up", "md");

  const [topic, setTopic] = useState("Konto");
  const [searchText, setSearchText] = useState<string>("");

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

  const findMatches = (
    options: {
      question: string;
      answer: string;
    }[],
  ) =>
    options.filter(
      (option) =>
        option.question.toLowerCase().includes(searchText) ||
        option.answer.toLowerCase().includes(searchText),
    );

  return (
    <>
      <SupportHero onSearch={setSearchText} />

      <Container>
        <Typography variant="h3" sx={{ py: { xs: 3, md: 8 } }}>
          Pomoc
        </Typography>

        <Stack direction={mdUp ? "row" : "column"} sx={{ pb: { xs: 5, md: 15 } }}>
          <SupportNav
            data={TOPICS.map((t) => ({ ...t, content: findMatches(t.content) }))}
            topic={topic}
            open={mobileOpen.value}
            onChangeTopic={handleChangeTopic}
            onClose={mobileOpen.onFalse}
          />

          {TOPICS.map(
            (item) =>
              item.title === topic && (
                <div key={item.title}>
                  <SupportContent contents={findMatches(item.content)} />
                </div>
              ),
          )}
        </Stack>

        {!mdUp && <MoreHelp />}
      </Container>
    </>
  );
}
