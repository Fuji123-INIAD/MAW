# MAW (Multi-Agent Workbench)

## v1.0 起動方法

### 必要なもの

- Python 3.10 以上
- Google Gemini API キー

API キーは画面上で入力します。サーバー側には保存せず、`.env` も使いません。

### セットアップ

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 起動

```bash
uvicorn backend.main:app --reload
```

ブラウザで以下を開きます。

```text
http://127.0.0.1:8000
```

8000番ポートが既に使われている場合は、別ポートを指定してください。

```bash
uvicorn backend.main:app --reload --port 8002
```

```text
http://127.0.0.1:8002
```

## 使い方

1. Gemini API キーを入力します。
2. モデル名を入力または選択します。推奨モデルは `gemini-3.1-flash-lite` です。
3. 質問を入力します。
4. 必要に応じてエージェントのチェックや役割プロンプトを編集します。
5. 「実行」を押すと、Moderator、Engineer/Critic/Beginner、Synthesizer の順に結果が表示されます。

## 手動テスト

1. API キーを空にして実行し、「APIキーを入力してください。」が表示されることを確認します。
2. モデル名を空にして実行し、「モデル名を入力してください。」が表示されることを確認します。
3. 有効な Gemini API キーとモデル名で質問を送信し、議論ログと最終回答が表示されることを確認します。
4. Engineer / Critic / Beginner の一部をオフにして、API 呼び出し回数が減った構成でも実行できることを確認します。

### 実APIテスト

- 実APIテスト済みです。
- `gemini-3.1-flash-lite` で動作確認しています。

## 注意事項

- DB、認証、ログ保存、Web検索、RAG は実装していません。
- 1回の実行で、Moderator 1回、選択した回答用エージェント数分、Synthesizer 1回の Gemini API 呼び出しを行います。
- エージェント定義は `agents/default_agents.json` にあります。追加や文言調整はこのファイルを編集してください。

---

MAWは、複数のAIエージェントによる議論・協調・批判的検討を可視化するための実験環境です。

## 目的

- AIコーディングの学習
- マルチエージェントの理解
- エージェント設計の実験
- 認知アーキテクチャ研究の基盤構築

## 特徴

- エージェントごとの発言を可視化
- 議論プロセスを表示
- ユーザーによる役割設定
- Gemini API対応（APIキーは各自で用意）
