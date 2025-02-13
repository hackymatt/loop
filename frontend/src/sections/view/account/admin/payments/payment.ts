import * as Yup from "yup";

import {
  PaymentMethod,
  PaymentStatus,
  PaymentCurrency,
  IPaymentMethodProp,
  IPaymentCurrencyProp,
} from "src/types/payment";

export const defaultValues = {
  amount: 0,
  currency: PaymentCurrency.PLN as IPaymentCurrencyProp,
  method: PaymentMethod.Przelew as IPaymentMethodProp,
  status: PaymentStatus.PENDING,
  notes: "",
};

export const schema = Yup.object().shape({
  amount: Yup.number().required("Kwota jest wymagana"),
  currency: Yup.string().required("Waluta jest wymagana"),
  method: Yup.string().required("Metoda jest wymagana"),
  status: Yup.string().required("Status jest wymagany"),
  notes: Yup.string(),
});
