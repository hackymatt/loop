import * as Yup from "yup";

import { PaymentStatus } from "src/types/payment";
import { IPaymentCurrencyProp } from "src/types/purchase";

export const defaultValues = {
  amount: 0,
  currency: "PLN" as IPaymentCurrencyProp,
  status: PaymentStatus.PENDING,
};

export const schema = Yup.object().shape({
  amount: Yup.number().required("Kwota jest wymagana"),
  currency: Yup.string()
    .oneOf(["PLN", "USD", "EUR"], "Nieobsługiwana waluta")
    .required("Waluta jest wymagana"),
  status: Yup.string().required("Status jest wymagany"),
});
