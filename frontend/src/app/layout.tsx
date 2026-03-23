import type { Metadata } from "next";
import "./globals.css";
import Sidebar from "@/components/Sidebar";

// アプリケーションのメタデータ設定（タイトルや説明）
export const metadata: Metadata = {
  title: "AI Chatbot",
  description: "Advanced RAG Chatbot with Gemini",
};

/**
 * 全ページ共通のルートレイアウト。
 * HTML構造、グローバルなCSS、およびサイドバーを定義します。
 */
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {/* アプリ全体のコンテナ。SidebarとMainコンテンツを横並びにするレイアウトを想定。 */}
        <div className="app-container">
          <Sidebar />
          <main className="main-content">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
