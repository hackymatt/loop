import { RHFTextField } from "src/components/hook-form";

export const useMessageFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    subject: <RHFTextField name="subject" label="Tytuł" />,
    body: <RHFTextField multiline rows={3} name="body" label="Treść" />,
  };
  return { fields };
};
