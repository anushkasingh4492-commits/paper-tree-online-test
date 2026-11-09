export async function fetchStudentData<T>(url: string): Promise<T> {
  const response = await fetch(url, {
    cache: "no-store",
    credentials: "include",
  });
  const payload = (await response.json()) as T & {
    success?: boolean;
    error?: string;
  };

  if (!response.ok || payload.success === false) {
    throw new Error(payload.error || `Could not load ${url}.`);
  }

  return payload;
}
