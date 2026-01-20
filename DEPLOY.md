# デプロイ手順

## GitHubリポジトリ
✅ リポジトリが作成され、コードがプッシュされました
- URL: https://github.com/nnanao00/meiko-shift-python

## Streamlit Cloudへのデプロイ

### 1. Streamlit Cloudにサインイン
1. https://share.streamlit.io/ にアクセス
2. GitHubアカウントでサインイン

### 2. 新しいアプリを作成
1. "New app"ボタンをクリック
2. 以下の情報を入力：
   - **Repository**: `nnanao00/meiko-shift-python`
   - **Branch**: `master`
   - **Main file path**: `app.py`

### 3. シークレットの設定
1. "Advanced settings"を開く
2. "Secrets"セクションに以下を追加：

```toml
google_token = {
    "token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "scopes": ["https://www.googleapis.com/auth/calendar"]
}
```

### 4. 認証トークンの取得方法
1. ローカル環境でアプリを実行：
   ```bash
   streamlit run app.py
   ```
2. ブラウザで認証を完了
3. 生成された`token.json`の内容をコピー
4. Streamlit Cloudのシークレット設定に貼り付け

### 5. デプロイ
1. "Deploy"ボタンをクリック
2. デプロイが完了するまで待機（数分かかります）
3. アプリのURLが表示されます

## 注意事項
- `token.json`と`credentials.json`は`.gitignore`に含まれているため、GitHubにはプッシュされません
- 認証トークンは定期的に更新が必要な場合があります
- 初回デプロイ後、アプリが正常に動作するか確認してください
