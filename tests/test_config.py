"""
Unit tests for KoeBridge configuration
"""

import os
import tempfile
from src.config import AppConfig


def test_default_config():
    cfg = AppConfig()
    assert cfg.audio.loopback_device_name == "Default Playback (Loopback)"
    assert cfg.pipeline.inbound_enabled is True
    assert cfg.pipeline.outbound_enabled is True
    assert cfg.pipeline.inbound_language == "ja"
    assert cfg.pipeline.inbound_task == "translate"
    assert cfg.gui.overlay_enabled is True


def test_config_serialization():
    cfg = AppConfig()
    cfg.pipeline.inbound_model_size = "base"
    cfg.gui.overlay_font_size = 24

    with tempfile.TemporaryDirectory() as tmpdir:
        test_path = os.path.join(tmpdir, "test_config.json")
        # Monkeypatch get_config_path
        AppConfig.get_config_path = classmethod(lambda cls: test_path)

        cfg.save()
        assert os.path.exists(test_path)

        loaded_cfg = AppConfig.load()
        assert loaded_cfg.pipeline.inbound_model_size == "base"
        assert loaded_cfg.gui.overlay_font_size == 24
