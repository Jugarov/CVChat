import { useState, useRef, useEffect } from "react";
import { askBackend } from "../api";
import MessageBubble from "./MessageBubble";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { from: "user", text: input };
    setMessages(m => [...m, userMsg]);

    // Llamada al backend
    const response = await askBackend(input);

    const botMsg = { from: "bot", text: response.answer };
    setMessages(m => [...m, botMsg]);

    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="messages-window">
        {messages.map((m, i) => (
          <MessageBubble key={i} from={m.from} text={m.text} />
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-row">
        <input
          placeholder="Escribe cualquier pregunta que desees hacer sobre mi CV"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button onClick={sendMessage}>Enviar</button>
      </div>
    </div>
  );
}
