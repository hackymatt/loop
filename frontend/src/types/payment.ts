export enum PaymentStatus {
  PENDING = "Pending",
  SUCCESS = "Success",
  FAILURE = "Failure",
}

export enum PaymentCurrency {
  PLN = "PLN",
  USD = "USD",
  EUR = "EUR",
}

export enum PaymentMethod {
  Przelewy24 = "Przelewy24",
  PayPal = "PayPal",
  Przelew = "Przelew",
}

export type IPaymentStatus = `${PaymentStatus}`;
export type IPaymentCurrencyProp = `${PaymentCurrency}`;
export type IPaymentMethodProp = `${PaymentMethod}`;

export type IPaymentProp = {
  id?: string;
  sessionId: string;
  orderId?: string;
  amount: number;
  currency?: IPaymentCurrencyProp;
  method?: IPaymentMethodProp;
  status: IPaymentStatus;
  notes?: string;
  createdAt?: Date;
};
