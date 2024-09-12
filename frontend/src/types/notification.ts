export enum NotificationStatus {
  NEW = "NEW",
  READ = "READ",
}

export type INotificationProp = {
  id: string;
  title: string;
  subtitle?: string;
  description: string;
  status: NotificationStatus;
  path?: string;
  icon: string;
  modifiedAt: string;
  createdAt: string;
};
