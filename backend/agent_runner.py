from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Iterable

from .gemini_client import generate_content


@dataclass(frozen=True)
class AgentConfig:
    id: str
    display_name: str
    description: str
    system_prompt: str
    enabled: bool = True


async def run_agents(
    question: str,
    api_key: str,
    model: str,
    agents: Iterable[AgentConfig],
) -> dict:
    agent_map = {agent.id: agent for agent in agents if agent.enabled}
    moderator = agent_map.get("moderator")
    synthesizer = agent_map.get("synthesizer")

    if moderator is None:
        raise ValueError("Moderatorエージェントが選択されていません。")
    if synthesizer is None:
        raise ValueError("Synthesizerエージェントが選択されていません。")

    discussion_agents = [
        agent
        for agent in agent_map.values()
        if agent.id not in {"moderator", "synthesizer"}
    ]
    if not discussion_agents:
        raise ValueError("回答用エージェントを1つ以上選択してください。")

    logs: list[dict[str, str]] = []

    moderator_prompt = _build_prompt(
        moderator,
        question,
        extra_context="まず質問を整理し、主要な論点を箇条書きで分解してください。",
    )
    moderator_answer = await generate_content(api_key, model, moderator_prompt)
    logs.append({"agent": moderator.display_name, "content": moderator_answer})

    async def run_discussion_agent(agent: AgentConfig) -> dict[str, str]:
        prompt = _build_prompt(
            agent,
            question,
            extra_context=(
                "Moderatorによる論点整理を踏まえて回答してください。\n\n"
                f"Moderatorの整理:\n{moderator_answer}"
            ),
        )
        answer = await generate_content(api_key, model, prompt)
        return {"agent": agent.display_name, "content": answer}

    discussion_logs = await asyncio.gather(
        *(run_discussion_agent(agent) for agent in discussion_agents)
    )
    logs.extend(discussion_logs)

    transcript = "\n\n".join(
        f"[{entry['agent']}]\n{entry['content']}" for entry in logs
    )
    synthesizer_prompt = _build_prompt(
        synthesizer,
        question,
        extra_context=(
            "以下の議論ログを統合し、重複を整理して最終回答を作成してください。"
            "必要なら弱点や注意点も含めてください。\n\n"
            f"議論ログ:\n{transcript}"
        ),
    )
    final_answer = await generate_content(api_key, model, synthesizer_prompt)
    logs.append({"agent": synthesizer.display_name, "content": final_answer})

    return {"logs": logs, "final_answer": final_answer}


def _build_prompt(agent: AgentConfig, question: str, extra_context: str) -> str:
    return (
        f"{agent.system_prompt}\n\n"
        f"ユーザーの質問:\n{question}\n\n"
        f"追加コンテキスト:\n{extra_context}\n\n"
        "日本語で、簡潔かつ具体的に回答してください。"
    )
