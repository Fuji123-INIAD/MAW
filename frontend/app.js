const state = {
  defaultAgents: [],
  agents: [],
};

const elements = {
  form: document.querySelector("#run-form"),
  apiKey: document.querySelector("#api-key"),
  model: document.querySelector("#model"),
  question: document.querySelector("#question"),
  agentList: document.querySelector("#agent-list"),
  runButton: document.querySelector("#run-button"),
  errorMessage: document.querySelector("#error-message"),
  logList: document.querySelector("#log-list"),
  finalAnswer: document.querySelector("#final-answer"),
  statusText: document.querySelector("#status-text"),
  clearLog: document.querySelector("#clear-log"),
  resetAgents: document.querySelector("#reset-agents"),
};

async function loadAgents() {
  try {
    const response = await fetch("/agents");
    if (!response.ok) {
      throw new Error("エージェント定義を取得できませんでした。");
    }
    state.defaultAgents = await response.json();
    resetAgents();
  } catch (error) {
    showError(error.message);
  }
}

function resetAgents() {
  state.agents = state.defaultAgents.map((agent) => ({
    ...agent,
    enabled: true,
  }));
  renderAgents();
}

function renderAgents() {
  elements.agentList.innerHTML = "";

  state.agents.forEach((agent, index) => {
    const locked = agent.id === "moderator" || agent.id === "synthesizer";
    const card = document.createElement("article");
    card.className = `agent-card${locked ? " locked" : ""}`;

    const top = document.createElement("div");
    top.className = "agent-top";

    const label = document.createElement("label");
    label.className = "agent-name";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = agent.enabled;
    checkbox.disabled = locked;
    checkbox.addEventListener("change", () => {
      state.agents[index].enabled = checkbox.checked;
    });

    const name = document.createElement("span");
    name.textContent = agent.display_name;

    label.append(checkbox, name);
    top.append(label);

    const description = document.createElement("p");
    description.textContent = agent.description;

    const prompt = document.createElement("textarea");
    prompt.value = agent.system_prompt;
    prompt.setAttribute("aria-label", `${agent.display_name}の役割プロンプト`);
    prompt.addEventListener("input", () => {
      state.agents[index].system_prompt = prompt.value;
    });

    card.append(top, description, prompt);
    elements.agentList.append(card);
  });
}

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();

  const payload = {
    api_key: elements.apiKey.value.trim(),
    model: elements.model.value.trim(),
    question: elements.question.value.trim(),
    agents: state.agents,
  };

  const validationError = validatePayload(payload);
  if (validationError) {
    showError(validationError);
    return;
  }

  setRunning(true);
  renderLogs([]);
  elements.finalAnswer.textContent = "実行中...";

  try {
    const response = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "実行に失敗しました。");
    }

    renderLogs(data.logs || []);
    elements.finalAnswer.textContent = data.final_answer || "最終回答がありません。";
    elements.statusText.textContent = "完了";
  } catch (error) {
    showError(error.message);
    elements.finalAnswer.textContent = "エラーにより最終回答を生成できませんでした。";
    elements.statusText.textContent = "エラー";
  } finally {
    setRunning(false);
  }
});

elements.clearLog.addEventListener("click", () => {
  renderLogs([]);
  elements.finalAnswer.textContent = "まだ最終回答はありません。";
  elements.statusText.textContent = "待機中";
  clearError();
});

elements.resetAgents.addEventListener("click", resetAgents);

function validatePayload(payload) {
  if (!payload.api_key) return "APIキーを入力してください。";
  if (!payload.model) return "モデル名を入力してください。";
  if (!payload.question) return "質問を入力してください。";
  if (!payload.agents.some((agent) => agent.enabled && agent.id !== "moderator" && agent.id !== "synthesizer")) {
    return "回答用エージェントを1つ以上選択してください。";
  }
  return "";
}

function renderLogs(logs) {
  elements.logList.innerHTML = "";
  const discussionLogs = logs.filter((entry) => entry.agent !== "Synthesizer");

  if (!discussionLogs.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "質問を送信すると、各エージェントの発言がここに表示されます。";
    elements.logList.append(empty);
    return;
  }

  discussionLogs.forEach((entry) => {
    const article = document.createElement("article");
    article.className = "log-entry";

    const title = document.createElement("h3");
    title.textContent = entry.agent;

    const content = document.createElement("pre");
    content.textContent = entry.content;

    article.append(title, content);
    elements.logList.append(article);
  });
}

function setRunning(isRunning) {
  elements.runButton.disabled = isRunning;
  elements.runButton.textContent = isRunning ? "実行中..." : "実行";
  elements.statusText.textContent = isRunning ? "実行中" : elements.statusText.textContent;
}

function showError(message) {
  elements.errorMessage.textContent = message;
}

function clearError() {
  elements.errorMessage.textContent = "";
}

loadAgents();
