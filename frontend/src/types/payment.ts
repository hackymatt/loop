export enum PaymentStatus {
  PENDING = "Pending",
  SUCCESS = "Success",
  FAILURE = "Failure",
}

export type IPaymentStatus = `${PaymentStatus}`;

export type IPaymentProp = {
  sessionId: string;
  orderId: string;
  amount: number;
  status: IPaymentStatus;
};
