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

export default function LessonCancelForm({ loading, onConfirm, onClose, ...other }: Props) {
  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <DialogTitle sx={{ typography: "h3", pb: 3 }}>Potwierdź odwołanie</DialogTitle>

      <DialogContent sx={{ py: 0 }}>
        <Typography>Czy na pewno chcesz odwołać tę lekcję?</Typography>

        <Alert severity="error" variant="outlined" sx={{ mt: 2 }}>
          Rezerwacje uczestników zostaną usunięte.
        </Alert>
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>

        <LoadingButton
          color="error"
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
