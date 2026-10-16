"""
Unit tests for STT, MT, and Local TTS abstractions
"""

import numpy as np
from src.stt.engine import SttEngine
from src.mt.engine import MachineTranslationEngine
from src.tts.engine import LocalJapaneseTtsEngine


def test_stt_engine_mock():
    engine = SttEngine(model_size="tiny")
    dummy_audio = np.zeros(16000, dtype=np.float32)

    # Test inbound translation task
    res = engine.transcribe(dummy_audio, language="ja", task="translate")
    assert "text" in res
    assert "latency_ms" in res
    assert res["latency_ms"] >= 0


def test_mt_engine_mock():
    engine = MachineTranslationEngine(from_code="en", to_code="ja")
    res = engine.translate("Hello everyone, nice to meet you.")
    assert "translated_text" in res
    assert len(res["translated_text"]) > 0


def test_tts_engine_mock():
    engine = LocalJapaneseTtsEngine()
    res = engine.synthesize("こんにちは、よろしくお願いします。")
    assert "audio" in res
    assert "sample_rate" in res
    assert isinstance(res["audio"], np.ndarray)
    assert res["sample_rate"] > 0
