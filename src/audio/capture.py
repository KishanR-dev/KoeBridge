"""
KoeBridge for Zoom — Thread-Safe Non-Blocking Audio Capture
"""

import threading
import queue
from typing import Optional
import numpy as np


class AudioCaptureStream:
    """
    Manages non-blocking audio capture into a thread-safe bounded queue.
    """

    def __init__(
        self,
        device_index: Optional[int] = None,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 480,  # 30ms at 16kHz
        is_loopback: bool = False,
        queue_maxsize: int = 1000,
    ):
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.is_loopback = is_loopback
        self.audio_queue: queue.Queue = queue.Queue(maxsize=queue_maxsize)
        self.is_running = False
        self._pa = None
        self._stream = None
        self._lock = threading.Lock()

    def start(self) -> bool:
        with self._lock:
            if self.is_running:
                return True

            try:
                import pyaudiowpatch as pyaudio
            except ImportError:
                try:
                    import pyaudio
                except ImportError:
                    print(
                        "[AudioCapture] PyAudio / PyAudioWPatch not installed. Operating in mock/test mode."
                    )
                    self.is_running = True
                    return False

            try:
                self._pa = pyaudio.PyAudio()

                # Determine device index and device info
                dev_idx = self.device_index
                dev_info = None

                if dev_idx is not None:
                    try:
                        dev_info = self._pa.get_device_info_by_index(dev_idx)
                    except Exception:
                        pass
                elif self.is_loopback:
                    try:
                        if hasattr(pyaudio, "paWASAPI"):
                            wasapi_info = self._pa.get_host_api_info_by_type(
                                pyaudio.paWASAPI
                            )
                            default_speakers = self._pa.get_device_info_by_index(
                                wasapi_info["defaultOutputDevice"]
                            )
                            if hasattr(self._pa, "get_loopback_device_info_generator"):
                                for (
                                    loopback
                                ) in self._pa.get_loopback_device_info_generator():
                                    if default_speakers.get("name", "") in loopback.get(
                                        "name", ""
                                    ):
                                        dev_info = loopback
                                        dev_idx = loopback["index"]
                                        break
                                if dev_info is None:
                                    for (
                                        loopback
                                    ) in self._pa.get_loopback_device_info_generator():
                                        dev_info = loopback
                                        dev_idx = loopback["index"]
                                        break
                    except Exception as e:
                        print(f"[AudioCapture] Could not auto-detect loopback: {e}")

                # Configure stream format: WASAPI loopback requires device native sample rate and channels
                stream_channels = self.channels
                stream_rate = self.sample_rate

                if self.is_loopback and dev_info is not None:
                    hw_channels = int(dev_info.get("maxInputChannels", 0))
                    hw_rate = int(dev_info.get("defaultSampleRate", 0))
                    if hw_channels > 0:
                        stream_channels = hw_channels
                    if hw_rate > 0:
                        stream_rate = hw_rate
                elif dev_info is not None:
                    hw_channels = int(dev_info.get("maxInputChannels", 0))
                    if 0 < hw_channels < stream_channels:
                        stream_channels = hw_channels

                frames_per_buffer = (
                    int(stream_rate * (self.chunk_size / self.sample_rate))
                    if self.sample_rate > 0
                    else self.chunk_size
                )

                def _callback(in_data, frame_count, time_info, status):
                    if in_data and self.is_running:
                        try:
                            # Convert raw bytes to float32 normalized [-1.0, 1.0]
                            audio_np = (
                                np.frombuffer(in_data, dtype=np.int16).astype(
                                    np.float32
                                )
                                / 32768.0
                            )
                            if stream_channels > 1:
                                audio_np = audio_np.reshape(-1, stream_channels).mean(
                                    axis=1
                                )

                            # Downsample to target sample_rate if needed (e.g. 48kHz -> 16kHz)
                            if stream_rate != self.sample_rate and stream_rate > 0:
                                ratio = stream_rate / self.sample_rate
                                if ratio.is_integer():
                                    audio_np = audio_np[:: int(ratio)]
                                else:
                                    target_len = int(
                                        len(audio_np) * (self.sample_rate / stream_rate)
                                    )
                                    indices = np.linspace(
                                        0, len(audio_np) - 1, target_len
                                    ).astype(int)
                                    audio_np = audio_np[indices]

                            self.audio_queue.put_nowait(audio_np)
                        except queue.Full:
                            # Discard oldest to avoid buffer lag
                            try:
                                self.audio_queue.get_nowait()
                                self.audio_queue.put_nowait(audio_np)
                            except Exception:
                                pass
                    return (None, pyaudio.paContinue)

                self._stream = self._pa.open(
                    format=pyaudio.paInt16,
                    channels=stream_channels,
                    rate=stream_rate,
                    input=True,
                    input_device_index=dev_idx,
                    frames_per_buffer=frames_per_buffer,
                    stream_callback=_callback,
                )
                self._stream.start_stream()
                self.is_running = True
                dev_name = (
                    dev_info.get("name", str(dev_idx)) if dev_info else str(dev_idx)
                )
                print(
                    f"[AudioCapture] Stream started on device {dev_name} (native: {stream_rate}Hz/{stream_channels}ch -> target: {self.sample_rate}Hz/1ch)"
                )
                return True
            except Exception as e:
                print(f"[AudioCapture] Failed to open audio stream: {e}")
                self.stop()
                return False

    def stop(self) -> None:
        with self._lock:
            self.is_running = False
            if self._stream:
                try:
                    self._stream.stop_stream()
                    self._stream.close()
                except Exception:
                    pass
                self._stream = None
            if self._pa:
                try:
                    self._pa.terminate()
                except Exception:
                    pass
                self._pa = None

    def get_chunk(self, timeout: float = 0.1) -> Optional[np.ndarray]:
        """Fetch next audio chunk from queue."""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def clear(self) -> None:
        """Purge all buffered frames."""
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except Exception:
                break
