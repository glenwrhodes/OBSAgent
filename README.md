# OBSAgent

An AI agent chat panel for OBS Studio. Describe what you want in natural language — the agent controls your entire production.

> "Set up a gaming stream with my webcam bottom-right, game capture fullscreen, and a subscriber alert overlay"
> "Mute my mic and switch to BRB scene"
> "Optimize my audio for streaming — I'm getting some background noise"
> "Create a 3-scene podcast setup with good defaults"

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   OBS Studio                        │
│  ┌──────────────────┐  ┌──────────────────────────┐ │
│  │  Existing Panels  │  │  OBSAgent Browser Dock  │ │
│  │  (Scenes, Sources)│  │  ┌────────────────────┐ │ │
│  │                   │  │  │  Chat UI (HTML/JS) │ │ │
│  └──────────────────┘  │  └────────────────────┘ │ │
│                         └──────────┬─────────────┘ │
│              OBS WebSocket API     │               │
│              (port 4455)           │               │
└──────────────────────────────────┼─────────────────┘
                                   │ HTTP
                          ┌────────▼────────┐
                          │  Agent Backend  │
                          │  (Python/Flask) │
                          │                 │
                          │  ┌───────────┐  │
                          │  │  Claude   │  │
                          │  │  (claude- │  │
                          │  │  opus-4)  │  │
                          │  └─────┬─────┘  │
                          │        │        │
                          │  ┌─────▼─────┐  │
                          │  │ OBS Tools │  │
                          │  │ (30+)     │  │
                          │  └───────────┘  │
                          └─────────────────┘
```

## How it works

1. **OBS WebSocket** — OBS Studio has a built-in WebSocket server (enabled in Tools → WebSocket Server Settings). OBSAgent connects to it and gets full read/write access to your OBS state.

2. **Agent backend** — A local Python server runs the AI agent. It has tools mapped to every major OBS WebSocket command: scene management, source control, audio, filters, recording, streaming, and more.

3. **Chat UI** — A simple web interface served locally and docked inside OBS via the Custom Browser Docks feature (no plugin required). You type commands, the agent runs, OBS responds.

4. **No C++ required** — This approach works entirely through OBS's existing plugin-free WebSocket API. A native C++ plugin version is planned for v2.

## Quick Start

```bash
# 1. Install dependencies
cd agent
pip install -r requirements.txt

# 2. Configure
cp config.example.json config.json
# Edit config.json: add your Anthropic API key, OBS WebSocket password

# 3. Start the agent server
python server.py

# 4. In OBS: Docks → Custom Browser Docks → Add
#    Name: OBSAgent
#    URL: http://localhost:5050
```

## Features

### Scene Management
- Create, rename, delete, and switch scenes
- Set scene transitions and durations
- Build complete scene collections from a description

### Source Control
- Add, remove, position, resize, and reorder sources
- Control visibility and locked state
- Configure source settings

### Audio
- Set volume, mute, monitor type per source
- Apply and configure filters (compressor, noise suppression, EQ, limiter)
- Set audio sync offsets

### Filters
- Add and configure any filter on any source
- Enable/disable filters
- Reorder filter chains

### Recording & Streaming
- Start/stop recording and streaming
- Configure output settings
- Set recording directory and format

### Virtual Camera
- Start/stop virtual camera

### Overlays & Text
- Create and update text sources
- Manage browser sources (alerts, overlays)
- Control image sources

## OBS Tools Reference

See [docs/tools.md](docs/tools.md) for the full list of agent tools and their parameters.

## Configuration

```json
{
  "anthropic_api_key": "sk-ant-...",
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

## Roadmap

- [x] Project structure
- [ ] OBS WebSocket client (obsws-python)
- [ ] Core tool set (scenes, sources, audio)
- [ ] Agent loop (Claude + tools)
- [ ] Chat UI (HTML/JS, dark theme matching OBS)
- [ ] Installer / setup script
- [ ] Extended tool set (filters, recording, streaming)
- [ ] Voice input support
- [ ] Native C++ plugin (v2)
- [ ] Stream health monitoring
- [ ] Post-stream highlight detection

## Requirements

- OBS Studio v28+ (for WebSocket support)
- Python 3.10+
- Anthropic API key

## License

MIT
