export enum PaymentStatus {
  Pending = "Pending",
  Success = "Success",
  Failure = "Failure",
}

export type IPaymentStatus = keyof typeof PaymentStatus;

export type IPaymentProp = {
  sessionId: string;
  orderId: string;
  amount: number;
  status: IPaymentStatus;
};
