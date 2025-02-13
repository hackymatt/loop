import * as Yup from "yup";

export const defaultValues = {
  service: [],
  other: [],
  price: 0,
  payment: [],
};

export const schema = Yup.object().shape({
  service: Yup.array().required("Usługa jest wymagana").max(1, "Wymagana jedna usługa"),
  other: Yup.array().required("Uzytkownik jest wymagany").max(1, "Wymagany jeden użytkownik"),
  price: Yup.number().required("Cena jest wymagana").min(0, "Cena musi być większa bądź równa 0"),
  payment: Yup.array().required("Płatność jest wymagana").max(1, "Wymagana jedna płatność"),
});
