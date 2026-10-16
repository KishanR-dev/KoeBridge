"""
KoeBridge for Zoom — Real Inbound Integration Tests
Tests real faster-whisper inference and real WASAPI loopback capture on Windows x64.
"""

import importlib.util
import os
import pytest
import numpy as np
from src.stt.engine import SttEngine
from src.audio.capture import AudioCaptureStream

REAL_DEPS_AVAILABLE = (
    importlib.util.find_spec("av") is not None
    and importlib.util.find_spec("pyaudiowpatch") is not None
    and importlib.util.find_spec("faster_whisper") is not None
)


@pytest.mark.skipif(
    not REAL_DEPS_AVAILABLE, reason="faster-whisper, av, or pyaudiowpatch not installed"
)
def test_real_faster_whisper_direct_translation():
    """Verify real faster-whisper tiny int8 inference on spoken Japanese audio."""
    import av

    sample_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "sample_arigato.oga"
    )
    assert os.path.exists(sample_path), f"Sample audio missing: {sample_path}"

    container = av.open(sample_path)
    resampler = av.audio.resampler.AudioResampler(
        format="fltp", layout="mono", rate=16000
    )
    frames = []
    for frame in container.decode(audio=0):
        for r in resampler.resample(frame):
            frames.append(r.to_ndarray())
    audio_arr = np.concatenate(frames, axis=1).squeeze(0)

    engine = SttEngine(model_size="tiny")
    assert engine.load_model() is True

    # 1. Direct Japanese -> English Translation
    result_translate = engine.transcribe(audio_arr, language="ja", task="translate")
    assert "Thank you" in result_translate["text"], (
        f"Unexpected translation: {result_translate['text']}"
    )
    assert result_translate["language"] == "ja"

    # 2. Japanese Transcription
    result_transcribe = engine.transcribe(audio_arr, language="ja", task="transcribe")
    assert "ありがとう" in result_transcribe["text"], (
        f"Unexpected transcription: {result_transcribe['text']}"
    )


@pytest.mark.skipif(not REAL_DEPS_AVAILABLE, reason="pyaudiowpatch not installed")
def test_real_wasapi_loopback_stream_lifecycle():
    """Verify WASAPI loopback stream initializes, negotiates native format, and terminates cleanly."""
    stream = AudioCaptureStream(is_loopback=True)
    started = stream.start()
    assert started is True
    assert stream.is_running is True
    stream.stop()
    assert stream.is_running is False
