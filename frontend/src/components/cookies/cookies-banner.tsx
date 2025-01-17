import { useForm } from "react-hook-form";

import { Link } from "@mui/material";
import Button from "@mui/material/Button";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { paths } from "src/routes/paths";

import { useBoolean } from "src/hooks/use-boolean";
import { useCookies } from "src/hooks/use-cookies";

import FormProvider from "src/components/hook-form";

import CookiesSettings from "./cookies-settings";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onConfirm: (cookies: { [cookie: string]: boolean }) => void;
}

// ----------------------------------------------------------------------

export default function CookiesBanner({ onConfirm, ...other }: Props) {
  const methods = useForm();
  const cookieSettingsFormOpen = useBoolean();
  const { defaultCookies } = useCookies();

  return (
    <>
      <Dialog fullWidth maxWidth="xs" {...other}>
        <FormProvider methods={methods}>
          <DialogTitle sx={{ typography: "h6", pb: 3 }}>Informacja o plikach cookies</DialogTitle>

          <DialogContent sx={{ py: 0, typography: "body2" }}>
            Ta strona korzysta z plików cookies, które pomagają jej funkcjonować i śledzić sposób
            interakcji z nią, dzięki czemu możemy zapewnić lepszą i spersonalizowaną obsługę.
            Będziemy używać wszystkich plików cookies tylko wtedy, gdy wyrazisz na to zgodę,
            klikając Akceptuj wszystkie. Możesz zarządzać indywidualnymi preferencjami dotyczącymi
            plików cookie klikając w przycisk Więcej opcji. Więcej informacji znajdziesz w naszej{" "}
            <Link
              target="_blank"
              rel="noopener"
              href={paths.privacyPolicy}
              sx={{ color: "text.secondary" }}
            >
              polityce prywatności
            </Link>
            .
          </DialogContent>

          <DialogActions sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <Button variant="contained" onClick={() => onConfirm(defaultCookies)} color="success">
              Akceptuję wszystkie
            </Button>
            <Button
              variant="text"
              onClick={cookieSettingsFormOpen.onToggle}
              color="inherit"
              size="small"
            >
              Więcej opcji
            </Button>
          </DialogActions>
        </FormProvider>
      </Dialog>
      <CookiesSettings
        open={cookieSettingsFormOpen.value}
        onConfirm={(selectedCookies) => {
          onConfirm(selectedCookies);
          cookieSettingsFormOpen.onFalse();
        }}
      />
    </>
  );
}
