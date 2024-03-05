import * as Yup from "yup";

export const defaultValues = {
  first_name: "",
  last_name: "",
  email: "",
  gender: "Mężczyzna",
  user_type: "Admin",
  image: "",
  user_title: "",
  rate: 0,
  commission: 0,
  account: "",
  phone_number: "",
  dob: "",
  street_address: "",
  zip_code: "",
  city: "",
  country: "",
};

export const schema = Yup.object().shape({
  first_name: Yup.string().required("Imię jest wymagane"),
  last_name: Yup.string().required("Nazwisko jest wymagane"),
  email: Yup.string().required("Adres email jest wymagany"),
  gender: Yup.string().required("Płeć jest wymagana"),
  user_type: Yup.string().required("Typ jest wymagany"),
  user_title: Yup.string().nullable(),
  rate: Yup.number().nullable(),
  commission: Yup.number().nullable(),
  account: Yup.string().nullable(),
  image: Yup.string().nullable(),
  phone_number: Yup.string().nullable(),
  dob: Yup.mixed<any>().nullable(),
  street_address: Yup.string().nullable(),
  zip_code: Yup.string().nullable(),
  city: Yup.string().nullable(),
  country: Yup.string().nullable(),
});
