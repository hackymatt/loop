import packageInfo from "package.json";

// ----------------------------------------------------------------------

export const createMetadata = (title: string) => ({
  title: `${title} • ${packageInfo.name}`,
});
