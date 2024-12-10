import * as Yup from "yup";

export const defaultValues = {
  name: "",
  description: "",
};

export const schema = Yup.object().shape({
  name: Yup.string().required("Nazwa jest wymagana"),
  description: Yup.string().required("Opis jest wymagany"),
});
