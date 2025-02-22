import * as Yup from "yup";

export const defaultValues = {
  rate: 0,
  commission: 0,
  account: "",
};

export const schema = Yup.object().shape({
  account: Yup.string().notRequired(),
  rate: Yup.number().nullable().min(0, "Stawka musi wynosić min 0 zł"),
  commission: Yup.number()
    .nullable()
    .min(0, "Prowizja musi wynosić min 0 %")
    .max(100, "Prowizja musi wynosić max 100 %"),
});
