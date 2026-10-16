"""
KoeBridge for Zoom — Audio Playback / Injection into VB-CABLE Input
"""

import threading
import wave
from typing import Optional
import numpy as np


class AudioOutputRenderer:
    """
    Renders synthesized audio buffers into a designated output endpoint (e.g., CABLE Input)
    or saves to a WAV file for offline testing/verification.
    """

    def __init__(self, device_index: Optional[int] = None, sample_rate: int = 24000):
        self.device_index = device_index
        self.sample_rate = sample_rate
        self._lock = threading.Lock()

    def play_audio(
        self, audio_data: np.ndarray, sample_rate: Optional[int] = None
    ) -> bool:
        """
        Play audio numpy array (float32 or int16) out through the configured device
        with automatic hardware format negotiation (sample rate and channels).
        """
        sr = sample_rate or self.sample_rate
        if len(audio_data) == 0:
            return True

        try:
            import pyaudiowpatch as pyaudio
        except ImportError:
            try:
                import pyaudio
            except ImportError:
                print(
                    f"[AudioOutput] Mock playing {len(audio_data)} samples at {sr} Hz"
                )
                return True

        with self._lock:
            p = pyaudio.PyAudio()
            try:
                dev_info = None
                dev_idx = self.device_index
                if dev_idx is not None:
                    try:
                        dev_info = p.get_device_info_by_index(dev_idx)
                    except Exception:
                        pass
                if dev_info is None:
                    try:
                        dev_info = p.get_default_output_device_info()
                        dev_idx = dev_info.get("index")
                    except Exception:
                        pass

                # Hardware format negotiation
                out_channels = 1
                out_rate = sr
                if dev_info is not None:
                    hw_channels = int(dev_info.get("maxOutputChannels", 0))
                    hw_rate = int(dev_info.get("defaultSampleRate", 0))
                    if hw_channels >= 2:
                        out_channels = 2
                    elif hw_channels == 1:
                        out_channels = 1
                    if hw_rate > 0:
                        out_rate = hw_rate

                # Convert float32 [-1.0, 1.0] to int16
                if audio_data.dtype in (np.float32, np.float64):
                    clipped = np.clip(audio_data, -1.0, 1.0)
                    int16_mono = (clipped * 32767.0).astype(np.int16)
                else:
                    int16_mono = audio_data.astype(np.int16)

                # Resample if device native rate differs from input sample rate
                if out_rate != sr and sr > 0:
                    target_len = int(len(int16_mono) * (out_rate / sr))
                    indices = np.linspace(0, len(int16_mono) - 1, target_len).astype(
                        int
                    )
                    int16_mono = int16_mono[indices]

                # Channel expansion (mono -> stereo) if required by output device
                if out_channels == 2:
                    int16_out = np.column_stack((int16_mono, int16_mono))
                else:
                    int16_out = int16_mono

                raw_bytes = int16_out.tobytes()

                stream = p.open(
                    format=pyaudio.paInt16,
                    channels=out_channels,
                    rate=out_rate,
                    output=True,
                    output_device_index=dev_idx,
                )
                try:
                    stream.write(raw_bytes)
                finally:
                    stream.stop_stream()
                    stream.close()
                return True
            except Exception as e:
                print(
                    f"[AudioOutput] Error rendering audio to device {self.device_index}: {e}"
                )
                return False
            finally:
                p.terminate()

    def save_wav(
        self, file_path: str, audio_data: np.ndarray, sample_rate: Optional[int] = None
    ) -> bool:
        """Save synthesized audio buffer directly to a 16-bit PCM WAV file."""
        sr = sample_rate or self.sample_rate
        try:
            if audio_data.dtype in (np.float32, np.float64):
                clipped = np.clip(audio_data, -1.0, 1.0)
                int16_data = (clipped * 32767.0).astype(np.int16)
            else:
                int16_data = audio_data.astype(np.int16)

            with wave.open(file_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(sr)
                wf.writeframes(int16_data.tobytes())
            return True
        except Exception as e:
            print(f"[AudioOutput] Failed to save WAV to {file_path}: {e}")
            return False
