import * as Yup from "yup";

export const defaultValues = {
  active: false,
  title: "",
  description: "",
  price: 0,
  duration: 15,
  github_url: "",
  technologies: [],
};

export const steps = [
  {
    label: "Uzupełnij podstawowe informacje",
    fields: ["title", "description", "price", "duration", "github_url"],
  },
  { label: "Wybierz technologie", fields: ["technologies"] },
];

export const schema = Yup.object().shape({
  active: Yup.boolean().required("Status jest wymagany"),
  title: Yup.string().required("Nazwa jest wymagana"),
  description: Yup.string().required("Opis jest wymagany"),
  price: Yup.number().required("Cena jest wymagana").min(0, "Cena musi być większa bądź równa 0"),
  duration: Yup.number()
    .required("Czas trwania jest wymagany")
    .min(30, "Czas trwania musi być większa bądź równa 30 minut")
    .test(
      "by30minutes",
      "Czas trwania musi być wielokrotnością 30 minut",
      (number) => number % 30 === 0,
    ),
  github_url: Yup.string().url().required("Link dla repozytorium jest wymagany"),
  technologies: Yup.array()
    .required("Technologie są wymagane")
    .min(1, "Wymagana przynajmniej jedna technologia"),
});
