import chromadb
import os

def check_chroma():
    # データベースのパス（絶対パスで指定すると確実です）
    db_path = os.path.join(os.getcwd(), "data", "chroma")
    
    if not os.path.exists(db_path):
        print(f"❌ エラー: 指定されたパスにデータベースが見つかりません: {db_path}")
        return

    print(f"📂 データベースを確認中: {db_path}")
    
    try:
        # Chromaのクライアントを初期化
        client = chromadb.PersistentClient(path=db_path)
        
        # コレクション一覧を取得
        collections = client.list_collections()
        
        if not collections:
            print("📭 コレクションは空です（データが登録されていません）。")
            return

        print(f"--- 登録済みのコレクション: {len(collections)}件 ---")
        for col in collections:
            count = col.count()
            print(f"📍 名前: {col.name}")
            print(f"📊 データ件数: {count}件")
            
            if count > 0:
                # 最初の1件を取得してメタデータを確認
                sample = col.peek(1)
                print(f"🔍 メタデータのサンプル: {sample['metadatas'][0]}")
                
    except Exception as e:
        print(f"⚠️ エラーが発生しました: {e}")

if __name__ == "__main__":
    check_chroma()