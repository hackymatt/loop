import * as Yup from "yup";

export const defaultValues = {
  active: false,
  title: "",
  description: "",
  price: 0,
};

export const schema = Yup.object().shape({
  active: Yup.boolean().required("Status jest wymagany"),
  title: Yup.string().required("Nazwa jest wymagana"),
  description: Yup.string().required("Opis jest wymagany"),
  price: Yup.number().required("Cena jest wymagana").min(0, "Cena musi być większa bądź równa 0"),
});
