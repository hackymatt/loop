import { Control, useController, useFieldArray } from "react-hook-form";

import { Stack, Button, InputAdornment } from "@mui/material";

import { RHFTextField, RHFAutocomplete } from "src/components/hook-form";

export const useInvoiceFields = (control: Control<any>) => {
  const { fields, append, remove } = useFieldArray({
    control,
    name: "items", // This refers to the `items` array in your form data
  });
  const {
    field: { value: paymentMethod },
  } = useController({ name: "payment.method", control });

  const invoiceFields: { [key: string]: JSX.Element } = {
    customer: (
      <>
        <RHFTextField key="customer-id" name="customer.id" label="ID Klienta" type="text" />
        <RHFTextField key="customer-name" name="customer.name" label="Nazwa Klienta" type="text" />
        <RHFTextField
          key="customer-streetAddress"
          name="customer.streetAddress"
          label="Adres"
          type="text"
        />
        <RHFTextField key="customer-city" name="customer.city" label="Miasto" type="text" />
        <RHFTextField
          key="customer-zipCode"
          name="customer.zipCode"
          label="Kod Pocztowy"
          type="text"
        />
        <RHFTextField key="customer-country" name="customer.country" label="Kraj" type="text" />
      </>
    ),
    items: (
      <>
        {fields.map((item, index) => (
          <Stack key={item.id} direction="column" spacing={1}>
            <RHFTextField
              key={`item-id-${index}`}
              name={`items[${index}].id`}
              label="ID"
              type="text"
            />
            <RHFTextField
              key={`item-name-${index}`}
              name={`items[${index}].name`}
              label="Nazwa"
              type="text"
            />
            <RHFTextField
              key={`item-price-${index}`}
              name={`items[${index}].price`}
              label="Cena"
              type="number"
              InputProps={{
                inputProps: { min: 0, step: ".01" },
                endAdornment: <InputAdornment position="end">zł</InputAdornment>,
              }}
            />
            <Button type="button" color="error" onClick={() => remove(index)}>
              Usuń przedmiot
            </Button>
          </Stack>
        ))}
        <Button
          type="button"
          color="success"
          onClick={() => append({ id: "", name: "", price: 0 })}
        >
          Dodaj Przedmiot
        </Button>
      </>
    ),
    payment: (
      <>
        <RHFTextField key="payment-id" name="payment.id" label="ID" type="text" disabled />
        <RHFTextField
          key="payment-amount"
          name="payment.amount"
          label="Kwota"
          type="number"
          InputProps={{
            inputProps: { min: 0, step: ".01" },
            endAdornment: <InputAdornment position="end">zł</InputAdornment>,
          }}
          disabled
        />
        <RHFAutocomplete
          key="payment-currency"
          name="payment.currency"
          label="Waluta"
          options={["PLN", "EUR", "USD"]}
          isOptionEqualToValue={(option, value) => option === value}
          disabled
        />
        <RHFAutocomplete
          key="payment-status"
          name="payment.status"
          label="Status"
          options={["Zapłacono", "Do zapłaty"]}
          isOptionEqualToValue={(option, value) => option === value}
          disabled
        />
        <RHFAutocomplete
          key="payment-method"
          name="payment.method"
          label="Metoda"
          options={["Przelewy24", "Przelew"]}
          isOptionEqualToValue={(option, value) => option === value}
          disabled
        />
        {paymentMethod === "Przelew" && (
          <RHFTextField
            key="payment-account"
            name="payment.account"
            label="Numer Konta"
            type="text"
            disabled
          />
        )}
      </>
    ),
    notes: <RHFTextField key="notes" name="notes" label="Uwagi" multiline rows={3} />,
  };

  return { fields: invoiceFields };
};
