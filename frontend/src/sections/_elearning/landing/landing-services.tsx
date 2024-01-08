import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import Image from "src/components/image";
import TextMaxLine from "src/components/text-max-line";

// ----------------------------------------------------------------------

const COLORS = ["primary", "secondary", "success", "warning"] as const;

const SERVICES = [
  {
    name: "Niski próg wejścia",
    icon: "/assets/icons/ic_savings.svg",
    content: "Nie wydajesz dużej kwoty",
  },
  {
    name: "Elastyczna edukacja",
    icon: "/assets/icons/ic_time.svg",
    content: "Decydujesz kiedy się uczysz",
  },
  {
    name: "Zakup pojedynczej lekcji",
    icon: "/assets/icons/ic_lesson.svg",
    content: "Wybierasz interesujące Cię lekcje",
  },
  {
    name: "Wybór nauczyciela",
    icon: "/assets/icons/ic_teacher.svg",
    content: "Wybierasz instruktora dla każdej lekcji",
  },
];

// ----------------------------------------------------------------------

export default function LandingServices() {
  return (
    <Container
      sx={{
        py: { xs: 5, md: 10 },
      }}
    >
      <Stack
        spacing={3}
        sx={{
          maxWidth: 480,
          mb: { xs: 8, md: 5 },
          mx: { xs: "auto", md: "unset" },
          textAlign: { xs: "center", md: "unset" },
        }}
      >
        <Typography
          variant="overline"
          sx={{
            display: "block",
            color: "primary.main",
          }}
        >
          Co nas wyróżnia
        </Typography>

        <Typography variant="h3">Nauka programowania inaczej</Typography>

        <Typography sx={{ color: "text.secondary" }}>
          Nasza szkoła programowania stosuje nowoczesne rozwiązania.
        </Typography>
      </Stack>

      <Box
        sx={{
          gap: 4,
          display: "grid",
          alignItems: "center",
          gridTemplateColumns: {
            xs: "repeat(1, 1fr)",
            sm: "repeat(2, 1fr)",
            md: "repeat(4, 1fr)",
          },
        }}
      >
        {SERVICES.map((service, index) => (
          <ServiceItem key={service.name} service={service} index={index} />
        ))}
      </Box>
    </Container>
  );
}

// ----------------------------------------------------------------------

type ServiceItemProps = {
  service: {
    name: string;
    content: string;
    icon: string;
  };
  index: number;
};

function ServiceItem({ service, index }: ServiceItemProps) {
  const { name, icon, content } = service;

  return (
    <Card
      sx={{
        px: 4,
        py: 5,
        textAlign: "center",
        ...(index === 1 && {
          py: { xs: 5, md: 8 },
        }),
        ...(index === 2 && {
          py: { xs: 5, md: 10 },
          boxShadow: (theme) => ({ md: theme.customShadows.z24 }),
        }),
      }}
    >
      <Image
        visibleByDefault
        disabledEffect
        alt="icon"
        src={icon}
        sx={{
          width: "auto",
          height: 88,
        }}
      />

      <Stack spacing={1} sx={{ my: 5 }}>
        <TextMaxLine variant="h6">{name}</TextMaxLine>
        <TextMaxLine variant="body2" sx={{ color: "text.secondary" }}>
          {content}
        </TextMaxLine>
      </Stack>
    </Card>
  );
}
