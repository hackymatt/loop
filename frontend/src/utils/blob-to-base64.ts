export async function blobToBase64(blob: Blob) {
  return new Promise((resolve, _) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}

export async function urlToBlob(url: string) {
  const result = await fetch(url);
  const blob = await result.blob();
  return blobToBase64(blob);
}
