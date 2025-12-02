const API_URL = import.meta.env.VITE_API_URL;

export async function askBackend(query) {
  const res = await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query })
  });

  if (!res.ok) {
    return { answer: "Error al consultar el backend." };
  }

  return await res.json();
}
