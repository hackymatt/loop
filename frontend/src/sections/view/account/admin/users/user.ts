import * as Yup from "yup";

import { Gender } from "src/consts/gender";

export const DEFAULT_COUNTRY = "Polska";

export const defaultValues = {
  firstName: "",
  lastName: "",
  email: "",
  phoneNumber: "",
  dob: null,
  gender: Gender.Other,
  streetAddress: "",
  zipCode: "",
  city: "",
  country: DEFAULT_COUNTRY,
  image: "",
};

export const schema = Yup.object().shape({
  firstName: Yup.string().required("Imię jest wymagane"),
  lastName: Yup.string().required("Nazwisko jest wymagane"),
  email: Yup.string().required("Adres email jest wymagany"),
  phoneNumber: Yup.string().nullable(),
  dob: Yup.mixed<any>().nullable(),
  gender: Yup.string().required("Płeć jest wymagana"),
  streetAddress: Yup.string().nullable(),
  zipCode: Yup.string().nullable(),
  city: Yup.string().nullable(),
  country: Yup.string().required("Państwo jest wymagane"),
  image: Yup.string().nullable(),
});
