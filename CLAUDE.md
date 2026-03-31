# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Server

```bash
cd agent
pip install -r requirements.txt          # First time setup
python server.py                         # Start the agent server (http://127.0.0.1:5050)
```

Config lives at `agent/config.json` (gitignored). Copy from `config.example.json` and fill in your Anthropic API key and OBS WebSocket password.

## Architecture

OBSAgent is a local Python/Flask server that embeds an AI chat panel inside OBS Studio via its Custom Browser Docks feature. There is no plugin required.

```
ui/templates/index.html    ← Chat UI served at http://localhost:5050 (docked in OBS)
agent/server.py            ← Flask server: routes /, /api/chat, /api/status, /api/scenes
agent/agent.py             ← OBSAgent class: agentic loop using Claude's tool use API
agent/tools.py             ← Tool definitions (get_all_tools) + tool dispatch (execute_tool)
agent/obs_client.py        ← OBSClient: wraps obsws-python ReqClient for OBS WebSocket v5
agent/image_gen.py         ← ImageGenerator: wraps OpenAI gpt-image-1.5 for AI image generation
```

**Data flow for a chat message:**
1. Browser UI (`index.html`) POSTs to `/api/chat` with `{message, history}`
2. `server.py` calls `agent.run(message, history)`
3. `agent.py` runs a while-loop calling the Claude API with tools until `stop_reason == 'end_turn'` or max iterations (20) is reached
4. Each tool call is dispatched via `execute_tool()` in `tools.py`, which routes to the corresponding `OBSClient` method
5. `OBSClient` calls `obsws-python`'s `ReqClient` which speaks OBS WebSocket protocol v5 (port 4455)

**Adding a new OBS tool:**
- Add a tool definition dict to `get_all_tools()` in `tools.py`
- Add an `elif` branch in `execute_tool()` in `tools.py`
- Add the corresponding method to `OBSClient` in `obs_client.py`

**Config schema** (`agent/config.json`):
- `anthropic_api_key` — Anthropic API key
- `openai_api_key` — OpenAI API key (optional, enables AI image generation)
- `obs_websocket.{host, port, password}` — OBS WebSocket connection (default: localhost:4455)
- `agent.{model, max_tokens, max_iterations}` — Claude model settings (default: claude-opus-4-6)
- `server.{host, port}` — Flask server binding (default: 127.0.0.1:5050)

**OBS connection:** `OBSClient` attempts to connect at startup and gracefully degrades (sets `_client = None`) if OBS isn't running. `ensure_connected()` is called before every operation and raises `ConnectionError` with a human-readable message if OBS is unavailable.

**Chat history:** The UI maintains a rolling window of the last 20 messages in JS memory (not persisted). History is passed to every `/api/chat` request and forwarded to the Claude API as prior messages.

**UI:** Single-file HTML/CSS/JS in `ui/templates/index.html`. Dark theme matching OBS. No build step, no framework.
