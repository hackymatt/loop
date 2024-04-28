import { RHFTextField } from "src/components/hook-form";

export const useSkillFields = () => {
  const fields: { [key: string]: JSX.Element } = {
    name: <RHFTextField name="name" label="Nazwa" />,
  };
  return { fields };
};
