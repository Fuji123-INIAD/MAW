from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent_runner import AgentConfig, run_agents
from .gemini_client import GeminiClientError


ROOT_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT_DIR / "frontend"
AGENTS_FILE = ROOT_DIR / "agents" / "default_agents.json"

app = FastAPI(title="MAW - Multi-Agent Workbench")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class AgentPayload(BaseModel):
    id: str
    display_name: str
    description: str = ""
    system_prompt: str
    enabled: bool = True


class RunRequest(BaseModel):
    question: str = ""
    api_key: str = ""
    model: str = ""
    agents: list[AgentPayload] = []


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/agents")
async def get_agents() -> list[dict]:
    try:
        with AGENTS_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="エージェント定義ファイルが見つかりません。",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail="エージェント定義ファイルのJSON形式が不正です。",
        ) from exc


@app.post("/run")
async def run(request: RunRequest) -> dict:
    if not request.api_key.strip():
        raise HTTPException(status_code=400, detail="APIキーを入力してください。")
    if not request.model.strip():
        raise HTTPException(status_code=400, detail="モデル名を入力してください。")
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="質問を入力してください。")
    if not request.agents:
        raise HTTPException(status_code=400, detail="エージェント設定を読み込めませんでした。")

    agents = [
        AgentConfig(
            id=agent.id,
            display_name=agent.display_name,
            description=agent.description,
            system_prompt=agent.system_prompt,
            enabled=agent.enabled,
        )
        for agent in request.agents
    ]

    try:
        return await run_agents(
            question=request.question.strip(),
            api_key=request.api_key.strip(),
            model=request.model.strip(),
            agents=agents,
        )
    except GeminiClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
