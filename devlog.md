# MAW (Multi-Agent Workbench) 開発ログまとめ

作成日: 2026-06-04

---

# 発端

Gemini APIの無料枠について調査した際、

- RPM: 約15
- TPM: 約1,000,000
- RPD: 約1,500

という制限を知る。

当初は

> 無料枠なのに1分100万トークン？

という驚きから始まった。

---

# 最初の発想

Gemini APIの無料枠を利用し、

単なるチャットAIの代替として、

独自のチャットフロントエンドを作れば、

無料で高性能モデルを利用できるのではないかと考えた。

ここから、

- マルチエージェント
- CoT
- 並列推論

を組み合わせる発想へ発展。

---

# Gemini無料枠の考察

## RPM

約15 RPM

つまり

```text
1分に15回リクエスト
```

まで。

しかし、

推論モデルは元々応答に時間がかかるため、

通常利用ではそこまで厳しくない可能性がある。

---

## TPM

約100万 TPM

これは非常に大きい。

例えば

```text
10エージェント
×
1万トークン
```

程度なら十分運用可能。

---

## RPD

約1500

仮に

```text
1回の質問
↓
10〜15エージェント実行
```

とすると

```text
100〜150回/日
```

程度。

ヘビーユーザーには少し厳しいが、

一般利用なら十分と判断。

---

# MAW構想誕生

議論の中で、

単なるチャットUIよりも、

マルチエージェントそのものを可視化するツールの方が面白い

という方向へ発展。

仮名称

```text
MAW
Multi-Agent Workbench
```

に決定。

---

# MAWの目的

## 主目的

AI利用者に

- マルチエージェント
- AIコーディング
- エージェント設計

を体験してもらうこと。

---

## 副目的

将来的な

- AIオーケストレーション
- 認知アーキテクチャ
- エージェントシステム

研究の実験基盤。

---

# MAWの位置付け

AIO

```text
実用ツール
```

に対し、

MAW

```text
学習・実験ツール
```

と定義。

---

# 初期設計

## 基本フロー

```text
ユーザー
↓
Moderator
↓
複数エージェント
↓
Synthesizer
↓
最終回答
```

---

## v1.0対象

### 実装

- マルチエージェント
- 議論ログ表示
- Gemini API
- エージェント編集

### 非実装

- 認証
- DB
- RAG
- Web検索
- 長期記憶
- ログ保存

---

# エージェント設計

## Moderator

質問整理

---

## Engineer

技術視点

---

## Critic

問題点・リスク

---

## Beginner

初心者視点

---

## Synthesizer

統合

---

# GitHub運用方針

Public Repository

```text
MAW
```

で公開。

---

## APIキー方針

重要方針

```text
ユーザー自身がAPIキーを用意
```

運営側では保持しない。

---

### 採用理由

- API料金不要
- サーバー不要
- スケール問題回避
- 教育用途向き

---

# プラグイン構想

当初、

プラグイン機能を検討。

しかし、

v1.0では過剰設計と判断。

代わりに

```text
agents/
workflows/
```

フォルダで管理。

---

# 実装

Codexに初回実装を依頼。

---

## 採用技術

Backend

```text
FastAPI
```

Frontend

```text
HTML
CSS
JavaScript
```

LLM

```text
Gemini API
```

---

# 初回完成

生成された構成

```text
backend/
frontend/
agents/
requirements.txt
README.md
```

---

# 安全性確認

追加改善

---

## APIキー

確認事項

- printなし
- loggingなし
- console.logなし

---

## Geminiエラー

接続失敗時

```text
Gemini APIへの接続に失敗しました
```

へ固定化。

---

## JSONエラー

明示的なエラー処理追加。

---

## 入力バリデーション

確認済み

- APIキー未入力
- モデル未入力
- 質問未入力
- エージェント未設定

---

# 実APIテスト

モデル

```text
gemini-3.1-flash-lite
```

を採用。

---

## テスト質問

```text
INIAD生向けAIアシスタントを開発する場合、
最初に実装すべき機能を検討してください。
便利さだけでなく、
運用負荷、
プライバシー、
開発初心者が参加しやすい設計も考慮してください。
```

---

# テスト結果

## 成功

フロー

```text
Moderator
↓
Engineer
↓
Critic
↓
Beginner
↓
Synthesizer
```

が正常動作。

---

## 発見された問題

### Moderator

勝手に結論を出していた。

修正：

```text
論点整理のみ
```

へ変更。

---

### Engineer

過剰設計傾向。

修正：

```text
MVP重視
```

を追加。

---

### Beginner

Engineerと役割が重複。

修正前

```text
初心者向け説明
```

修正後

```text
開発初心者・AI初心者の参加者視点
```

---

### Synthesizer

ログと最終回答が重複。

修正：

```text
議論ログから除外
```

---

# UI改善

## エージェント表示

左ボーダー追加

---

## バッジ追加

エージェント名を見やすくした。

---

## 最終回答

Synthesizer専用枠追加。

---

# デフォルトモデル変更

変更前

```text
gemini-2.0-flash
```

変更後

```text
gemini-3.1-flash-lite
```

---

# README整備

追加内容

- 起動方法
- ポート8002
- 実APIテスト済み
- 推奨モデル
- 注意事項

---

# MAW v1.0 完成時点

## 実装済み

- Gemini API入力
- モデル指定
- エージェント編集
- Moderator
- Engineer
- Critic
- Beginner
- Synthesizer
- 並列実行
- 議論ログ
- 最終回答
- Public公開可能
- README
- 実API動作確認

---

# 現在の構成

## Backend

FastAPI

### main.py

- GET /
- GET /agents
- POST /run

---

### agent_runner.py

実行フロー

```text
Moderator
↓
Discussion Agents
↓
Synthesizer
```

---

### gemini_client.py

Gemini API呼び出し

---

## Frontend

### index.html

UI

---

### app.js

状態管理

---

### style.css

デザイン

---

## Agents

default_agents.json

---

# 今後の候補

## v1.1

- ワークフロー定義JSON
- Markdown出力
- エージェント追加

---

## v2.0

- プラグイン機構
- OpenAI対応
- Claude対応
- 複数モデル混成
- 可視化強化

---

# 総括

MAWは、

```text
Gemini無料API
↓
マルチエージェント
↓
教育用途
```

という雑談から生まれた。

当初は単なるチャットUIの代替案だったが、

最終的に

```text
AIの議論を可視化する学習・実験環境
```

としてまとまった。

AIOが

```text
実用ツール
```

であるのに対し、

MAWは

```text
AIオーケストレーションや
マルチエージェント理解のための実験基盤
```

という位置付けになった。

2026-06-04時点で、

MAW v1.0は実API動作確認まで完了している。
