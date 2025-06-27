export async function sendFeedback(id_image, feedback, token) {
  const body = JSON.stringify({ id_image, feedback });

  const response = await fetch("http://localhost:8000/send_feedback", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(err || "Erreur lors de l'envoi du feedback");
  }

  return await response.json();
}