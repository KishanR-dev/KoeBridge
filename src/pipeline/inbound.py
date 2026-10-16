"""
KoeBridge for Zoom — Inbound Pipeline (Zoom JA Loopback -> EN Captions)
"""

import threading
import time
from typing import Callable, Optional
import numpy as np

from ..audio.capture import AudioCaptureStream
from ..stt.engine import SttEngine


class InboundPipeline:
    """
    Inbound Pipeline: Captures Japanese audio from Zoom playback loopback,
    translates directly to English text via faster-whisper, and notifies caption listeners.
    """

    def __init__(
        self,
        loopback_device_id: Optional[int] = None,
        model_size: str = "tiny",
        on_caption: Optional[Callable[[str, float], None]] = None,
        silence_timeout_s: float = 1.0,
        energy_threshold: float = 0.015,
    ):
        self.loopback_device_id = loopback_device_id
        self.on_caption = on_caption
        self.silence_timeout_s = silence_timeout_s
        self.energy_threshold = energy_threshold

        self.capture = AudioCaptureStream(
            device_index=loopback_device_id,
            sample_rate=16000,
            channels=1,
            chunk_size=480,  # 30 ms chunks
            is_loopback=True,
        )
        self.stt = SttEngine(model_size=model_size)

        self._running = False
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        if self._running:
            return True
        self._running = True
        self.capture.start()
        self._thread = threading.Thread(
            target=self._worker_loop, daemon=True, name="InboundPipelineWorker"
        )
        self._thread.start()
        print("[InboundPipeline] Started.")
        return True

    def stop(self) -> None:
        self._running = False
        self.capture.stop()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)
        self._thread = None
        print("[InboundPipeline] Stopped.")

    def _worker_loop(self) -> None:
        speech_buffer = []
        silence_start_time = None
        is_speaking = False

        while self._running:
            chunk = self.capture.get_chunk(timeout=0.05)
            if chunk is None:
                continue

            # Calculate RMS energy of chunk
            rms = np.sqrt(np.mean(chunk**2))

            if rms >= self.energy_threshold:
                if not is_speaking:
                    is_speaking = True
                silence_start_time = None
                speech_buffer.append(chunk)
            else:
                if is_speaking:
                    speech_buffer.append(chunk)
                    if silence_start_time is None:
                        silence_start_time = time.time()
                    elif time.time() - silence_start_time >= self.silence_timeout_s:
                        # Utterance finished, process through STT
                        self._process_utterance(speech_buffer)
                        speech_buffer = []
                        is_speaking = False
                        silence_start_time = None

    def _process_utterance(self, buffer_chunks: list) -> None:
        if not buffer_chunks:
            return
        full_audio = np.concatenate(buffer_chunks)
        duration_s = len(full_audio) / 16000.0

        # Discard spurious noise < 0.3s
        if duration_s < 0.3:
            return

        # Direct JA -> EN translation
        result = self.stt.transcribe(full_audio, language="ja", task="translate")
        if result.get("is_mock"):
            print("[InboundPipeline] STT returned mock output. Caption rejected.")
            return

        text = result.get("text", "").strip()

        if text and self.on_caption:
            timestamp = time.time()
            self.on_caption(text, timestamp)
