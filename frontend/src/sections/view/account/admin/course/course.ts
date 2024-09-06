import * as Yup from "yup";

export const defaultValues = {
  active: false,
  title: "",
  description: "",
  level: "Podstawowy",
  modules: [],
  skills: [],
  topics: [],
  image: "",
  video: "",
};

export const steps = [
  {
    label: "Uzupełnij podstawowe informacje",
    fields: ["title", "description", "level", "duration", "github_url"],
  },
  { label: "Wybierz umiejętności", fields: ["skills"] },
  { label: "Wybierz tematy", fields: ["topics"] },
  { label: "Wybierz moduły", fields: ["modules"] },
  { label: "Wybierz zdjęcie", fields: ["image"] },
  { label: "Wybierz film", fields: ["video"] },
];

export const schema = Yup.object().shape({
  active: Yup.boolean().required("Status jest wymagany"),
  title: Yup.string().required("Nazwa jest wymagana"),
  description: Yup.string().required("Opis jest wymagany"),
  level: Yup.string().required("Poziom jest wymagany"),
  image: Yup.string().required("Zdjęcie jest wymagane"),
  video: Yup.string(),
  modules: Yup.array().required("Moduły są wymagane").min(1, "Wymagany przynajmniej jeden moduł"),
  skills: Yup.array()
    .required("Umiejętności są wymagane")
    .min(1, "Wymagana przynajmniej jedna umiejętność"),
  topics: Yup.array().required("Tematy są wymagane").min(1, "Wymagana przynajmniej jeden temat"),
});
