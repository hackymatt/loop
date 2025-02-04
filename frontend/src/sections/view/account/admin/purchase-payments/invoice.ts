import * as Yup from "yup";

import { IInvoicePaymentMethod, IInvoicePaymentStatus } from "src/types/invoice";

export const defaultValues = {
  customer: {
    id: 0,
    name: "",
    streetAddress: "",
    city: "",
    zipCode: "",
    country: "",
  },
  items: [
    {
      id: 0,
      name: "",
      price: 0,
    },
  ],
  payment: {
    id: 0,
    amount: 0,
    status: "Do zapłaty" as IInvoicePaymentStatus,
    method: "Przelew" as IInvoicePaymentMethod,
    account: "",
  },
};

export const steps = [
  {
    label: "Uzupełnij dane klienta",
    fields: ["customer"],
  },
  { label: "Uzupełnij dane przedmiotów", fields: ["items"] },
  { label: "Uzupełnij dane płatności", fields: ["payment"] },
];

export const schema = Yup.object().shape({
  customer: Yup.object().shape({
    id: Yup.number().required("ID klienta jest wymagane"),
    name: Yup.string().required("Nazwa klienta jest wymagana"),
    streetAddress: Yup.string().required("Adres jest wymagany"),
    city: Yup.string().required("Miasto jest wymagane"),
    zipCode: Yup.string().required("Kod pocztowy jest wymagany"),
    country: Yup.string().required("Kraj jest wymagany"),
  }),
  items: Yup.array()
    .of(
      Yup.object().shape({
        id: Yup.number().required("ID przedmiotu jest wymagane"),
        name: Yup.string().required("Nazwa przedmiotu jest wymagana"),
        price: Yup.number().positive().required("Cena jest wymagana"),
      }),
    )
    .min(1, "Musi być co najmniej jeden przedmiot")
    .required("Lista przedmiotów jest wymagana"),
  payment: Yup.object().shape({
    id: Yup.number().required("ID płatności jest wymagane"),
    amount: Yup.number().positive().required("Kwota jest wymagana"),
    status: Yup.string().oneOf(["Zapłacono", "Do zapłaty"]).required("Status jest wymagany"),
    method: Yup.string()
      .oneOf(["Przelewy24", "Przelew"])
      .required("Metoda płatności jest wymagana"),
    account: Yup.string().required("Numer konta jest wymagany"),
  }),
});
