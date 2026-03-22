"use client";

import { useState, useRef, useEffect } from "react";
import styles from "./page.module.css";

interface Message {
  role: "user" | "ai";
  content: string;
  sources?: string[];
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "こんにちは！私はあなたのAIアシスタントです。今日はどのようなご用件でしょうか？" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to fetch");

      const data = await response.json();
      setMessages(prev => [...prev, { 
        role: "ai", 
        content: data.response, 
        sources: data.sources 
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: "ai", 
        content: "Sorry, I encountered an error. Please try again later." 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <header className="header">
        <h1>Chat</h1>
      </header>
      <div className={styles.chatContainer}>
        <div className={styles.messageList}>
          {messages.map((msg, i) => (
            <div key={i} className={`${styles.message} ${styles[msg.role]}`}>
              <div className={styles.content}>{msg.content}</div>
              {msg.sources && msg.sources.length > 0 && (
                <div className={styles.sources}>
                  Sources: {msg.sources.join(", ")}
                </div>
              )}
            </div>
          ))}
          {isLoading && <div className={`${styles.message} ${styles.ai}`}>Thinking...</div>}
          <div ref={messagesEndRef} />
        </div>
        <form className={styles.inputArea} onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="ここにメッセージ内容を入力してください..."
            disabled={isLoading}
          />
          <button type="submit" className="button button-primary" disabled={isLoading}>
            送信
          </button>
        </form>
      </div>
    </>
  );
}
