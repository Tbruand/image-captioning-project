export async function uploadImage(file, token) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("lang", "fr"); // ✅ Ajout clé ici

  const response = await fetch("http://localhost:8000/upload_image", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "Erreur lors de l'envoi");
  }

  return await response.json();
}