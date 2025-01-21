import { loadIcons, iconExists } from "@iconify/react";

const isIconExists = (iconName: string) => {
  if (iconExists(iconName)) {
    return true;
  }

  try {
    loadIcons([iconName]);
    return isIconExists(iconName);
  } catch (error) {
    return false;
  }
};

export default isIconExists;
