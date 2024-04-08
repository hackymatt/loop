import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import Logo from "src/components/logo";

// ----------------------------------------------------------------------

export default function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer>
      <Container sx={{ py: 8, textAlign: "center" }}>
        <Logo single />

        <Typography variant="caption" component="div" sx={{ color: "text.secondary" }}>
          {`© ${currentYear}. Wszelkie prawa zastrzeżone`}
        </Typography>
      </Container>
    </footer>
  );
}
