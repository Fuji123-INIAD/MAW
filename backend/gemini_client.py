from __future__ import annotations

import httpx


class GeminiClientError(RuntimeError):
    pass


async def generate_content(api_key: str, model: str, prompt: str) -> str:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                params={"key": api_key},
                json=payload,
            )
    except httpx.HTTPError as exc:
        raise GeminiClientError(
            "Gemini APIへの接続に失敗しました。ネットワークまたはモデル名を確認してください。"
        ) from exc

    if response.status_code >= 400:
        detail = _extract_error_message(response)
        raise GeminiClientError(f"Gemini APIエラー: {detail}")

    try:
        data = response.json()
    except ValueError as exc:
        raise GeminiClientError("Gemini APIからJSON形式の応答を取得できませんでした。") from exc
    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as exc:
        raise GeminiClientError("Gemini APIから回答本文を取得できませんでした。") from exc

    text = "\n".join(part.get("text", "") for part in parts).strip()
    if not text:
        raise GeminiClientError("Gemini APIの回答が空でした。")
    return text


def _extract_error_message(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code}"

    error = data.get("error", {})
    message = error.get("message")
    if message:
        return message
    return f"HTTP {response.status_code}"
