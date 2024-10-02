import { usePathname } from "next/navigation";

import { paths } from "../paths";

// ----------------------------------------------------------------------

type ReturnType = boolean;

export function useActiveLink(path: string, deep = true): ReturnType {
  const pathname = usePathname();

  if (!pathname.includes(paths.account.root)) {
    return false;
  }

  const checkPath = path.startsWith("#");

  const currentPath = path === "/" ? "/" : `${path}/`;

  const normalActive = !checkPath && pathname === currentPath;

  const deepActive =
    !checkPath && (currentPath.includes(pathname) || pathname.includes(currentPath));

  return deep ? deepActive : normalActive;
}
