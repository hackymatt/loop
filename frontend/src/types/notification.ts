export type INotificationProp = {
  id: string;
  title: string;
  lesson?: string;
  description: string;
  status: "NEW" | "READ";
  url: string;
  icon: string;
  modifiedAt: string;
  createdAt: string;
};
