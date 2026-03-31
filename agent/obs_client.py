"""
OBS WebSocket client wrapper
Connects to OBS Studio's built-in WebSocket server (v5 protocol, OBS 28+)
"""

import obsws_python as obs


class OBSClient:
    def __init__(self, config: dict):
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 4455)
        self.password = config.get('password', '')
        self._client = None
        self._connect()

    def _connect(self):
        try:
            self._client = obs.ReqClient(
                host=self.host,
                port=self.port,
                password=self.password,
                timeout=5
            )
        except Exception as e:
            print(f"Warning: Could not connect to OBS WebSocket: {e}")
            self._client = None

    def is_connected(self) -> bool:
        if not self._client:
            return False
        try:
            self._client.get_version()
            return True
        except Exception:
            return False

    def ensure_connected(self):
        if not self.is_connected():
            self._connect()
        if not self._client:
            raise ConnectionError("OBS is not running or WebSocket is not enabled. "
                                  "Enable it in OBS: Tools → WebSocket Server Settings")

    # --- Version / Stats ---

    def get_version(self) -> dict:
        self.ensure_connected()
        r = self._client.get_version()
        return {'obsVersion': r.obs_version, 'websocketVersion': r.obs_web_socket_version}

    def get_stats(self) -> dict:
        self.ensure_connected()
        r = self._client.get_stats()
        return {
            'cpuUsage': r.cpu_usage,
            'memoryUsage': r.memory_usage,
            'activeFps': r.active_fps,
            'renderTotalFrames': r.render_total_frames,
            'renderSkippedFrames': r.render_skipped_frames,
            'outputTotalFrames': r.output_total_frames,
            'outputSkippedFrames': r.output_skipped_frames,
        }

    # --- Scenes ---

    def get_scene_list(self) -> dict:
        self.ensure_connected()
        r = self._client.get_scene_list()
        return {
            'currentScene': r.current_program_scene_name,
            'scenes': [s['sceneName'] for s in r.scenes]
        }

    def set_current_scene(self, scene_name: str):
        self.ensure_connected()
        self._client.set_current_program_scene(scene_name)
        return {'switched': scene_name}

    def create_scene(self, scene_name: str):
        self.ensure_connected()
        self._client.create_scene(scene_name)
        return {'created': scene_name}

    def remove_scene(self, scene_name: str):
        self.ensure_connected()
        self._client.remove_scene(scene_name)
        return {'removed': scene_name}

    def set_scene_name(self, old_name: str, new_name: str):
        self.ensure_connected()
        self._client.set_scene_name(old_name, new_name)
        return {'renamed': new_name}

    # --- Sources / Scene Items ---

    def get_input_kind_list(self) -> dict:
        self.ensure_connected()
        r = self._client.get_input_kind_list(False)
        return {'inputKinds': sorted(r.input_kinds)}

    def get_scene_item_list(self, scene_name: str) -> list:
        self.ensure_connected()
        r = self._client.get_scene_item_list(scene_name)
        return r.scene_items

    def create_input(self, scene_name: str, input_name: str, input_kind: str, input_settings: dict = None):
        self.ensure_connected()
        r = self._client.create_input(
            scene_name, input_name, input_kind,
            input_settings or {}, True
        )
        return {'sceneItemId': r.scene_item_id}

    def remove_input(self, input_name: str):
        self.ensure_connected()
        self._client.remove_input(input_name)
        return {'removed': input_name}

    def set_input_settings(self, input_name: str, settings: dict, overlay: bool = True):
        self.ensure_connected()
        self._client.set_input_settings(input_name, settings, overlay)
        return {'updated': input_name}

    def get_input_settings(self, input_name: str) -> dict:
        self.ensure_connected()
        r = self._client.get_input_settings(input_name)
        return {'kind': r.input_kind, 'settings': r.input_settings}

    def set_scene_item_transform(self, scene_name: str, scene_item_id: int, transform: dict):
        self.ensure_connected()
        self._client.set_scene_item_transform(scene_name, scene_item_id, transform)
        return {'transformed': scene_item_id}

    def set_scene_item_enabled(self, scene_name: str, scene_item_id: int, enabled: bool):
        self.ensure_connected()
        self._client.set_scene_item_enabled(scene_name, scene_item_id, enabled)
        return {'enabled': enabled}

    def get_scene_item_id(self, scene_name: str, source_name: str) -> int:
        self.ensure_connected()
        r = self._client.get_scene_item_id(scene_name, source_name)
        return r.scene_item_id

    # --- Audio ---

    def get_input_mute(self, input_name: str) -> bool:
        self.ensure_connected()
        r = self._client.get_input_mute(input_name)
        return r.input_muted

    def set_input_mute(self, input_name: str, muted: bool):
        self.ensure_connected()
        self._client.set_input_mute(input_name, muted)
        return {'muted': muted}

    def toggle_input_mute(self, input_name: str) -> bool:
        self.ensure_connected()
        r = self._client.toggle_input_mute(input_name)
        return r.input_muted

    def get_input_volume(self, input_name: str) -> dict:
        self.ensure_connected()
        r = self._client.get_input_volume(input_name)
        return {'volumeMul': r.input_volume_mul, 'volumeDb': r.input_volume_db}

    def set_input_volume(self, input_name: str, volume_db: float = None, volume_mul: float = None):
        self.ensure_connected()
        if volume_db is not None:
            self._client.set_input_volume(input_name, vol_db=volume_db)
        elif volume_mul is not None:
            self._client.set_input_volume(input_name, vol_mul=volume_mul)
        return {'set': input_name}

    def get_input_audio_monitor_type(self, input_name: str) -> str:
        self.ensure_connected()
        r = self._client.get_input_audio_monitor_type(input_name)
        return r.monitor_type

    def set_input_audio_monitor_type(self, input_name: str, monitor_type: str):
        self.ensure_connected()
        self._client.set_input_audio_monitor_type(input_name, monitor_type)
        return {'monitorType': monitor_type}

    def get_input_audio_sync_offset(self, input_name: str) -> int:
        self.ensure_connected()
        r = self._client.get_input_audio_sync_offset(input_name)
        return r.input_audio_sync_offset

    def set_input_audio_sync_offset(self, input_name: str, offset_ms: int):
        self.ensure_connected()
        self._client.set_input_audio_sync_offset(input_name, offset_ms)
        return {'syncOffset': offset_ms}

    # --- Filters ---

    def get_source_filter_list(self, source_name: str) -> list:
        self.ensure_connected()
        r = self._client.get_source_filter_list(source_name)
        return r.filters

    def create_source_filter(self, source_name: str, filter_name: str, filter_kind: str, filter_settings: dict = None):
        self.ensure_connected()
        self._client.create_source_filter(source_name, filter_name, filter_kind, filter_settings or {})
        return {'created': filter_name}

    def remove_source_filter(self, source_name: str, filter_name: str):
        self.ensure_connected()
        self._client.remove_source_filter(source_name, filter_name)
        return {'removed': filter_name}

    def set_source_filter_settings(self, source_name: str, filter_name: str, settings: dict, overlay: bool = True):
        self.ensure_connected()
        self._client.set_source_filter_settings(source_name, filter_name, settings, overlay)
        return {'updated': filter_name}

    def set_source_filter_enabled(self, source_name: str, filter_name: str, enabled: bool):
        self.ensure_connected()
        self._client.set_source_filter_enabled(source_name, filter_name, enabled)
        return {'enabled': enabled}

    # --- Recording ---

    def get_record_status(self) -> dict:
        self.ensure_connected()
        r = self._client.get_record_status()
        return {'active': r.output_active, 'paused': r.output_paused, 'timecode': r.output_timecode}

    def start_record(self):
        self.ensure_connected()
        self._client.start_record()
        return {'recording': True}

    def stop_record(self) -> str:
        self.ensure_connected()
        r = self._client.stop_record()
        return {'path': r.output_path}

    def pause_record(self):
        self.ensure_connected()
        self._client.pause_record()
        return {'paused': True}

    def resume_record(self):
        self.ensure_connected()
        self._client.resume_record()
        return {'resumed': True}

    # --- Streaming ---

    def get_stream_status(self) -> dict:
        self.ensure_connected()
        r = self._client.get_stream_status()
        return {
            'active': r.output_active,
            'reconnecting': r.output_reconnecting,
            'timecode': r.output_timecode,
            'bytes': r.output_bytes
        }

    def start_stream(self):
        self.ensure_connected()
        self._client.start_stream()
        return {'streaming': True}

    def stop_stream(self):
        self.ensure_connected()
        self._client.stop_stream()
        return {'streaming': False}

    # --- Virtual Camera ---

    def get_virtual_cam_status(self) -> dict:
        self.ensure_connected()
        r = self._client.get_virtual_cam_status()
        return {'active': r.output_active}

    def start_virtual_cam(self):
        self.ensure_connected()
        self._client.start_virtual_cam()
        return {'virtualCam': True}

    def stop_virtual_cam(self):
        self.ensure_connected()
        self._client.stop_virtual_cam()
        return {'virtualCam': False}

    # --- Hotkeys ---

    def get_hotkey_list(self) -> list:
        self.ensure_connected()
        r = self._client.get_hotkey_list()
        return r.hotkeys

    def trigger_hotkey_by_name(self, hotkey_name: str):
        self.ensure_connected()
        self._client.trigger_hotkey_by_name(hotkey_name)
        return {'triggered': hotkey_name}
