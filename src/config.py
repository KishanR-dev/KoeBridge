"""
KoeBridge for Zoom — Configuration & Runtime Settings
"""

from dataclasses import dataclass, field
from typing import Optional
import os
import json


@dataclass
class AudioDeviceConfig:
    loopback_device_id: Optional[int] = None
    loopback_device_name: str = "Default Playback (Loopback)"
    microphone_device_id: Optional[int] = None
    microphone_device_name: str = "Default Microphone"
    cable_input_device_id: Optional[int] = None
    cable_input_device_name: str = "CABLE Input (VB-Audio Virtual Cable)"
    headphones_device_id: Optional[int] = None
    headphones_device_name: str = "Default Headphones"


@dataclass
class PipelineConfig:
    # Inbound (Zoom JA -> EN Captions)
    inbound_enabled: bool = True
    inbound_model_size: str = "tiny"  # tiny or base for CPU low-latency
    inbound_language: str = "ja"
    inbound_task: str = "translate"  # Whisper direct JA -> EN translation

    # Outbound (User EN -> JA Voice into Zoom)
    outbound_enabled: bool = True
    outbound_stt_model_size: str = "tiny"
    outbound_source_lang: str = "en"
    outbound_target_lang: str = "ja"
    ptt_hotkey: str = "space"  # Global or in-app PTT hotkey

    # Audio buffer parameters
    sample_rate: int = 16000
    channels: int = 1
    chunk_size_ms: int = 30  # 30ms audio chunks
    vad_threshold: float = 0.5
    inbound_silence_timeout_s: float = 1.0  # Finalize sentence after 1s silence
    outbound_max_utterance_s: float = 15.0


@dataclass
class GuiConfig:
    overlay_enabled: bool = True
    overlay_font_size: int = 18
    overlay_bg_color: str = "#1e1e1e"
    overlay_fg_color: str = "#ffffff"
    overlay_opacity: float = 0.85
    show_timestamps: bool = True


@dataclass
class AppConfig:
    audio: AudioDeviceConfig = field(default_factory=AudioDeviceConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    gui: GuiConfig = field(default_factory=GuiConfig)

    @classmethod
    def get_config_path(cls) -> str:
        app_data = os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))
        kb_dir = os.path.join(app_data, "KoeBridge")
        os.makedirs(kb_dir, exist_ok=True)
        return os.path.join(kb_dir, "config.json")

    def save(self) -> None:
        path = self.get_config_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, indent=2, default=lambda o: o.__dict__)
        except Exception as e:
            print(f"[Config] Error saving configuration: {e}")

    @classmethod
    def load(cls) -> "AppConfig":
        path = cls.get_config_path()
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                cfg = cls()
                if "audio" in data:
                    cfg.audio = AudioDeviceConfig(**data["audio"])
                if "pipeline" in data:
                    cfg.pipeline = PipelineConfig(**data["pipeline"])
                if "gui" in data:
                    cfg.gui = GuiConfig(**data["gui"])
                return cfg
            except Exception as e:
                print(f"[Config] Error loading configuration: {e}. Using defaults.")
        return cls()
