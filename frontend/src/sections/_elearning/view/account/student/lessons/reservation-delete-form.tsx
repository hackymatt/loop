import Button from "@mui/material/Button";
import { Typography } from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useDeleteReservation } from "src/api/reservations/reservation";

import { useToastContext } from "src/components/toast";

import { IPurchaseItemProp } from "src/types/purchase";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  purchase: IPurchaseItemProp;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function TeachingDeleteForm({ purchase, onClose, ...other }: Props) {
  const { enqueueSnackbar } = useToastContext();

  const { mutateAsync: deleteReservation, isLoading: isSubmitting } = useDeleteReservation(
    purchase.id,
  );

  const onSubmit = async () => {
    try {
      await deleteReservation({});
      onClose();
      enqueueSnackbar("Rezerwacja została usunięta", { variant: "success" });
    } catch (error) {
      // enqueueSnackbar("Lekcja została oznaczona jako nieprowadzona", { variant: "success" });
    }
  };

  return (
    <Dialog fullWidth maxWidth="sm" onClose={onClose} {...other}>
      <DialogTitle sx={{ typography: "h3", pb: 3 }}>Przestań prowadzić lekcję</DialogTitle>

      <DialogContent sx={{ py: 0 }}>
        <Typography>{`Czy na pewno chcesz usunąć rezerwację dla lekcji ${purchase.lessonTitle}?`}</Typography>
      </DialogContent>

      <DialogActions>
        <Button variant="outlined" onClick={onClose} color="inherit">
          Anuluj
        </Button>

        <LoadingButton
          color="error"
          type="submit"
          variant="contained"
          loading={isSubmitting}
          onClick={onSubmit}
        >
          Usuń
        </LoadingButton>
      </DialogActions>
    </Dialog>
  );
}
