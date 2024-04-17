import * as Yup from "yup";

export const defaultValues = {
  code: "",
  discount: 0,
  is_percentage: false,
  users: [],
  all_users: true,
  max_uses: 1,
  is_infinite: true,
  uses_per_user: 1,
  expiration_date: new Date(),
  active: false,
  min_total: 100,
};

export const steps = [
  {
    label: "Uzupełnij dane kuponu",
    fields: ["code", "discount_with_type"],
  },
  { label: "Zdefiniuj dozwolonych użytkowników", fields: ["all_users", "users"] },
  { label: "Zdefiniuj ilość wykorzystań", fields: ["is_infinite", "max_uses", "uses_per_user"] },
  { label: "Zdefiniuj date ważności", fields: ["expiration_date"] },
  { label: "Zdefiniuj minimalną wartość zamówienia", fields: ["min_total"] },
];

export const schema = Yup.object().shape({
  active: Yup.boolean().required("Status jest wymagany"),
  code: Yup.string()
    .required("Kod jest wymagany")
    .min(6, "Długość kuponu musi być większa bądź równa 6")
    .max(36, "Długość kuponu musi być mniejsza bądź równa 36"),
  discount: Yup.number()
    .required("Zniżka jest wymagana")
    .min(0, "Zniżka musi być większa bądź równa 0"),
  is_percentage: Yup.boolean().required("Typ zniżki jest wymagany"),
  all_users: Yup.boolean().required("To pole jest wymagane"),
  users: Yup.array().required("To pole jest wymagane"),
  is_infinite: Yup.boolean().required("To pole jest wymagane"),
  max_uses: Yup.number()
    .required("Maksymalna ilość wykorzystań jest wymagana")
    .min(0, "Maksymalna ilość wykorzystań musi być większa bądź równa 0"),
  uses_per_user: Yup.number()
    .required("Maksymalna ilość wykorzystań przez użytkownika jest wymagana")
    .min(1, "Maksymalna ilość wykorzystań przez użytkownika musi być większa bądź równa 1"),

  expiration_date: Yup.date().required("Data ważności jest wymagana"),
  min_total: Yup.number()
    .required("Minimalna wartość zamówienia jest wymagana")
    .min(0, "Minimalna wartość zamówienia musi być większa bądź równa 0"),
});
