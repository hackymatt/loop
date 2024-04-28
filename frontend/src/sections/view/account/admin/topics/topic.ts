import * as Yup from "yup";

export const defaultValues = {
  name: "",
};

export const schema = Yup.object().shape({
  name: Yup.string().required("Nazwa jest wymagana"),
});
