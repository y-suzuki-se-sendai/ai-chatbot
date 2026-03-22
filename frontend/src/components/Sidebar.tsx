"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./Sidebar.module.css";

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className={styles.header}>
        <h2>Chatbot</h2>
        <Link href="/admin" className="button button-secondary">
          Manage Files
        </Link>
      </div>
      <div className={styles.historyList}>
        <div className={styles.sectionTitle}>履歴</div>
        <div className={styles.historyItem}>
          <span>New Chat</span>
        </div>
        {/* History items will go here */}
      </div>
      <div className={styles.footer}>
        <Link href="/" className={pathname === "/" ? styles.active : ""}>
          Home
        </Link>
      </div>
    </aside>
  );
}
