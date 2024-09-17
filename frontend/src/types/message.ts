import { UserType } from "./user";

export enum MessageStatus {
  NEW = "NEW",
  READ = "READ",
}

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
  status: MessageStatus;
  sender: IMessageUserProp;
  recipient: IMessageUserProp;
  modifiedAt: string;
  createdAt: string;
};
