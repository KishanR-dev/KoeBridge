"""
KoeBridge for Zoom — Outbound Pipeline (PTT Mic EN -> MT JA -> Local TTS -> VB-CABLE Input)
"""

import threading
import time
from typing import Callable, Optional, Dict, Any
import numpy as np

from ..audio.capture import AudioCaptureStream
from ..audio.output import AudioOutputRenderer
from ..stt.engine import SttEngine
from ..mt.engine import MachineTranslationEngine
from ..tts.engine import LocalJapaneseTtsEngine


class OutboundPipeline:
    """
    Outbound Pipeline:
    When user holds PTT, records English speech from microphone.
    When user releases PTT:
      1. Transcribes English audio with Whisper
      2. Translates English text to Japanese with ArgosTranslate
      3. Synthesizes Japanese speech with LocalJapaneseTtsEngine
      4. Injects Japanese speech into VB-CABLE Input for Zoom meeting participants
    """

    def __init__(
        self,
        microphone_device_id: Optional[int] = None,
        cable_input_device_id: Optional[int] = None,
        stt_model_size: str = "tiny",
        on_status: Optional[Callable[[str, Dict[str, Any]], None]] = None,
    ):
        self.microphone_device_id = microphone_device_id
        self.cable_input_device_id = cable_input_device_id
        self.on_status = on_status

        self.capture = AudioCaptureStream(
            device_index=microphone_device_id,
            sample_rate=16000,
            channels=1,
            is_loopback=False,
        )
        self.output_renderer = AudioOutputRenderer(device_index=cable_input_device_id)
        self.stt = SttEngine(model_size=stt_model_size)
        self.mt = MachineTranslationEngine(from_code="en", to_code="ja")
        self.tts = LocalJapaneseTtsEngine()

        self._is_recording = False
        self._record_buffer = []
        self._lock = threading.Lock()

    def start(self) -> bool:
        return self.capture.start()

    def stop(self) -> None:
        self.capture.stop()

    def ptt_press(self) -> None:
        """Called when PTT key or button is pressed."""
        with self._lock:
            if self._is_recording:
                return  # Prevent duplicate recording workers
            self._is_recording = True
            self._record_buffer = []
            self.capture.clear()
            if self.on_status:
                self.on_status("RECORDING", {"message": "Recording English speech..."})

            # Start background reader thread for recording
            threading.Thread(target=self._record_worker, daemon=True).start()

    def ptt_release(self) -> None:
        """Called when PTT key or button is released."""
        with self._lock:
            if not self._is_recording:
                return
            self._is_recording = False

        if self.on_status:
            self.on_status(
                "PROCESSING", {"message": "Translating and synthesizing speech..."}
            )

        # Process in background thread to keep UI responsive
        threading.Thread(target=self._process_recorded_speech, daemon=True).start()

    def ptt_cancel(self, message: str = "PTT recording cancelled.") -> None:
        """Called to abort an active PTT recording without processing or injecting speech."""
        with self._lock:
            if not self._is_recording:
                return
            self._is_recording = False
            self._record_buffer = []
            self.capture.clear()

        if self.on_status:
            self.on_status("IDLE", {"message": message})

    def _record_worker(self) -> None:
        while self._is_recording:
            chunk = self.capture.get_chunk(timeout=0.05)
            if chunk is not None:
                with self._lock:
                    if self._is_recording:
                        self._record_buffer.append(chunk)

    def _process_recorded_speech(self) -> None:
        with self._lock:
            if not self._record_buffer:
                if self.on_status:
                    self.on_status("IDLE", {"message": "No speech detected."})
                return
            audio_data = np.concatenate(self._record_buffer)
            self._record_buffer = []

        duration_s = len(audio_data) / 16000.0
        if duration_s < 0.2:
            if self.on_status:
                self.on_status("IDLE", {"message": "Utterance too short."})
            return

        # 1. Transcribe English
        t0 = time.perf_counter()
        stt_res = self.stt.transcribe(
            audio_data,
            language="en",
            task="transcribe",
            initial_prompt="English business meeting conversation: Greetings, screen sharing, questions, discussion.",
            vad_filter=False,
        )
        if stt_res.get("is_mock"):
            if self.on_status:
                self.on_status(
                    "FAILED",
                    {
                        "message": "Outbound STT Failed: Real Whisper STT model unavailable (mock rejected)."
                    },
                )
            return

        en_text = stt_res.get("text", "").strip()

        if not en_text:
            if self.on_status:
                self.on_status("IDLE", {"message": "No English speech recognized."})
            return

        # 2. Translate EN -> JA
        t1 = time.perf_counter()
        mt_res = self.mt.translate(en_text)
        if mt_res.get("is_mock"):
            if self.on_status:
                self.on_status(
                    "FAILED",
                    {
                        "message": "Outbound MT Failed: Real Argos MT model unavailable (mock rejected).",
                        "en_text": en_text,
                    },
                )
            return

        ja_text = mt_res.get("translated_text", "").strip()
        if not ja_text:
            if self.on_status:
                self.on_status("IDLE", {"message": "No translation produced."})
            return

        # 3. Synthesize Japanese TTS
        t2 = time.perf_counter()
        tts_res = self.tts.synthesize(ja_text)
        if tts_res.get("is_mock"):
            if self.on_status:
                self.on_status(
                    "FAILED",
                    {
                        "message": "Outbound TTS Failed: Real Japanese TTS model unavailable (mock rejected).",
                        "en_text": en_text,
                        "ja_text": ja_text,
                    },
                )
            return

        ja_audio = tts_res.get("audio")
        sr = tts_res.get("sample_rate", 44100)

        # 4. Inject into VB-CABLE Input
        t3 = time.perf_counter()
        if ja_audio is not None and len(ja_audio) > 0:
            self.output_renderer.play_audio(ja_audio, sample_rate=sr)

        t4 = time.perf_counter()
        total_time_ms = (t4 - t0) * 1000.0

        if self.on_status:
            self.on_status(
                "INJECTED",
                {
                    "en_text": en_text,
                    "ja_text": ja_text,
                    "stt_ms": (t1 - t0) * 1000.0,
                    "mt_ms": (t2 - t1) * 1000.0,
                    "tts_ms": (t3 - t2) * 1000.0,
                    "inject_ms": (t4 - t3) * 1000.0,
                    "total_time_ms": total_time_ms,
                    "message": f"Injected into Zoom: '{ja_text}' ({total_time_ms:.0f} ms)",
                },
            )
