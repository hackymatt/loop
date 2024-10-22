export enum CertificateType {
  LESSON = "Lekcja",
  MODULE = "Moduł",
  COURSE = "Kurs",
}

type ICertificateType = `${CertificateType}`;

export type ICertificateProps = {
  id: string;
  referenceNumber?: string;
  type: ICertificateType;
  title: string;
  studentName?: string;
  duration?: string;
  completedAt: string;
  isAuthorized?: boolean;
};
