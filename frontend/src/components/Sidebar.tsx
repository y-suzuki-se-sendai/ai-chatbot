"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Sidebar.module.css";

/**
 * アプリケーションのサイドバーコンポーネント。
 * ナビゲーションリンクや会話履歴の表示（予定）を担当します。
 */
export default function Sidebar() {
  // 現在のパス名を取得して、アクティブなリンクのスタイリングに使用します
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      {/* ヘッダー部分：ロゴと管理画面へのリンク */}
      <div className={styles.header}>
        <h2>Chatbot</h2>
        <Link href="/admin" className="button button-secondary">
          Manage Files
        </Link>
      </div>

      {/* 会話履歴リスト表示エリア（現在は静的な表示） */}
      <div className={styles.historyList}>
        <div className={styles.sectionTitle}>履歴</div>
        <div className={styles.historyItem}>
          <span>New Chat</span>
        </div>
        {/* 今後、過去のチャット履歴がここに動的に追加される想定です */}
      </div>

      {/* フッター部分：ホームへのナビゲーション */}
      <div className={styles.footer}>
        <Link href="/" className={pathname === "/" ? styles.active : ""}>
          Home
        </Link>
      </div>
    </aside>
  );
}
