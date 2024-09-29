import { Link, Typography } from "@mui/material";

import { paths } from "src/routes/paths";

export const generalAcceptance = (
  <Typography variant="caption" align="left" sx={{ color: "text.secondary", textAlign: "justify" }}>
    Akceptuję{" "}
    <Link
      target="_blank"
      rel="noopener"
      href={paths.termsAndConditions}
      color="text.primary"
      underline="always"
    >
      regulamin
    </Link>{" "}
    oraz{" "}
    <Link
      target="_blank"
      rel="noopener"
      href={paths.privacyPolicy}
      color="text.primary"
      underline="always"
    >
      politykę prywatności.
    </Link>
  </Typography>
);

export const dataAcceptance = (
  <Typography variant="caption" align="left" sx={{ color: "text.secondary", textAlign: "justify" }}>
    Wyrażam zgodę na przetwarzanie moich danych osobowych zawartych w formularzu w celu i zakresie
    niezbędnym do realizacji usługi i tylko w takim celu.
  </Typography>
);

export const newsletterAcceptance = (
  <Typography variant="caption" align="left" sx={{ color: "text.secondary", textAlign: "justify" }}>
    Wyrażam zgodę na otrzymywanie na podany adres poczty elektronicznej informacji handlowych
    dotyczących usług oraz w celu otrzymywania newslettera — więcej informacji uzyskają Państwo{" "}
    <Link
      target="_blank"
      rel="noopener"
      href={paths.privacyPolicy}
      color="text.primary"
      underline="always"
    >
      tutaj
    </Link>
    .
  </Typography>
);
