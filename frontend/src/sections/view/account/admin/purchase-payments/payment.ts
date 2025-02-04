import * as Yup from "yup";

import { PaymentStatus } from "src/types/payment";

export const defaultValues = {
  amount: 0,
  status: PaymentStatus.PENDING,
};

export const schema = Yup.object().shape({
  amount: Yup.number().required("Kwota jest wymagana"),
  status: Yup.string().required("Status jest wymagany"),
});
