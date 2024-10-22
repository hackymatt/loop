import { UserType } from "./user";

export enum MessageStatus {
  NEW = "NEW",
  READ = "READ",
}

type IMessageStatus = `${MessageStatus}`;

export enum MessageType {
  INBOX = "INBOX",
  SENT = "SENT",
}

export type IMessageUserProp = {
  id: string;
  name: string;
  type: UserType;
};

export type IMessageProp = {
  id: string;
  subject: string;
  body: string;
  status: IMessageStatus;
  sender: IMessageUserProp;
  recipient: IMessageUserProp;
  modifiedAt: string;
  createdAt: string;
};
