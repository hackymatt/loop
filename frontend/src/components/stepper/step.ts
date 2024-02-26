import { FieldErrors } from "react-hook-form";

import { haveCommonItems } from "src/utils/array-utils";

export const isStepFailed = (stepFields: string[], fieldErrors: FieldErrors) => {
  const errorFields = Object.keys(fieldErrors);
  return haveCommonItems(stepFields, errorFields);
};
