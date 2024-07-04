import Button from "@mui/material/Button";
import { Alert, Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  loading: boolean;
  onConfirm: VoidFunction;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function ReservationConfirmForm({ loading, onConfirm, onClose, ...other }: Props) {
  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <DialogTitle sx={{ typography: "h3", pb: 3 }}>Potwierdź rezerwację</DialogTitle>

      <DialogContent sx={{ py: 0 }}>
        <Typography>
          Czy na pewno chcesz zarezerwować ten termin? Potwierdzenie realizacji wraz z linkiem do
          spotkania otrzymasz 24 godziny przed planowanym rozpoczęciem zajęć.
        </Typography>
        <Alert variant="outlined" severity="warning" sx={{ mt: 2 }}>
          Odwołanie rezerwacji jest możliwe do 24 godzin przed rozpoczęciem zajęć.
        </Alert>
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>

        <LoadingButton
          color="success"
          type="submit"
          variant="contained"
          onClick={onConfirm}
          loading={loading}
        >
          Potwierdź
        </LoadingButton>
      </DialogActions>
    </Dialog>
  );
}
