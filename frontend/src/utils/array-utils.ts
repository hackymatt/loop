export function haveCommonItems(arr1: string[], arr2: string[]) {
  const set1 = new Set(arr1);
  const commonItems = arr2.filter((item) => set1.has(item));
  return commonItems.length > 0;
}
