"use client";

import { m } from "framer-motion";
import { useRef, useMemo, useState, useEffect } from "react";

import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Container from "@mui/material/Container";
import { CircularProgress } from "@mui/material";
import Typography from "@mui/material/Typography";

import { paths } from "src/routes/paths";
import { useRouter } from "src/routes/hooks";

import { useQueryParams } from "src/hooks/use-query-params";

import { usePaymentStatus } from "src/api/payment/payment-status";

import { varBounce, MotionContainer } from "src/components/animate";

import { PaymentStatus } from "src/types/payment";

// ----------------------------------------------------------------------

export default function OrderStatusView() {
  const { push } = useRouter();
  const { getQueryParams } = useQueryParams();

  const queryParams = useMemo(() => getQueryParams(), [getQueryParams]);

  const [sessionId, setSessionId] = useState<string>("");

  const { data: paymentStatusData } = usePaymentStatus(
    { session_id: sessionId },
    sessionId !== "",
    1000,
  );

  const effectRan = useRef(false);
  useEffect(() => {
    const { session_id } = queryParams;
    if (session_id) {
      if (!effectRan.current) {
        setSessionId(session_id);
        effectRan.current = true;
      }
    }
  }, [queryParams]);

  useEffect(() => {
    if (paymentStatusData) {
      const { status } = paymentStatusData;

      switch (status) {
        case PaymentStatus.SUCCESS:
          push(paths.order.completed);
          break;

        case PaymentStatus.FAILURE:
          push(paths.order["not-completed"]);
          break;

        default:
          break;
      }
    }
  }, [paymentStatusData, push]);

  return (
    <Container
      component={MotionContainer}
      sx={{
        textAlign: "center",
        pt: { xs: 5, md: 10 },
        pb: { xs: 10, md: 20 },
      }}
    >
      <m.div variants={varBounce().in}>
        <Box sx={{ fontSize: 128 }}>
          <CircularProgress size={50} />
        </Box>
      </m.div>

      <Stack spacing={1} sx={{ my: 5 }}>
        <Typography variant="h3">Oczekiwanie na płatność...</Typography>
      </Stack>
    </Container>
  );
}
