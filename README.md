# OBSAgent

An AI agent that lives inside OBS Studio. Describe what you want in plain English — it controls your entire production: scenes, sources, audio, filters, recording, streaming, and even generates images for backgrounds and overlays.

No plugin required. Just a local Python server and a browser dock.

> "Set up a gaming stream with my webcam bottom-right, game capture fullscreen, and a subscriber alert overlay"

> "Generate a cyberpunk 'Starting Soon' background and add it to my waiting scene"

> "Mute my mic, switch to BRB scene, and lower the desktop audio to 50%"

> "Create a 3-scene podcast setup with good defaults"

## How It Works

OBSAgent is a local Python/Flask server that connects to OBS Studio's built-in WebSocket API. A chat panel is docked directly inside OBS as a browser dock — no external app, no browser tab. You type what you want, the AI figures out which OBS operations to run, and executes them.

```
┌─────────────────────────────────────────────────────────┐
│                      OBS Studio                         │
│  ┌───────────────────┐  ┌───────────────────────────┐   │
│  │  Existing Panels   │  │  OBSAgent Chat (Docked)  │   │
│  │  (Scenes, Sources) │  │  "Make a starting soon   │   │
│  │                    │  │   screen with a cool bg"  │   │
│  └───────────────────┘  └────────────┬──────────────┘   │
│                                      │ HTTP              │
│         OBS WebSocket (4455)         │                   │
└──────────────────┬───────────────────┼───────────────────┘
                   │                   │
          ┌────────▼───────────────────▼────────┐
          │         Agent Backend (Flask)        │
          │                                      │
          │   ┌──────────┐    ┌──────────────┐   │
          │   │  Claude   │    │   OpenAI     │   │
          │   │ (Reason + │    │ (Image Gen)  │   │
          │   │  Control) │    │ gpt-image-   │   │
          │   │           │    │ 1.5          │   │
          │   └─────┬─────┘    └──────┬───────┘   │
          │         │                 │            │
          │   ┌─────▼─────────────────▼───────┐   │
          │   │     30+ OBS Tools             │   │
          │   │  Scenes · Sources · Audio     │   │
          │   │  Filters · Recording · Stream │   │
          │   │  Image Gen · Virtual Cam      │   │
          │   └───────────────────────────────┘   │
          └────────────────────────────────────────┘
```

## Why Two AIs?

OBSAgent uses **Claude** for reasoning and **OpenAI** for image generation. Each does what it's best at:

- **Claude** (Anthropic) powers the agent brain. Its tool-use API is purpose-built for agentic loops — the model decides which OBS operations to call, interprets the results, and chains multiple steps together. When you say "set up a podcast scene," Claude plans the sequence: check existing scenes, create new ones, add sources, position them, configure audio, and confirm back to you.

- **OpenAI** (gpt-image-1.5) handles image generation. When the agent needs to create a background, overlay, thumbnail, or any visual asset, it calls OpenAI's image API, saves the result locally, and feeds the file path back into OBS as an image source. This is optional — OBSAgent works without an OpenAI key, you just won't have AI image generation.

## Quick Start

### Prerequisites

- **OBS Studio v28+** with WebSocket server enabled (Tools → WebSocket Server Settings)
- **Python 3.10+**
- **Anthropic API key** ([console.anthropic.com](https://console.anthropic.com))
- **OpenAI API key** (optional, for AI image generation — [platform.openai.com](https://platform.openai.com))

### Setup

```bash
# Clone the repo
git clone https://github.com/glenwrhodes/OBSAgent.git
cd OBSAgent

# Install dependencies
cd agent
pip install -r requirements.txt

# Configure
cp ../config.example.json config.json
# Edit config.json: add your API keys and OBS WebSocket password
```

### Run

```bash
# From the agent/ directory
python server.py
```

Then in OBS:
1. Go to **Docks → Custom Browser Docks**
2. Add a new dock:
   - **Name**: `OBSAgent`
   - **URL**: `http://localhost:5050`
3. Click **Apply**

The chat panel appears as a dockable window inside OBS. Start typing.

## Features

### Scene Management
- Create, rename, delete, and switch scenes
- Build complete multi-scene setups from a single description

### Source Control
- Add, remove, position, resize, and configure any source type
- Automatically discovers available source types for your OBS version
- Control visibility per scene

### AI Image Generation
- Generate backgrounds, overlays, logos, and thumbnails on demand
- Images are created via OpenAI's gpt-image-1.5 and saved locally
- Supports transparent backgrounds for overlays
- Sizes optimized for streaming: 1920x1080, 1024x1024, and more
- Generated images are automatically added to scenes as image sources

### Audio
- Volume, mute, and monitor type per source
- Apply and configure filters: compressor, noise suppression, EQ, limiter, gain, noise gate
- Audio sync offset control

### Filters
- Add, remove, enable/disable any filter on any source
- Configure filter settings (chroma key, color correction, etc.)

### Recording & Streaming
- Start/stop recording and streaming
- Virtual camera control
- Status monitoring

### Chat UI
- Dark theme matching OBS
- Markdown rendering for rich agent responses
- Quick-action buttons for common tasks
- New Chat button to reset context

## Configuration

```json
{
  "anthropic_api_key": "sk-ant-...",
  "openai_api_key": "sk-...",
  "obs_websocket": {
    "host": "localhost",
    "port": 4455,
    "password": "your-obs-ws-password"
  },
  "agent": {
    "model": "claude-opus-4-6",
    "max_tokens": 4096,
    "max_iterations": 20
  },
  "server": {
    "port": 5050,
    "host": "127.0.0.1"
  }
}
```

| Key | Required | Description |
|-----|----------|-------------|
| `anthropic_api_key` | Yes | Anthropic API key for Claude |
| `openai_api_key` | No | OpenAI API key for image generation |
| `obs_websocket.password` | Yes | From OBS → Tools → WebSocket Server Settings |
| `agent.model` | No | Claude model (default: `claude-opus-4-6`) |
| `server.port` | No | Local server port (default: `5050`) |

## Project Structure

```
ui/templates/index.html    Chat UI (docked in OBS via browser dock)
agent/server.py            Flask server: routes and API endpoints
agent/agent.py             Agent loop: Claude + tool use
agent/tools.py             Tool definitions + dispatch
agent/obs_client.py        OBS WebSocket client wrapper
agent/image_gen.py         OpenAI image generation wrapper
agent/generated_images/    AI-generated images (gitignored)
config.example.json        Config template
```

## Roadmap

- [x] OBS WebSocket client with full scene/source/audio/filter control
- [x] Agentic loop with Claude tool use
- [x] Chat UI docked inside OBS (dark theme, markdown rendering)
- [x] AI image generation (OpenAI gpt-image-1.5)
- [x] Dynamic source type discovery (works across OBS versions)
- [ ] Voice input support
- [ ] Stream health monitoring and alerts
- [ ] Post-stream highlight detection
- [ ] Native C++ OBS plugin (v2)

## Contributing

Contributions are welcome. The codebase is intentionally simple — single-file modules, no framework beyond Flask, no build step for the UI.

To add a new OBS tool:
1. Add a tool definition dict to `get_all_tools()` in `agent/tools.py`
2. Add an `elif` branch in `execute_tool()` in `agent/tools.py`
3. Add the corresponding method to `OBSClient` in `agent/obs_client.py`

## License

[MIT](LICENSE)
