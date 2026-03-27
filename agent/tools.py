"""
Tool definitions for the OBSAgent Claude integration.
Each tool maps to an OBS WebSocket operation.
"""


def get_all_tools() -> list:
    return [
        # --- Scene tools ---
        {
            "name": "get_scene_list",
            "description": "Get the list of all scenes and the current active scene.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "switch_scene",
            "description": "Switch the active scene to the specified scene name.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string", "description": "Name of the scene to switch to"}
                },
                "required": ["scene_name"]
            }
        },
        {
            "name": "create_scene",
            "description": "Create a new empty scene.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string", "description": "Name for the new scene"}
                },
                "required": ["scene_name"]
            }
        },
        {
            "name": "remove_scene",
            "description": "Delete a scene by name.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string", "description": "Name of the scene to remove"}
                },
                "required": ["scene_name"]
            }
        },
        {
            "name": "rename_scene",
            "description": "Rename an existing scene.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "old_name": {"type": "string"},
                    "new_name": {"type": "string"}
                },
                "required": ["old_name", "new_name"]
            }
        },

        # --- Source / Scene item tools ---
        {
            "name": "get_scene_sources",
            "description": "List all sources (scene items) in a scene.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string"}
                },
                "required": ["scene_name"]
            }
        },
        {
            "name": "add_source",
            "description": "Add a new source to a scene. input_kind options: 'monitor_capture' (screen capture), 'dshow_video' (webcam/capture card), 'image_source' (image), 'browser_source' (webpage/overlay), 'text_gdiplus_v3' (text on Windows), 'ffmpeg_source' (media file), 'wasapi_input_capture' (mic), 'wasapi_output_capture' (desktop audio).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string"},
                    "source_name": {"type": "string", "description": "Name for the new source"},
                    "input_kind": {"type": "string", "description": "OBS source type identifier"},
                    "settings": {"type": "object", "description": "Source-specific settings (optional)"}
                },
                "required": ["scene_name", "source_name", "input_kind"]
            }
        },
        {
            "name": "remove_source",
            "description": "Remove a source (input) from OBS entirely.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"}
                },
                "required": ["source_name"]
            }
        },
        {
            "name": "set_source_visibility",
            "description": "Show or hide a source in a scene.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string"},
                    "source_name": {"type": "string"},
                    "visible": {"type": "boolean"}
                },
                "required": ["scene_name", "source_name", "visible"]
            }
        },
        {
            "name": "set_source_transform",
            "description": "Set the position, size, and rotation of a source in a scene. positionX/Y are pixel coordinates. scaleX/Y are multipliers (1.0 = original size). rotation is in degrees.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "scene_name": {"type": "string"},
                    "source_name": {"type": "string"},
                    "position_x": {"type": "number"},
                    "position_y": {"type": "number"},
                    "scale_x": {"type": "number"},
                    "scale_y": {"type": "number"},
                    "rotation": {"type": "number"}
                },
                "required": ["scene_name", "source_name"]
            }
        },
        {
            "name": "update_source_settings",
            "description": "Update the settings of an existing source (e.g., change a text source's content, update a browser source URL).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "settings": {"type": "object", "description": "Settings to update (merged with existing)"}
                },
                "required": ["source_name", "settings"]
            }
        },
        {
            "name": "get_source_settings",
            "description": "Get the current settings of a source.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"}
                },
                "required": ["source_name"]
            }
        },

        # --- Audio tools ---
        {
            "name": "set_volume",
            "description": "Set the volume of an audio source. Use volume_db for decibel value (-100 to 26) or volume_mul for multiplier (0.0 to 20.0). 0 dB = 100% volume.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "volume_db": {"type": "number", "description": "Volume in dB (-100 to 26)"},
                    "volume_mul": {"type": "number", "description": "Volume as multiplier (0.0 to 20.0)"}
                },
                "required": ["source_name"]
            }
        },
        {
            "name": "get_volume",
            "description": "Get the current volume of an audio source.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"}
                },
                "required": ["source_name"]
            }
        },
        {
            "name": "mute_source",
            "description": "Mute or unmute an audio source.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "muted": {"type": "boolean"}
                },
                "required": ["source_name", "muted"]
            }
        },
        {
            "name": "set_audio_monitor",
            "description": "Set audio monitoring type. monitor_type options: 'OBS_MONITORING_TYPE_NONE', 'OBS_MONITORING_TYPE_MONITOR_ONLY', 'OBS_MONITORING_TYPE_MONITOR_AND_OUTPUT'.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "monitor_type": {"type": "string"}
                },
                "required": ["source_name", "monitor_type"]
            }
        },
        {
            "name": "set_audio_sync_offset",
            "description": "Set the audio sync offset for a source in milliseconds.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "offset_ms": {"type": "integer"}
                },
                "required": ["source_name", "offset_ms"]
            }
        },

        # --- Filter tools ---
        {
            "name": "get_filters",
            "description": "Get all filters applied to a source.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"}
                },
                "required": ["source_name"]
            }
        },
        {
            "name": "add_filter",
            "description": "Add a filter to a source. Common filter_kind values: 'noise_suppress_filter_v2' (noise suppression), 'compressor_filter' (compressor), 'equalizer_filter' (EQ), 'limiter_filter' (limiter), 'gain_filter' (gain), 'noise_gate_filter' (noise gate), 'chroma_key_filter_v2' (chroma key/greenscreen), 'color_correction_filter' (color correction).",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "filter_name": {"type": "string"},
                    "filter_kind": {"type": "string"},
                    "settings": {"type": "object", "description": "Filter-specific settings"}
                },
                "required": ["source_name", "filter_name", "filter_kind"]
            }
        },
        {
            "name": "remove_filter",
            "description": "Remove a filter from a source.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "filter_name": {"type": "string"}
                },
                "required": ["source_name", "filter_name"]
            }
        },
        {
            "name": "update_filter",
            "description": "Update the settings of an existing filter.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "filter_name": {"type": "string"},
                    "settings": {"type": "object"}
                },
                "required": ["source_name", "filter_name", "settings"]
            }
        },
        {
            "name": "set_filter_enabled",
            "description": "Enable or disable a filter without removing it.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "source_name": {"type": "string"},
                    "filter_name": {"type": "string"},
                    "enabled": {"type": "boolean"}
                },
                "required": ["source_name", "filter_name", "enabled"]
            }
        },

        # --- Recording / Streaming ---
        {
            "name": "get_record_status",
            "description": "Check if recording is active.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "start_recording",
            "description": "Start recording.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "stop_recording",
            "description": "Stop recording. Returns the path to the saved file.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "get_stream_status",
            "description": "Check if streaming is active.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "start_streaming",
            "description": "Start streaming.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "stop_streaming",
            "description": "Stop streaming.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "get_virtual_cam_status",
            "description": "Check if virtual camera is active.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "start_virtual_cam",
            "description": "Start virtual camera.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
        {
            "name": "stop_virtual_cam",
            "description": "Stop virtual camera.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },

        # --- Utility ---
        {
            "name": "get_obs_stats",
            "description": "Get OBS performance stats: CPU usage, memory, FPS, dropped frames.",
            "input_schema": {"type": "object", "properties": {}, "required": []}
        },
    ]


def execute_tool(obs_client, tool_name: str, tool_input: dict):
    """Route a tool call to the appropriate OBS client method"""
    t = tool_name

    if t == "get_scene_list":
        return obs_client.get_scene_list()
    elif t == "switch_scene":
        return obs_client.set_current_scene(tool_input["scene_name"])
    elif t == "create_scene":
        return obs_client.create_scene(tool_input["scene_name"])
    elif t == "remove_scene":
        return obs_client.remove_scene(tool_input["scene_name"])
    elif t == "rename_scene":
        return obs_client.set_scene_name(tool_input["old_name"], tool_input["new_name"])
    elif t == "get_scene_sources":
        return obs_client.get_scene_item_list(tool_input["scene_name"])
    elif t == "add_source":
        return obs_client.create_input(
            tool_input["scene_name"],
            tool_input["source_name"],
            tool_input["input_kind"],
            tool_input.get("settings", {})
        )
    elif t == "remove_source":
        return obs_client.remove_input(tool_input["source_name"])
    elif t == "set_source_visibility":
        item_id = obs_client.get_scene_item_id(tool_input["scene_name"], tool_input["source_name"])
        return obs_client.set_scene_item_enabled(tool_input["scene_name"], item_id, tool_input["visible"])
    elif t == "set_source_transform":
        item_id = obs_client.get_scene_item_id(tool_input["scene_name"], tool_input["source_name"])
        transform = {}
        if "position_x" in tool_input: transform["positionX"] = tool_input["position_x"]
        if "position_y" in tool_input: transform["positionY"] = tool_input["position_y"]
        if "scale_x" in tool_input: transform["scaleX"] = tool_input["scale_x"]
        if "scale_y" in tool_input: transform["scaleY"] = tool_input["scale_y"]
        if "rotation" in tool_input: transform["rotation"] = tool_input["rotation"]
        return obs_client.set_scene_item_transform(tool_input["scene_name"], item_id, transform)
    elif t == "update_source_settings":
        return obs_client.set_input_settings(tool_input["source_name"], tool_input["settings"])
    elif t == "get_source_settings":
        return obs_client.get_input_settings(tool_input["source_name"])
    elif t == "set_volume":
        return obs_client.set_input_volume(
            tool_input["source_name"],
            volume_db=tool_input.get("volume_db"),
            volume_mul=tool_input.get("volume_mul")
        )
    elif t == "get_volume":
        return obs_client.get_input_volume(tool_input["source_name"])
    elif t == "mute_source":
        return obs_client.set_input_mute(tool_input["source_name"], tool_input["muted"])
    elif t == "set_audio_monitor":
        return obs_client.set_input_audio_monitor_type(tool_input["source_name"], tool_input["monitor_type"])
    elif t == "set_audio_sync_offset":
        return obs_client.set_input_audio_sync_offset(tool_input["source_name"], tool_input["offset_ms"])
    elif t == "get_filters":
        return obs_client.get_source_filter_list(tool_input["source_name"])
    elif t == "add_filter":
        return obs_client.create_source_filter(
            tool_input["source_name"], tool_input["filter_name"],
            tool_input["filter_kind"], tool_input.get("settings", {})
        )
    elif t == "remove_filter":
        return obs_client.remove_source_filter(tool_input["source_name"], tool_input["filter_name"])
    elif t == "update_filter":
        return obs_client.set_source_filter_settings(
            tool_input["source_name"], tool_input["filter_name"], tool_input["settings"]
        )
    elif t == "set_filter_enabled":
        return obs_client.set_source_filter_enabled(
            tool_input["source_name"], tool_input["filter_name"], tool_input["enabled"]
        )
    elif t == "get_record_status":
        return obs_client.get_record_status()
    elif t == "start_recording":
        return obs_client.start_record()
    elif t == "stop_recording":
        return obs_client.stop_record()
    elif t == "get_stream_status":
        return obs_client.get_stream_status()
    elif t == "start_streaming":
        return obs_client.start_stream()
    elif t == "stop_streaming":
        return obs_client.stop_stream()
    elif t == "get_virtual_cam_status":
        return obs_client.get_virtual_cam_status()
    elif t == "start_virtual_cam":
        return obs_client.start_virtual_cam()
    elif t == "stop_virtual_cam":
        return obs_client.stop_virtual_cam()
    elif t == "get_obs_stats":
        return obs_client.get_stats()
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
