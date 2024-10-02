import * as Yup from "yup";

export const defaultValues = {
  title: "",
  lessons: [],
};

export const steps = [
  {
    label: "Uzupełnij podstawowe informacje",
    fields: ["title"],
  },
  { label: "Wybierz lekcje", fields: ["lessons"] },
];

export const schema = Yup.object().shape({
  title: Yup.string().required("Nazwa jest wymagana"),
  lessons: Yup.array().required("Lekcje są wymagane").min(1, "Wymagana przynajmniej jedna lekcja"),
});
