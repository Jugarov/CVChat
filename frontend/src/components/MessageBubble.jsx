export default function MessageBubble({ from, text }) {
  return (
    <div className={`message ${from === "user" ? "message-user" : "message-bot"}`}>
      {text}
    </div>
  );
}
