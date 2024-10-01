import { useForm } from "react-hook-form";
import { useMemo, useState, useCallback } from "react";

import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";
import {
  Switch,
  Accordion,
  Typography,
  AccordionDetails,
  AccordionSummary,
  FormControlLabel,
  accordionSummaryClasses,
} from "@mui/material";

import { cookies } from "src/consts/cookies";

import FormProvider from "src/components/hook-form";

import Iconify from "../iconify";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onConfirm: (cookies: { [cookie: string]: boolean }) => void;
}

// ----------------------------------------------------------------------

export default function CookiesSettings({ onConfirm, ...other }: Props) {
  const methods = useForm();

  const defaultCookies = useMemo(
    () =>
      cookies.reduce((acc: { [cookie: string]: boolean }, cookie) => {
        acc[cookie.type] = true;
        return acc;
      }, {}),
    [],
  );

  const [settings, setSettings] = useState<{ [cookie: string]: boolean }>(defaultCookies);
  const [expanded, setExpanded] = useState<string | false>(false);

  const handleChangeExpanded = useCallback(
    (panel: string) => (event: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    },
    [],
  );

  return (
    <Dialog fullWidth maxWidth="xs" {...other}>
      <FormProvider methods={methods}>
        <DialogTitle sx={{ typography: "h6", pb: 3 }}>Zarządzaj cookies</DialogTitle>

        <DialogContent sx={{ py: 0, typography: "body2" }}>
          {cookies.map((cookie, index) => (
            <Accordion
              key={index}
              expanded={expanded === cookie.title}
              onChange={handleChangeExpanded(cookie.title)}
            >
              <AccordionSummary
                sx={{
                  py: 2,
                  [`& .${accordionSummaryClasses.content}`]: {
                    p: 0,
                    m: 0,
                  },
                  [`&.${accordionSummaryClasses.expanded}`]: {
                    bgcolor: "action.selected",
                  },
                }}
              >
                <Iconify
                  icon={expanded === cookie.title ? "eva:minus-outline" : "eva:plus-outline"}
                  sx={{ mr: 0.5, width: 12 }}
                />

                <Typography variant="subtitle2" sx={{ flexGrow: 1 }}>
                  {cookie.title}
                </Typography>

                <FormControlLabel
                  control={
                    <Switch
                      checked={settings[cookie.type]}
                      disabled={cookie.disabled}
                      size="small"
                      onClick={(event) => {
                        event.preventDefault();
                        event.stopPropagation();
                        setSettings((prev) => ({ ...prev, [cookie.type]: !settings[cookie.type] }));
                      }}
                    />
                  }
                  label={cookie.disabled ? "Wymagane" : "Opcjonalne"}
                  labelPlacement="start"
                />
              </AccordionSummary>

              <AccordionDetails sx={{ color: "text.secondary" }}>
                {cookie.description}
              </AccordionDetails>
            </Accordion>
          ))}
        </DialogContent>

        <DialogActions sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
          <Button variant="contained" onClick={() => onConfirm(defaultCookies)} color="success">
            Akceptuję wszystkie
          </Button>
          <Button variant="text" onClick={() => onConfirm(settings)} size="small">
            Akceptuję wybrane
          </Button>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
