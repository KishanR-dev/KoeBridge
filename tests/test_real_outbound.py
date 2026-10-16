"""
KoeBridge for Zoom — Real Outbound Integration Tests
Tests real Argos Translate English-to-Japanese offline MT and AudioOutputRenderer format negotiation.
"""

import importlib.util
import pytest
import numpy as np

from src.mt.engine import MachineTranslationEngine
from src.audio.output import AudioOutputRenderer
from src.tts.engine import LocalJapaneseTtsEngine

ARGOS_AVAILABLE = importlib.util.find_spec("argostranslate") is not None
ONNX_AVAILABLE = importlib.util.find_spec("onnxruntime") is not None


@pytest.mark.skipif(not ARGOS_AVAILABLE, reason="argostranslate is not installed")
def test_real_argos_en_to_ja_translation():
    """Verify real ArgosTranslate EN->JA offline model translation."""
    mt = MachineTranslationEngine(from_code="en", to_code="ja")
    assert mt.load_model() is True

    # First call warms up the internal Stanza tokenizer pipeline
    mt.translate("Hello.")

    # Test representative meeting phrase on warm model
    res = mt.translate("Thank you very much.")
    assert res.get("is_mock") is False, "Translation fell back to mock"
    assert "ありがとう" in res.get("translated_text", ""), (
        f"Unexpected translation: {res}"
    )
    assert res.get("latency_ms", 9999) < 500.0, (
        f"Warm latency too high: {res.get('latency_ms')} ms"
    )


@pytest.mark.skipif(not ONNX_AVAILABLE, reason="onnxruntime is not installed")
def test_real_melotts_japanese_synthesis():
    """Verify real MeloTTS Japanese ONNX synthesis via LocalJapaneseTtsEngine."""
    tts = LocalJapaneseTtsEngine()
    assert tts._backend == "melotts_onnx", (
        f"Expected melotts_onnx backend, got {tts._backend}"
    )
    assert tts.sample_rate == 44100

    res = tts.synthesize("ありがとうございます。")
    assert res.get("is_mock") is False, "TTS fell back to mock"
    assert res.get("sample_rate") == 44100
    audio = res.get("audio")
    assert audio is not None and len(audio) > 0, "No audio generated"

    # Check non-silent speech
    rms = float(np.sqrt(np.mean(audio**2)))
    assert rms > 0.05, f"Audio is silent or too quiet: RMS={rms}"
    assert res.get("latency_ms", 9999) < 2500.0, (
        f"Latency too high: {res.get('latency_ms')} ms"
    )


def test_audio_output_renderer_format_negotiation_and_wav():
    """Verify AudioOutputRenderer hardware format negotiation and WAV export."""
    renderer = AudioOutputRenderer(sample_rate=24000)
    # Generate 0.1s 440Hz test sine tone
    t = np.linspace(0, 0.1, 2400, endpoint=False)
    audio = (0.1 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    # 1. Hardware format negotiation playback
    played = renderer.play_audio(audio, sample_rate=24000)
    assert played is True

    # 2. WAV file export
    test_wav = "test_verify_outbound.wav"
    saved = renderer.save_wav(test_wav, audio, sample_rate=24000)
    assert saved is True
    import os

    if os.path.exists(test_wav):
        os.remove(test_wav)
