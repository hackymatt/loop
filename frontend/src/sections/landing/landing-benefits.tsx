import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { useResponsive } from "src/hooks/use-responsive";

import Image from "src/components/image";

// ----------------------------------------------------------------------

const BENEFITS = [
  {
    title: "Przystępne koszty",
    description: "Rozpocznij naukę bez dużych wydatków, dopasowując wydatki do swojego budżetu.",
    iconColor: "success",
  },
  {
    title: "Elastyczny harmonogram",
    description: "Ucz się w dogodnym dla siebie czasie, dostosowując naukę do swojego trybu życia.",
    iconColor: "secondary",
  },
  {
    title: "Indywidualny wybór lekcji",
    description: "Dobierz lekcje zgodnie ze swoimi potrzebami i zainteresowaniami.",
    iconColor: "success",
  },
  {
    title: "Dowolność w wyborze nauczyciela",
    description:
      "Sam decydujesz, z kim chcesz się uczyć, wybierając instruktora najlepiej dopasowanego do Twoich oczekiwań.",
    iconColor: "secondary",
  },
  {
    title: "Certyfikaty ukończenia",
    description:
      "Zdobywaj certyfikaty, które potwierdzą Twoje umiejętności i wyróżnią Cię na rynku pracy.",
    iconColor: "success",
  },
  {
    title: "Nowoczesne technologie",
    description:
      "Poznaj najnowsze narzędzia i technologie, aby być zawsze o krok przed konkurencją.",
    iconColor: "secondary",
  },
];

// ----------------------------------------------------------------------

export default function LandingBenefits() {
  const mdUp = useResponsive("up", "md");

  return (
    <Box
      sx={{
        bgcolor: "background.neutral",
        py: { xs: 10, md: 15 },
      }}
    >
      <Container>
        <Typography variant="h2" sx={{ textAlign: "center" }}>
          Dlaczego warto wybrać{" "}
          <Box component="span" sx={{ color: "primary.main" }}>
            loop
          </Box>
          ?
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
          Nasza szkoła programowania oferuje nowoczesne podejście do nauki, elastyczność i wsparcie,
          które pomogą Ci osiągnąć sukces w branży IT.
        </Typography>

        <Box
          sx={{
            display: "grid",
            alignItems: "center",
            gap: { xs: 4, md: 8 },
            gridTemplateColumns: { md: "repeat(3, 1fr)" },
          }}
        >
          <Stack spacing={{ xs: 4, md: 10 }}>
            {BENEFITS.slice(0, 3).map((benefit, index) => (
              <BenefitItem key={benefit.title} benefit={benefit} index={index} reverse />
            ))}
          </Stack>

          {mdUp && <Image alt="benefits" src="/assets/illustrations/illustration-customer.svg" />}

          <Stack spacing={{ xs: 4, md: 10 }}>
            {BENEFITS.slice(-3).map((benefit, index) => (
              <BenefitItem key={benefit.title} benefit={benefit} index={index} />
            ))}
          </Stack>
        </Box>
      </Container>
    </Box>
  );
}

// ----------------------------------------------------------------------

type BenefitItemProps = {
  index: number;
  reverse?: boolean;
  benefit: {
    title: string;
    description: string;
    iconColor: string;
  };
};

function BenefitItem({ benefit, reverse, index }: BenefitItemProps) {
  const { title, description, iconColor } = benefit;

  return (
    <Stack
      spacing={1}
      direction={{ xs: "row", md: reverse ? "row-reverse" : "row" }}
      sx={{
        ...(reverse && {
          textAlign: { md: "right" },
        }),
        ...(index === 1 && {
          pl: { md: 6 },
          ...(reverse && {
            pl: { md: 0 },
            pr: { md: 6 },
          }),
        }),
      }}
    >
      <Box
        sx={{
          m: 1,
          width: 16,
          height: 16,
          flexShrink: 0,
          borderRadius: "50%",
          background: (theme) =>
            `linear-gradient(to bottom, ${theme.palette.primary.light}, ${theme.palette.primary.main})`,
          ...(iconColor === "secondary" && {
            background: (theme) =>
              `linear-gradient(to bottom, ${theme.palette.secondary.light}, ${theme.palette.secondary.main})`,
          }),
          ...(iconColor === "success" && {
            background: (theme) =>
              `linear-gradient(to bottom, ${theme.palette.success.light}, ${theme.palette.success.main})`,
          }),
        }}
      />

      <Stack spacing={1}>
        <Typography variant="h5">{title}</Typography>

        <Typography variant="body2" sx={{ color: "text.secondary" }}>
          {description}
        </Typography>
      </Stack>
    </Stack>
  );
}
