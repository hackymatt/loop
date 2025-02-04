type ICustomer = {
  id: number;
  name: string;
  streetAddress: string;
  city: string;
  zipCode: string;
  country: string;
};

type IItem = {
  id: number;
  name: string;
  price: number;
};

export type IInvoicePaymentStatus = "Zapłacono" | "Do zapłaty";
export type IInvoicePaymentMethod = "Przelewy24" | "Przelew";

type IPayment = {
  id: number;
  amount: number;
  status: IInvoicePaymentStatus;
  method: IInvoicePaymentMethod;
  account: string;
};

export type IInvoiceProp = {
  customer: ICustomer;
  items: IItem[];
  payment: IPayment;
  notes: string;
};
