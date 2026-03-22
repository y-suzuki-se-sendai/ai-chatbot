"use client";

import { useState } from "react";
import styles from "./admin.module.css";
import Link from "next/link";

interface UploadResult {
  filename: string;
  success: boolean;
}

export default function AdminPage() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [results, setResults] = useState<UploadResult[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(e.target.files);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length === 0) return;

    setIsUploading(true);
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files", files[i]);
    }

    try {
      const response = await fetch("http://localhost:8000/api/ingest/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Upload failed");

      const data = await response.json();
      setResults(data.results);
      setFiles(null);
      // Reset input
      const input = document.getElementById("file-upload") as HTMLInputElement;
      if (input) input.value = "";
      
    } catch (error) {
      console.error(error);
      alert("Error uploading files");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <>
      <header className="header">
        <h1>Admin - Manage Training Files</h1>
        <Link href="/" className="button button-secondary">Back to Chat</Link>
      </header>
      <div className={styles.adminContainer}>
        <section className={styles.uploadSection}>
          <h2>ファイルアップロード</h2>
          <p className={styles.description}>PDF,CSV,Exsel(.xlsx),Word(.docx),テキストファイル(.txt)をアップロードできます。</p>
          <form onSubmit={handleUpload} className={styles.uploadForm}>
            <input
              id="file-upload"
              type="file"
              multiple
              accept=".pdf,.txt,.docx"
              onChange={handleFileChange}
              className={styles.fileInput}
            />
            <button
              type="submit"
              className="button button-primary"
              disabled={!files || isUploading}
            >
              {isUploading ? "アップロード中..." : "アップロード"}
            </button>
          </form>
        </section>

        {results.length > 0 && (
          <section className={styles.resultsSection}>
            <h2>アップロードが完了しました！</h2>
            <ul className={styles.resultList}>
              {results.map((res, i) => (
                <li key={i} className={res.success ? styles.success : styles.error}>
                  <span>{res.filename}</span>
                  <span className={styles.statusLabel}>{res.success ? "Processed" : "Failed"}</span>
                </li>
              ))}
            </ul>
          </section>
        )}
      </div>
    </>
  );
}
