# blog-zendesk-fetch-attachments

Zendesk のチケットから添付ファイルを取得して、特定 S3 バケットに保存するサービス

# デプロイ

## 事前設定

### 端末にインストールが必要なもの

- npm
- pipenv

### プラグインインストール

```bash
$ npm ci
```

### Python 必要パッケージインストール

```bash
$ pipenv install
```

### 手動作成が必要な AWS リソース

- S3 バケット
- Secrets Manager

設定内容は[ブログ]()を参照ください。

## デプロイ

```bash
$ sls deploy --stage {{ステージ名}} --profile {{プロファイル名}}
```

## 補足

- Zendesk トリガーや Webhook の設定は、[ブログ]()を参照ください。
