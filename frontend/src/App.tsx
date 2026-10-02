import { useState } from "react";
import "./index.css";

type Message = {
  role: "user" | "assistant";
  content: string;
};

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = async () => {
    if (!message.trim() || loading) return;

    const currentMessage = message;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: currentMessage },
    ]);

    setMessage("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: currentMessage,
          history: messages,
        }),
      });

      if (!res.ok || !res.body) {
        throw new Error("Failed to get response.");
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();

      let assistantResponse = "";

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "" },
      ]);

      while (true) {
        const { done, value } = await reader.read();

        if (done) break;

        assistantResponse += decoder.decode(value, {
          stream: true,
        });

        setMessages((prev) => {
          const updated = [...prev];

          updated[updated.length - 1] = {
            role: "assistant",
            content: assistantResponse,
          };

          return updated;
        });
      }
    } catch {
      setError("Unable to connect to the AI model.");
    } finally {
      setLoading(false);
    }
  };

  const runAction = async (
    endpoint: string,
    body: object
  ) => {
    if (!message.trim() || loading) return;

    const currentMessage = message;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: currentMessage },
    ]);

    setMessage("");
    setLoading(true);
    setError("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000${endpoint}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );

      if (!res.ok) {
        throw new Error("Request failed.");
      }

      const data = await res.json();

      const result =
        typeof data === "object" && !data.response
          ? JSON.stringify(data, null, 2)
          : data.response;

      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: result },
      ]);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const summarize = () =>
    runAction("/summarize", { text: message });

  const rewrite = () =>
    runAction("/rewrite", {
      text: message,
      style: "professional",
    });

  const extract = () =>
    runAction("/extract", { text: message });

  const generate = () =>
    runAction("/generate", {
      instruction: message,
    });

  return (
    <div className="app">
      <header>
        <h1>ContextFlow</h1>
        <p>Turn your text into useful AI-powered outputs.</p>
      </header>

      <main className="chat">
        {messages.length === 0 && (
          <div className="welcome">
            <h2>What can I help with?</h2>
            <p>
              Chat, summarize, rewrite, extract information,
              or generate content.
            </p>
          </div>
        )}

        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role}`}
          >
            <div className="message-label">
              {msg.role === "user" ? "You" : "ContextFlow"}
            </div>

            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div className="loading">
            ContextFlow is thinking...
          </div>
        )}

        {error && <div className="error">{error}</div>}
      </main>

      <section className="composer">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Enter text or ask ContextFlow something..."
          disabled={loading}
        />

        <div className="actions">
          <button onClick={sendMessage} disabled={loading}>
            Chat
          </button>

          <button onClick={summarize} disabled={loading}>
            Summarize
          </button>

          <button onClick={rewrite} disabled={loading}>
            Rewrite
          </button>

          <button onClick={extract} disabled={loading}>
            Extract
          </button>

          <button onClick={generate} disabled={loading}>
            Generate
          </button>
        </div>
      </section>
    </div>
  );
}

export default App;