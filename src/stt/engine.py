"""
KoeBridge for Zoom — Speech-to-Text (STT) Engine Abstraction
"""

from typing import Optional, Dict, Any
import numpy as np
import time


class SttEngine:
    """
    STT Engine using faster-whisper (CTranslate2).
    Supports transcription and direct JA -> EN translation.
    """

    _SHARED_MODELS: Dict[tuple, Any] = {}

    def __init__(
        self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8"
    ):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = None
        self._is_loaded = False

    def load_model(self) -> bool:
        if self._is_loaded and self.model is not None:
            return True

        cache_key = (self.model_size, self.device, self.compute_type)
        if cache_key in SttEngine._SHARED_MODELS:
            self.model = SttEngine._SHARED_MODELS[cache_key]
            self._is_loaded = True
            return True

        try:
            from faster_whisper import WhisperModel

            print(
                f"[STT] Loading faster-whisper '{self.model_size}' model ({self.compute_type} on {self.device})..."
            )
            model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
                cpu_threads=4,
            )
            SttEngine._SHARED_MODELS[cache_key] = model
            self.model = model
            self._is_loaded = True
            print(f"[STT] faster-whisper '{self.model_size}' loaded successfully.")
            return True
        except ImportError:
            print("[STT] faster-whisper is not installed. Running in mock mode.")
            return False
        except Exception as e:
            print(f"[STT] Failed to load model '{self.model_size}': {e}")
            return False

    def transcribe(
        self,
        audio_data: np.ndarray,
        language: Optional[str] = None,
        task: str = "transcribe",  # 'transcribe' or 'translate'
    ) -> Dict[str, Any]:
        """
        Transcribe or directly translate speech audio.
        audio_data must be float32 1D numpy array at 16,000 Hz.
        """
        if not self._is_loaded:
            if not self.load_model():
                # Mock return for testing when model is uninstalled
                mock_text = (
                    "[Mock Transcription]"
                    if task == "transcribe"
                    else "[Mock Translation to English]"
                )
                return {
                    "text": mock_text,
                    "language": language or "ja",
                    "duration": len(audio_data) / 16000.0,
                    "latency_ms": 10.0,
                    "is_mock": True,
                }

        start_time = time.perf_counter()
        segments, info = self.model.transcribe(
            audio_data,
            language=language,
            task=task,
            beam_size=1,  # Greedy for minimal CPU latency
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )
        text = " ".join([seg.text.strip() for seg in segments]).strip()
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "text": text,
            "language": info.language,
            "language_probability": info.language_probability,
            "duration": info.duration,
            "latency_ms": elapsed_ms,
            "is_mock": False,
        }
