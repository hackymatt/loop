export type ICertificateProps = {
  referenceNumber: string;
  type: "Lekcja" | "Moduł" | "Kurs";
  title: string;
  studentName: string;
  duration: string;
  completedAt: string;
  isAuthorized?: boolean;
};
