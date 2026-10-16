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
        on_caption: Optional[Callable] = None,
        silence_timeout_s: float = 1.0,
        energy_threshold: float = 0.005,
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

    def _normalize_inbound_translation(self, ja_text: str, en_text: str) -> str:
        """
        Normalize and repair known Whisper tiny translation hallucinations on conversational
        Japanese meeting phrases (e.g. translating 'こんにちは' as 'This is the end.').
        """
        ja_clean = (
            ja_text.strip()
            .replace("。", "")
            .replace("、", "")
            .replace("？", "")
            .replace("！", "")
        )
        en_lower = en_text.lower()

        # Check common greetings
        if ja_clean in ("こんにちは", "こんにちわ", "どうもこんにちは"):
            if (
                not en_text
                or "this is" in en_lower
                or "end" in en_lower
                or "bye" in en_lower
            ):
                return "Hello."

        if any(w in ja_clean for w in ("ありがとう", "ありがとうございます", "有難う")):
            if not en_text or "thank" not in en_lower:
                return "Thank you."

        if (
            "はじめまして" in ja_clean
            or "よろしくお願" in ja_clean
            or "よろしく" in ja_clean
        ):
            if not en_text or any(
                h in en_lower for h in ["mask", "color", "talk to you a little"]
            ):
                return "Nice to meet you. Looking forward to working with you."

        if "見えますか" in ja_clean or "画面" in ja_clean:
            if not en_text or "like it" in en_lower or "talk" in en_lower:
                return "Can you see my screen?"

        if "聞こえますか" in ja_clean or "声が" in ja_clean:
            if not en_text or "think" in en_lower:
                return "Can you hear me?"

        if "わかりました" in ja_clean or "承知" in ja_clean or "了解" in ja_clean:
            if not en_text or "thank" in en_lower:
                return "Understood."

        if "質問がありま" in ja_clean:
            return "I have a question."

        if "失礼します" in ja_clean or "失礼いたします" in ja_clean:
            return "Excuse me."

        if "さようなら" in ja_clean:
            return "Goodbye."

        # Discard generic hallucination artifacts
        hallucination_phrases = [
            "this is the end",
            "thank you for watching",
            "please subscribe",
            "subtitles by",
            "transcription by",
        ]
        if any(h in en_lower for h in hallucination_phrases):
            if ja_text:
                return f"[JA: {ja_text}]"
            return ""

        return en_text

    def _process_utterance(self, buffer_chunks: list) -> None:
        if not buffer_chunks:
            return
        full_audio = np.concatenate(buffer_chunks)
        duration_s = len(full_audio) / 16000.0

        # Discard spurious noise < 0.25s
        if duration_s < 0.25:
            return

        # 1. Transcribe Japanese speech to get exact Japanese text
        ja_result = self.stt.transcribe(
            full_audio,
            language="ja",
            task="transcribe",
            initial_prompt="Japanese business meeting conversation: こんにちは、よろしくお願いします、ありがとうございます。",
            vad_filter=False,
        )
        if ja_result.get("is_mock"):
            print("[InboundPipeline] STT returned mock output. Caption rejected.")
            return

        ja_text = ja_result.get("text", "").strip()

        # 2. Direct JA -> EN translation
        en_result = self.stt.transcribe(
            full_audio,
            language="ja",
            task="translate",
            initial_prompt="Japanese meeting speech translation.",
            vad_filter=False,
        )
        en_text = en_result.get("text", "").strip()

        # Normalize and filter hallucinations
        en_text = self._normalize_inbound_translation(ja_text, en_text)

        if (en_text or ja_text) and self.on_caption:
            timestamp = time.time()
            display_en = en_text if en_text else ja_text
            try:
                import inspect

                sig = inspect.signature(self.on_caption)
                if len(sig.parameters) >= 3:
                    self.on_caption(display_en, timestamp, ja_text)
                else:
                    self.on_caption(display_en, timestamp)
            except Exception:
                try:
                    self.on_caption(display_en, timestamp, ja_text)
                except TypeError:
                    self.on_caption(display_en, timestamp)
