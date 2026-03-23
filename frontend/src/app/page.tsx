"use client";

import { useState, useRef, useEffect } from "react";
import styles from "./page.module.css";

// メッセージの型定義
interface Message {
  role: "user" | "ai";
  content: string;
  sources?: string[]; // AIが回答の根拠とした情報のソース
}

export default function Home() {
  // 会話履歴を保持するためのステート
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "こんにちは！私はあなたのAIアシスタントです。今日はどのようなご用件でしょうか？" }
  ]);
  // ユーザーの入力値を保持するためのステート
  const [input, setInput] = useState("");
  // 送信中（レスポンス待ち）かどうかを管理するステート
  const [isLoading, setIsLoading] = useState(false);
  // メッセージリストの末尾への参照。新着メッセージの自動スクロールに使用。
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 最新のメッセージまで自動でスクロールさせる関数
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // メッセージが更新された際にスクロールを実行
  useEffect(scrollToBottom, [messages]);

  // メッセージ送信時の処理
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    // ユーザーのメッセージを履歴に追加
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      // バックエンドAPIへのリクエスト送信
      const response = await fetch("http://127.0.0.1:8000/api/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to fetch");

      const data = await response.json();
      // AIの回答を履歴に追加
      setMessages(prev => [...prev, { 
        role: "ai", 
        content: data.response, 
        sources: data.sources 
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { 
        role: "ai", 
        content: " 申し訳ありません、エラーが発生しました。しばらくしてからもう一度お試しください。" 
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
        {/* メッセージ表示エリア */}
        <div className={styles.messageList}>
          {messages.map((msg, i) => (
            <div key={i} className={`${styles.message} ${styles[msg.role]}`}>
              <div className={styles.content}>{msg.content}</div>
              {/* 参照元（ソース）があれば表示 */}
              {msg.sources && msg.sources.length > 0 && (
                <div className={styles.sources}>
                  Sources: {msg.sources.join(", ")}
                </div>
              )}
            </div>
          ))}
          {/* ローディング表示 */}
          {isLoading && <div className={`${styles.message} ${styles.ai}`}>Thinking...</div>}
          <div ref={messagesEndRef} />
        </div>
        {/* 入力フォーム */}
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
