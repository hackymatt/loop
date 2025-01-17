import Box from "@mui/material/Box";
import Timeline from "@mui/lab/Timeline";
import TimelineDot from "@mui/lab/TimelineDot";
import Container from "@mui/material/Container";
import TimelineItem from "@mui/lab/TimelineItem";
import Typography from "@mui/material/Typography";
import TimelineContent from "@mui/lab/TimelineContent";
import { alpha, useTheme } from "@mui/material/styles";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineSeparator from "@mui/lab/TimelineSeparator";

import { useResponsive } from "src/hooks/use-responsive";

import { bgGradient } from "src/theme/css";

// ----------------------------------------------------------------------

const TIMELINES = [
  {
    step: "KROK 1",
    title: "Załóż konto",
    description: "Zarejestruj się, aby uzyskać dostęp do naszej platformy i rozpocząć naukę.",
  },
  {
    step: "KROK 2",
    title: "Znajdź lekcje",
    description:
      "Przeglądaj dostępne lekcje i wybierz te, które najlepiej odpowiadają Twoim potrzebom.",
  },
  {
    step: "KROK 3",
    title: "Dodaj do koszyka",
    description: "Dodaj wybrane lekcje do koszyka i przygotuj się do zakupu.",
  },
  {
    step: "KROK 4",
    title: "Dokonaj zakupu",
    description: "Sfinalizuj transakcję, aby zarezerwować wybrane lekcje.",
  },
  {
    step: "KROK 5",
    title: "Wybierz termin i nauczyciela",
    description:
      "Zarezerwuj dogodny termin oraz wybierz nauczyciela, który poprowadzi Twoje zajęcia.",
  },
];

const COLORS = ["primary", "secondary", "warning", "info", "error"] as const;

// ----------------------------------------------------------------------

export default function LandingHowItWork() {
  const theme = useTheme();

  const mdUp = useResponsive("up", "md");

  return (
    <Box
      sx={{
        ...bgGradient({
          color: alpha(theme.palette.grey[900], 0.8),
          imgUrl: "/assets/background/overlay-2.webp",
        }),
        color: "common.white",
        py: { xs: 10, md: 15 },
      }}
    >
      <Container>
        <Typography variant="h2" sx={{ textAlign: "center" }}>
          Jak to działa
        </Typography>

        <Typography
          sx={{
            mt: 3,
            mx: "auto",
            opacity: 0.72,
            maxWidth: 480,
            textAlign: "center",
            mb: { xs: 8, md: 10 },
          }}
        >
          Zacznij swoją przygodę z nauką programowania w kilku prostych krokach. Od założenia konta,
          przez wybór lekcji, aż po rezerwację terminu z nauczycielem – wszystko jest szybkie i
          intuicyjne!
        </Typography>

        <Timeline position={mdUp ? "alternate" : "right"}>
          {TIMELINES.map((value, index) => (
            <TimelineItem
              key={value.title}
              sx={{
                "&:before": {
                  ...(!mdUp && { display: "none" }),
                },
              }}
            >
              <TimelineSeparator>
                <TimelineDot color={COLORS[index]} />
                <TimelineConnector />
              </TimelineSeparator>

              <TimelineContent sx={{ pb: { xs: 3, md: 5 } }}>
                <Typography variant="overline" sx={{ color: `${COLORS[index]}.main` }}>
                  {value.step}
                </Typography>

                <Typography variant="h4" sx={{ mt: 0.5, mb: 1 }}>
                  {value.title}
                </Typography>

                <Typography
                  variant="body2"
                  sx={{
                    opacity: 0.72,
                    maxWidth: { md: 360 },
                    ...(index % 2 && {
                      ml: "auto",
                    }),
                  }}
                >
                  {value.description}
                </Typography>
              </TimelineContent>
            </TimelineItem>
          ))}
        </Timeline>
      </Container>
    </Box>
  );
}
