import * as Yup from "yup";

export const defaultValues = {
  active: false,
  title: "",
  description: "",
  content: "",
  category: [],
  tags: [],
  authors: [],
  image: "",
  publication_date: new Date(),
};

export const steps = [
  {
    label: "Uzupełnij podstawowe informacje",
    fields: ["title", "description", "publication_date"],
  },
  { label: "Uzupełnij treść", fields: ["content"] },
  { label: "Wybierz kategorię", fields: ["category"] },
  { label: "Wybierz tagi", fields: ["tags"] },
  { label: "Wybierz autorów", fields: ["authors"] },
  { label: "Wybierz zdjęcie", fields: ["image"] },
];

export const schema = Yup.object().shape({
  active: Yup.boolean().required("Status jest wymagany"),
  title: Yup.string().required("Nazwa jest wymagana"),
  publication_date: Yup.date().required("Data publikacji jest wymagana"),
  description: Yup.string().required("Opis jest wymagany"),
  content: Yup.string().required("Treść jest wymagana"),
  category: Yup.array().required("Kategoria jest wymagana").max(1, "Wymagana jedna kategoria"),
  tags: Yup.array().required("Tagi są wymagane").min(1, "Wymagany przynajmniej jeden tag"),
  authors: Yup.array().required("Autorzy są wymagani").min(1, "Wymagany przynajmniej jeden autor"),
  image: Yup.string().required("Zdjęcie jest wymagane"),
});
