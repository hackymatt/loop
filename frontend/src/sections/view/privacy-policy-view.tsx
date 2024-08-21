"use client";

import { Box, Link } from "@mui/material";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

import { privacyPolicy } from "src/consts/privacyPolicy";

// ----------------------------------------------------------------------

export default function PrivacyPolicyView() {
  return (
    <Container sx={{ mb: 10 }}>
      <Typography variant="h3" sx={{ py: { xs: 3, md: 10 } }}>
        Polityka prywatności
      </Typography>

      {privacyPolicy.map((section) => (
        <Link href={`#${section.header}`}>
          <Typography>{section.header}</Typography>
        </Link>
      ))}

      <Box sx={{ mt: 10 }}>
        {privacyPolicy.map((section) => (
          <Box key={section.header}>
            <Box
              id={section.header}
              sx={{ display: "block", position: "relative", top: "-100px", hidden: "true" }}
            />
            <Box sx={{ mt: 4 }}>
              <Typography align="center" fontWeight="bold" sx={{ mb: 2 }}>
                {section.header}
              </Typography>
              <Box>{section.content}</Box>
            </Box>
          </Box>
        ))}
      </Box>
    </Container>
  );
}
