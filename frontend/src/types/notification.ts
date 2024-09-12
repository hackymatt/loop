export type INotificationProp = {
  id: string;
  title: string;
  subtitle?: string;
  description: string;
  status: "NEW" | "READ";
  path?: string;
  icon: string;
  modifiedAt: string;
  createdAt: string;
};
