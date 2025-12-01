async function sendMessage() {
  const input = document.getElementById("input");
  const chat = document.getElementById("chat");

  const userText = input.value;
  chat.innerHTML += `<div><b>Tú:</b> ${userText}</div>`;
  input.value = "";

  const res = await fetch("http://localhost:8000/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: userText })
  });

  const data = await res.json();
  chat.innerHTML += `<div><b>CVChat:</b> ${data.answer}</div>`;
}
