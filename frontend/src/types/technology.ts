export type ITechnologyProps = {
  id: string;
  name: string;
  description: string;
  createdAt: string;
};

export type ITechnologyDetailsProps = ITechnologyProps & {
  description: string;
};

export type IBestTechnologyProps = ITechnologyProps & {
  coursesCount: number;
};
