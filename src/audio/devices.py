"""
KoeBridge for Zoom — Windows Audio Endpoint Enumeration
"""

from dataclasses import dataclass
from typing import List, Optional
import ctypes
from ctypes import wintypes


@dataclass
class AudioDeviceInfo:
    index: int
    name: str
    max_input_channels: int
    max_output_channels: int
    default_sample_rate: int
    is_loopback: bool = False
    is_cable: bool = False


def enumerate_pyaudio_devices() -> List[AudioDeviceInfo]:
    """Enumerate devices using PyAudio or PyAudioWPatch if available."""
    devices = []
    try:
        import pyaudiowpatch as pyaudio
    except ImportError:
        try:
            import pyaudio
        except ImportError:
            return devices

    p = pyaudio.PyAudio()
    try:
        device_count = p.get_device_count()
        for i in range(device_count):
            try:
                info = p.get_device_info_by_index(i)
                name = str(info.get("name", f"Device {i}"))
                in_ch = int(info.get("maxInputChannels", 0))
                out_ch = int(info.get("maxOutputChannels", 0))
                rate = int(info.get("defaultSampleRate", 44100))
                is_loopback = bool(info.get("isLoopbackDevice", False))
                is_cable = "cable" in name.lower() or "vb-audio" in name.lower()

                devices.append(
                    AudioDeviceInfo(
                        index=i,
                        name=name,
                        max_input_channels=in_ch,
                        max_output_channels=out_ch,
                        default_sample_rate=rate,
                        is_loopback=is_loopback,
                        is_cable=is_cable,
                    )
                )
            except Exception:
                continue
    finally:
        p.terminate()

    return devices


def enumerate_winmm_devices() -> List[AudioDeviceInfo]:
    """Fallback device enumeration using Windows WinMM API (always available)."""
    devices = []
    try:

        class WAVEINCAPSW(ctypes.Structure):
            _fields_ = [
                ("wMid", wintypes.WORD),
                ("wPid", wintypes.WORD),
                ("vDriverVersion", wintypes.UINT),
                ("szPname", wintypes.WCHAR * 32),
                ("dwFormats", wintypes.DWORD),
                ("wChannels", wintypes.WORD),
                ("wReserved1", wintypes.WORD),
            ]

        class WAVEOUTCAPSW(ctypes.Structure):
            _fields_ = [
                ("wMid", wintypes.WORD),
                ("wPid", wintypes.WORD),
                ("vDriverVersion", wintypes.UINT),
                ("szPname", wintypes.WCHAR * 32),
                ("dwFormats", wintypes.DWORD),
                ("wChannels", wintypes.WORD),
                ("wReserved1", wintypes.WORD),
                ("dwSupport", wintypes.DWORD),
            ]

        num_in = ctypes.windll.winmm.waveInGetNumDevs()
        wic = WAVEINCAPSW()
        for i in range(num_in):
            if (
                ctypes.windll.winmm.waveInGetDevCapsW(
                    i, ctypes.byref(wic), ctypes.sizeof(wic)
                )
                == 0
            ):
                name = wic.szPname
                devices.append(
                    AudioDeviceInfo(
                        index=i,
                        name=name,
                        max_input_channels=wic.wChannels,
                        max_output_channels=0,
                        default_sample_rate=44100,
                        is_loopback=False,
                        is_cable="cable" in name.lower(),
                    )
                )

        num_out = ctypes.windll.winmm.waveOutGetNumDevs()
        woc = WAVEOUTCAPSW()
        for i in range(num_out):
            if (
                ctypes.windll.winmm.waveOutGetDevCapsW(
                    i, ctypes.byref(woc), ctypes.sizeof(woc)
                )
                == 0
            ):
                name = woc.szPname
                devices.append(
                    AudioDeviceInfo(
                        index=1000 + i,  # Offset to distinguish playback
                        name=name,
                        max_input_channels=0,
                        max_output_channels=woc.wChannels,
                        default_sample_rate=44100,
                        is_loopback=False,
                        is_cable="cable" in name.lower(),
                    )
                )
    except Exception as e:
        print(f"[AudioDevices] Error querying WinMM: {e}")

    return devices


def get_audio_devices() -> List[AudioDeviceInfo]:
    """Get all available audio endpoints."""
    devs = enumerate_pyaudio_devices()
    if not devs:
        devs = enumerate_winmm_devices()
    return devs


def find_default_loopback_device(
    devices: List[AudioDeviceInfo],
) -> Optional[AudioDeviceInfo]:
    """Find the default WASAPI loopback device."""
    for d in devices:
        if d.is_loopback:
            return d
    # If not explicitly marked as loopback, look for common default names
    for d in devices:
        if "loopback" in d.name.lower() or "stereo mix" in d.name.lower():
            return d
    return None


def find_cable_input_device(
    devices: List[AudioDeviceInfo],
) -> Optional[AudioDeviceInfo]:
    """Find VB-CABLE Input (playback device into which we inject Japanese speech)."""
    for d in devices:
        if (
            d.is_cable
            and d.max_output_channels > 0
            and ("input" in d.name.lower() or "cable" in d.name.lower())
        ):
            return d
    return None


def find_microphone_device(devices: List[AudioDeviceInfo]) -> Optional[AudioDeviceInfo]:
    """Find physical microphone (excluding VB-CABLE Output)."""
    for d in devices:
        if d.max_input_channels > 0 and not d.is_cable and not d.is_loopback:
            return d
    return None
