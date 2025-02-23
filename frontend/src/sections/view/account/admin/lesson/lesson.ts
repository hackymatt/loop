import * as Yup from "yup";

import { LESSON_DURATION_MULTIPLIER } from "src/config-global";

export const defaultValues = {
  active: false,
  title: "",
  description: "",
  price: 0,
  duration: 30,
  githubUrl: "",
  technologies: [],
};

export const steps = [
  {
    label: "Uzupełnij podstawowe informacje",
    fields: ["title", "description", "price", "duration", "githubUrl"],
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
    .min(
      LESSON_DURATION_MULTIPLIER,
      `Czas trwania musi być większy bądź równy ${LESSON_DURATION_MULTIPLIER} minut`,
    )
    .test(
      `by${LESSON_DURATION_MULTIPLIER}minutes`,
      `Czas trwania musi być wielokrotnością ${LESSON_DURATION_MULTIPLIER} minut`,
      (number) => number % LESSON_DURATION_MULTIPLIER === 0,
    ),
  githubUrl: Yup.string().required("Link do repozytorium jest wymagany"),
  technologies: Yup.array().nullable(),
});
