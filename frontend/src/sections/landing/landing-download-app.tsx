import { useState } from "react";

import Grid from "@mui/material/Unstable_Grid2";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { alpha, styled } from "@mui/material/styles";
import Stack, { StackProps } from "@mui/material/Stack";
import Button, { buttonClasses } from "@mui/material/Button";
import {
  Box,
  Dialog,
  useTheme,
  IconButton,
  DialogProps,
  DialogTitle,
  DialogContent,
} from "@mui/material";

import { useBoolean } from "src/hooks/use-boolean";

import { bgGradient } from "src/theme/css";

import Image from "src/components/image";
import Iconify from "src/components/iconify";

// ----------------------------------------------------------------------

const StyledAppStoreButton = styled(Button)(({ theme }) => ({
  minWidth: 160,
  flexShrink: 0,
  padding: "5px 12px",
  color: theme.palette.common.white,
  border: `solid 1px ${alpha(theme.palette.common.black, 0.24)}`,
  background: `linear-gradient(180deg, ${theme.palette.grey[900]} 0%, ${theme.palette.common.black} 100%)`,
  [`& .${buttonClasses.startIcon}`]: {
    marginLeft: 0,
  },
}));

// ----------------------------------------------------------------------

export default function LandingDownloadApp() {
  const theme = useTheme();

  return (
    <Box
      component="section"
      sx={{
        ...bgGradient({
          color: `to bottom, ${alpha(theme.palette.background.default, 0.9)}, ${alpha(theme.palette.background.default, 0.9)}`,
          imgUrl: "/assets/background/overlay-1.webp",
        }),
        overflow: "hidden",
        position: "relative",
        py: { xs: 10, md: 20 },
      }}
    >
      <Box
        component="img"
        alt="Texture"
        src="/assets/background/texture-2.webp"
        sx={{
          top: 0,
          right: 0,
          opacity: 0.24,
          position: "absolute",
        }}
      />
      <Container sx={{ py: { xs: 8, md: 15 } }}>
        <Grid container spacing={3} justifyContent={{ lg: "space-between" }}>
          <Grid xs={12} md={6} lg={5}>
            <Stack
              sx={{
                textAlign: { xs: "center", md: "unset" },
              }}
            >
              <Typography variant="h2">
                Pobierz aplikację{" "}
                <Box component="span" sx={{ color: "primary.main" }}>
                  loop
                </Box>
              </Typography>

              <Typography sx={{ color: "text.secondary", mt: 3, mb: 8 }}>
                Pobierz aplikację{" "}
                <Box component="span" sx={{ color: "primary.main" }}>
                  loop
                </Box>{" "}
                i ucz się programowania gdziekolwiek jesteś! Dzięki niej masz szybki dostęp do
                kursów, materiałów edukacyjnych i harmonogramu zajęć. Rozwijaj swoje umiejętności w
                wygodny sposób, zawsze pod ręką.
              </Typography>
            </Stack>

            <Stack
              alignItems="center"
              sx={{
                py: 5,
                borderRadius: 2,
                mb: { xs: 8, md: 0 },
                px: { xs: 3, md: 5 },
                border: (t) => `solid 1px ${t.palette.divider}`,
              }}
            >
              <AppStoreButton direction={{ xs: "column", sm: "row" }} />
            </Stack>
          </Grid>

          <Grid xs={12} md={6} lg={6}>
            <Image
              alt="loop-app"
              src="assets/images/general/download-app.webp"
              sx={{
                maxWidth: 564,
                filter: (t) => `drop-shadow(0 48px 80px ${alpha(t.palette.common.black, 0.24)})`,
              }}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

// ----------------------------------------------------------------------

const Platform = { iOS: "iOS", Android: "Android" } as const;

type IPlatform = keyof typeof Platform;

function AppStoreButton({ ...other }: StackProps) {
  const downloadPromptOpen = useBoolean();

  const [platform, setPlatform] = useState<IPlatform>(Platform.iOS);

  return (
    <>
      <Stack direction="row" flexWrap="wrap" spacing={2} {...other}>
        <StyledAppStoreButton
          startIcon={<Iconify icon="bxl:apple" width={28} color="white" />}
          onClick={() => {
            setPlatform(Platform.iOS);
            downloadPromptOpen.onToggle();
          }}
        >
          <Stack alignItems="flex-start">
            <Typography variant="caption" sx={{ opacity: 0.72 }}>
              Zainstaluj na
            </Typography>

            <Typography variant="h6" sx={{ mt: -0.5 }}>
              iOS
            </Typography>
          </Stack>
        </StyledAppStoreButton>

        <StyledAppStoreButton
          startIcon={<Iconify icon="bxl:android" width={28} color="white" />}
          onClick={() => {
            setPlatform(Platform.Android);
            downloadPromptOpen.onToggle();
          }}
        >
          <Stack alignItems="flex-start">
            <Typography variant="caption" sx={{ opacity: 0.72 }}>
              Zainstaluj na
            </Typography>

            <Typography variant="h6" sx={{ mt: -0.5 }}>
              Android
            </Typography>
          </Stack>
        </StyledAppStoreButton>
      </Stack>
      <DownloadPrompt
        platform={platform}
        open={downloadPromptOpen.value}
        onClose={downloadPromptOpen.onFalse}
      />
    </>
  );
}

interface Props extends DialogProps {
  platform: IPlatform;
  onClose: VoidFunction;
}

function DownloadPrompt({ platform, onClose, ...other }: Props) {
  const content = (
    <Stack direction="column" spacing={1} pt={3} pb={3}>
      <Stack direction="row" spacing={0.5} justifyContent="left" alignItems="center">
        <Typography variant="body2">1. Kliknij na</Typography>
        <Iconify
          icon={
            platform === Platform.iOS ? "material-symbols:ios-share" : "material-symbols:more-vert"
          }
          width={28}
          sx={{ bgcolor: "background.neutral", p: 0.5, borderRadius: 1 }}
        />
        {platform === Platform.iOS ? "na dole ekranu" : "na górze ekranu"}
      </Stack>
      <Stack direction="row" spacing={0.5} justifyContent="left" alignItems="center">
        <Typography variant="body2">2. Wybierz opcję</Typography>
        {platform === Platform.iOS ? (
          <Stack
            direction="row"
            spacing={0.5}
            justifyContent="left"
            alignItems="center"
            sx={{ bgcolor: "background.neutral", p: 0.5, borderRadius: 1 }}
          >
            <Typography variant="body2">Do ekranu głównego</Typography>
            <Iconify icon="material-symbols:add-box-outline-rounded" />
          </Stack>
        ) : (
          <Stack
            direction="row"
            spacing={0.5}
            justifyContent="left"
            alignItems="center"
            sx={{ bgcolor: "background.neutral", p: 0.5, borderRadius: 1 }}
          >
            <Iconify icon="material-symbols:open-in-phone" />
            <Typography variant="body2">Dodaj do ekranu głównego</Typography>
          </Stack>
        )}
      </Stack>
    </Stack>
  );

  return (
    <Dialog fullWidth maxWidth="xs" onClose={onClose} {...other}>
      <Stack direction="row" justifyContent="space-between" alignItems="center" pb={2}>
        <DialogTitle sx={{ typography: "h6" }}>Zainstaluj aplikację</DialogTitle>
        <IconButton onClick={onClose} sx={{ p: 3 }}>
          <Iconify icon="carbon:close" />
        </IconButton>
      </Stack>

      <DialogContent sx={{ py: 0, typography: "body2" }}>
        Zainstaluj aplikację na swoim urządzeniu, aby mieć łatwy dostęp do nauki w każdej chwili.
        Bez {platform === Platform.iOS ? "App Store" : "Google Play"}, bez pobierania, bez
        problemów. {content}
      </DialogContent>
    </Dialog>
  );
}
