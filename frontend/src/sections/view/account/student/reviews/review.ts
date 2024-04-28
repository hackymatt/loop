import * as Yup from "yup";

export const defaultValues = {
  rating: 5,
  review: "",
};

export const schema = Yup.object().shape({
  rating: Yup.number()
    .min(1, "Ocena musi być większa lub równa 1")
    .max(5, "Ocena musi być mniejsza lub równa 5")
    .required("Ocena jest wymagana"),
  review: Yup.string().nullable(),
});
