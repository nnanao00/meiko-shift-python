# Meiko Shift Tool

Googleカレンダーを使用したシフト管理アプリケーション

## 機能

- 月次カレンダービューでシフトを視覚化
- ワンクリックでシフトを登録
- 登録済みシフトの削除
- モバイル対応UI

## セットアップ

### ローカル開発

1. 仮想環境を作成
```bash
python -m venv venv
source venv/bin/activate
```

2. 依存関係をインストール
```bash
pip install -r requirements.txt
```

3. Google Calendar APIの認証情報を設定
   - Google Cloud Consoleでプロジェクトを作成
   - Calendar APIを有効化
   - OAuth 2.0認証情報を作成
   - `credentials.json`をプロジェクトルートに配置

4. アプリケーションを起動
```bash
streamlit run app.py
```

初回起動時にブラウザで認証を行い、`token.json`が自動生成されます。

## Streamlit Cloudへのデプロイ

### 前提条件

- GitHubリポジトリにコードをプッシュ済み
- Streamlit Cloudアカウント

### デプロイ手順

1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. "New app"をクリック
3. GitHubリポジトリを選択
4. ブランチとメインファイル（`app.py`）を指定
5. "Advanced settings"を開き、シークレットを設定：

```
google_token = {
    "token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "scopes": ["https://www.googleapis.com/auth/calendar"]
}
```

6. "Deploy"をクリック

### 認証トークンの取得方法

1. ローカル環境でアプリを実行し、認証を完了
2. 生成された`token.json`の内容をコピー
3. Streamlit Cloudのシークレット設定に貼り付け

## シフトスロット

- Yコマ: 10:20 - 11:50
- 休憩 (45分): 11:50 - 12:35
- Zコマ: 12:35 - 14:05
- Aコマ: 14:10 - 15:40
- 休憩 (60分): 15:40 - 16:40
- Bコマ: 16:40 - 18:10
- Cコマ: 18:15 - 19:45
- Dコマ: 19:50 - 21:20
