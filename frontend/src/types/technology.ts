export type ITechnologyProps = {
  id: string;
  name: string;
  createdAt: string;
};

export type ITechnologyDetailsProps = ITechnologyProps & {
  description: string;
};

export type IBestTechnologyProps = ITechnologyProps & {
  coursesCount: number;
};
