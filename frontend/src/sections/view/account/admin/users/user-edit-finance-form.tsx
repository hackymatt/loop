import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LoadingButton from "@mui/lab/LoadingButton";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogActions from "@mui/material/DialogActions";
import Dialog, { DialogProps } from "@mui/material/Dialog";

import { useFormErrorHandler } from "src/hooks/use-form-error-handler";

import { useUserFinance, useEditUserFinance } from "src/api/users/user-finance";

import FormProvider from "src/components/hook-form";

import { IUserDetailsProps } from "src/types/user";

import { schema, defaultValues } from "./finance";
import { useFinanceFields } from "./finance-fields";

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  user: IUserDetailsProps;
  onClose: VoidFunction;
}

// ----------------------------------------------------------------------

export default function UserEditFinanceForm({ user, onClose, ...other }: Props) {
  const { data: financeData } = useUserFinance(user.id);
  const { mutateAsync: editUserFinance } = useEditUserFinance(user.id);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues,
  });

  const {
    reset,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  useEffect(() => {
    if (financeData) {
      const { account, rate, commission } = financeData;
      reset({ account: account ?? "", rate: rate ?? 0, commission: commission ?? 0 });
    }
  }, [reset, financeData]);

  const handleFormError = useFormErrorHandler(methods);

  const onSubmit = handleSubmit(async (data) => {
    const { account, rate, commission } = data;
    try {
      await editUserFinance({
        account: account ?? "",
        rate: rate ?? 0,
        commission: commission ?? 0,
      });
      reset();
      onClose();
    } catch (error) {
      handleFormError(error);
    }
  });

  const { fields } = useFinanceFields();

  return (
    <Dialog
      fullScreen
      fullWidth
      maxWidth="sm"
      disablePortal
      onClose={onClose}
      {...other}
      sx={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <FormProvider methods={methods} onSubmit={onSubmit}>
        <DialogTitle sx={{ typography: "h3", pb: 3 }}>Edytuj dane finansowe</DialogTitle>

        <DialogContent sx={{ py: 0 }}>
          <Stack spacing={1}>
            {fields.account}
            {fields.rate}
            {fields.commission}
          </Stack>
        </DialogContent>

        <DialogActions
          sx={{
            position: "fixed",
            bottom: 0,
            left: 0,
            right: 0,
            zIndex: (theme) => theme.zIndex.modal + 2,
            bgcolor: "background.paper",
            boxShadow: (theme) => theme.shadows[4],
            p: 2,
          }}
        >
          <Button variant="outlined" onClick={onClose} color="inherit">
            Anuluj
          </Button>

          <LoadingButton color="inherit" type="submit" variant="contained" loading={isSubmitting}>
            Zapisz
          </LoadingButton>
        </DialogActions>
      </FormProvider>
    </Dialog>
  );
}
