export enum CertificateType {
  LESSON = "Lekcja",
  MODULE = "Moduł",
  COURSE = "Kurs",
}

export type ICertificateProps = {
  id: string;
  referenceNumber?: string;
  type: CertificateType;
  title: string;
  studentName?: string;
  duration?: string;
  completedAt: string;
  isAuthorized?: boolean;
};
