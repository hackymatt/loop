import { IGender } from "./testimonial";

export enum MessageStatus {
  NEW = "NEW",
  READ = "READ",
}

export type IMessageUserProp = {
  id: string;
  name: string;
  gender: IGender;
  image: string;
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
