import { toPng } from "html-to-image";
import { useRef, useMemo } from "react";

import { Stack, Button, Container, Typography } from "@mui/material";

import { fDate } from "src/utils/format-time";

import { grey } from "src/theme/palette";
import { BASE_URL } from "src/config-global";
import { useCertificate } from "src/api/certificate/certificate";

import Logo from "src/components/logo";
import Iconify from "src/components/iconify";
import { useToastContext } from "src/components/toast";
import { SplashScreen } from "src/components/loading-screen";

import NotFoundView from "../error/not-found-view";

interface IProps {
  id: string;
}

export default function Certificate({ id }: IProps) {
  const elementRef = useRef(null);

  const { enqueueSnackbar } = useToastContext();

  const { data: certificateData, isLoading } = useCertificate(id);

  const authorized = useMemo(
    () => certificateData?.isAuthorized ?? false,
    [certificateData?.isAuthorized],
  );

  const certificateUrl = useMemo(() => `${BASE_URL}/certificate/${id}`, [id]);

  const type = useMemo(() => {
    switch (certificateData.type) {
      case "Lekcja":
        return "LEKCJI";
      case "Moduł":
        return "MODUŁU";
      case "Kurs":
        return "KURSU";
      default:
        return "LEKCJI";
    }
  }, [certificateData.type]);

  if (isLoading) {
    return <SplashScreen />;
  }

  if (Object.keys(certificateData).length === 0) {
    return <NotFoundView />;
  }

  const downloadPng = () => {
    if (elementRef.current === null) {
      return;
    }

    toPng(elementRef.current, { cacheBust: false, style: { marginTop: "0" } })
      .then((dataUrl) => {
        const link = document.createElement("a");
        link.download = `certificate_${certificateData.referenceNumber}.png`;
        link.href = dataUrl;
        link.click();
      })
      .catch((err) => {
        enqueueSnackbar("Wystąpił błąd podczas pobierania", { variant: "error" });
      });
  };

  return (
    <Container
      ref={elementRef}
      sx={{
        height: "80%",
        p: 5,
        mt: 2,
        borderStyle: "solid",
        borderWidth: "thin",
        borderColor: grey[300],
        borderRadius: "8px",
        backgroundColor: grey[100],
      }}
    >
      <Stack spacing={8}>
        <Stack direction="row" justifyContent="space-between">
          <Logo sx={{ width: "200px", ml: 16 }} />
          <Stack spacing={0.5} alignItems="flex-end">
            <Typography variant="caption" color={grey[600]}>
              {`Numer certyfikatu: ${id}`}
            </Typography>
            <Typography variant="caption" color={grey[600]}>
              {`Link certyfikatu: ${certificateUrl}`}
            </Typography>
            <Typography variant="caption" color={grey[600]}>
              {`Numer referencyjny: ${certificateData.referenceNumber}`}
            </Typography>
          </Stack>
        </Stack>

        <Stack spacing={1} sx={{ minHeight: "300px", maxHeight: "350px" }}>
          <Typography variant="h6" color={grey[600]} sx={{ fontWeight: "bold" }}>
            {`CERTYFIKAT UKOŃCZENIA ${type}`}
          </Typography>
          <Typography variant="h1">{certificateData.title}</Typography>
        </Stack>

        <Stack spacing={2}>
          <Typography variant="h2">{certificateData.studentName}</Typography>
          <Stack spacing={0.5}>
            <Stack direction="row" spacing={1}>
              <Typography variant="body1" color={grey[800]}>
                Data ukończenia
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                {fDate(certificateData.completedAt)}
              </Typography>
            </Stack>

            <Stack direction="row" spacing={1}>
              <Typography variant="body1" color={grey[800]}>
                Czas trwania
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: "bold" }}>
                {`${certificateData.duration} minut`}
              </Typography>
            </Stack>
          </Stack>
        </Stack>

        {authorized && (
          <Stack direction="row" spacing={1} justifyContent="flex-end">
            <Button
              variant="contained"
              startIcon={<Iconify icon="carbon:download" />}
              onClick={downloadPng}
            >
              Pobierz
            </Button>
            <Button
              component="a"
              target="_blank"
              href={`https://www.linkedin.com/sharing/share-offsite/?url=${certificateUrl}`}
              variant="contained"
              startIcon={<Iconify icon="carbon:logo-linkedin" />}
              sx={{ backgroundColor: "#007EBB" }}
            >
              Udostępnij
            </Button>
          </Stack>
        )}
      </Stack>
    </Container>
  );
}
