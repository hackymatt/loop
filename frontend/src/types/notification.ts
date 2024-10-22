export enum NotificationStatus {
  NEW = "NEW",
  READ = "READ",
}

type INotificationStatus = `${NotificationStatus}`;

export type INotificationProp = {
  id: string;
  title: string;
  subtitle?: string;
  description: string;
  status: INotificationStatus;
  path?: string;
  icon: string;
  modifiedAt: string;
  createdAt: string;
};
