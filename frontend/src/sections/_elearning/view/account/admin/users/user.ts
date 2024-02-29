import * as Yup from "yup";

export const defaultValues = {
  first_name: "",
  last_name: "",
  email: "",
  gender: "Mężczyzna",
  user_type: "Admin",
  image: "",
  user_title: "",
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
  phone_number: Yup.string().nullable(),
  dob: Yup.mixed<any>().nullable(),
  gender: Yup.string().required("Płeć jest wymagana"),
  street_address: Yup.string().nullable(),
  zip_code: Yup.string().nullable(),
  city: Yup.string().nullable(),
  country: Yup.string().required("Państwo jest wymagane"),
  image: Yup.string().nullable(),
});
