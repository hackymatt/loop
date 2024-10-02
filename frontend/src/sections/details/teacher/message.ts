import * as Yup from "yup";

export const defaultValues = {
  subject: "",
  body: "",
};

export const schema = Yup.object().shape({
  subject: Yup.string().required("Tytuł wiadomości jest wymagany"),
  body: Yup.string().required("Treść wiadomości jest wymagana"),
});
