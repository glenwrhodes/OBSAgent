# OBSAgent Tool Reference

Full list of tools available to the agent.

## Scene Management
| Tool | Description |
|------|-------------|
| `get_scene_list` | List all scenes + current active scene |
| `switch_scene` | Switch to a scene by name |
| `create_scene` | Create a new empty scene |
| `remove_scene` | Delete a scene |
| `rename_scene` | Rename a scene |

## Source Control
| Tool | Description |
|------|-------------|
| `get_scene_sources` | List all sources in a scene |
| `add_source` | Add a new source (screen capture, webcam, image, text, browser, audio) |
| `remove_source` | Remove a source entirely |
| `set_source_visibility` | Show/hide a source |
| `set_source_transform` | Position, scale, rotate a source |
| `update_source_settings` | Update source-specific settings |
| `get_source_settings` | Read current source settings |

## Audio
| Tool | Description |
|------|-------------|
| `set_volume` | Set volume in dB or multiplier |
| `get_volume` | Read current volume |
| `mute_source` | Mute/unmute an audio source |
| `set_audio_monitor` | Set monitoring type (none/monitor/monitor+output) |
| `set_audio_sync_offset` | Set audio delay in milliseconds |

## Filters
| Tool | Description |
|------|-------------|
| `get_filters` | List filters on a source |
| `add_filter` | Add a filter (noise suppression, compressor, EQ, limiter, gain, chroma key, etc.) |
| `remove_filter` | Remove a filter |
| `update_filter` | Change filter settings |
| `set_filter_enabled` | Enable/disable a filter |

## Recording
| Tool | Description |
|------|-------------|
| `get_record_status` | Check if recording |
| `start_recording` | Start recording |
| `stop_recording` | Stop recording (returns file path) |

## Streaming
| Tool | Description |
|------|-------------|
| `get_stream_status` | Check if streaming |
| `start_streaming` | Start stream |
| `stop_streaming` | Stop stream |

## Virtual Camera
| Tool | Description |
|------|-------------|
| `get_virtual_cam_status` | Check virtual cam status |
| `start_virtual_cam` | Start virtual camera |
| `stop_virtual_cam` | Stop virtual camera |

## Utility
| Tool | Description |
|------|-------------|
| `get_obs_stats` | CPU, memory, FPS, dropped frames |

## Common Source Types (input_kind)
| Kind | Description |
|------|-------------|
| `monitor_capture` | Screen/monitor capture |
| `window_capture` | Specific window capture |
| `dshow_video` | Webcam / capture card (Windows) |
| `image_source` | Static image |
| `browser_source` | Webpage / alerts overlay |
| `text_gdiplus_v3` | Text (Windows) |
| `ffmpeg_source` | Media file (video/audio) |
| `wasapi_input_capture` | Microphone (Windows) |
| `wasapi_output_capture` | Desktop audio (Windows) |
| `game_capture` | Game capture (Windows) |

## Common Filter Types (filter_kind)
| Kind | Description |
|------|-------------|
| `noise_suppress_filter_v2` | AI noise suppression |
| `noise_gate_filter` | Noise gate |
| `compressor_filter` | Compressor |
| `limiter_filter` | Limiter |
| `gain_filter` | Gain |
| `equalizer_filter` | EQ |
| `chroma_key_filter_v2` | Chroma key / greenscreen |
| `color_correction_filter` | Color correction |
| `scroll_filter` | Scroll effect |
| `sharpness_filter` | Sharpness |
