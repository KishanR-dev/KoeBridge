"""
Unit tests for audio device enumeration and matching
"""

from src.audio.devices import (
    AudioDeviceInfo,
    find_default_loopback_device,
    find_cable_input_device,
    find_microphone_device,
    get_audio_devices,
)


def test_device_matching_helpers():
    test_devs = [
        AudioDeviceInfo(
            index=0,
            name="Speakers (Realtek)",
            max_input_channels=0,
            max_output_channels=2,
            default_sample_rate=48000,
        ),
        AudioDeviceInfo(
            index=1,
            name="Speakers (Realtek) [Loopback]",
            max_input_channels=2,
            max_output_channels=0,
            default_sample_rate=48000,
            is_loopback=True,
        ),
        AudioDeviceInfo(
            index=2,
            name="Microphone Array",
            max_input_channels=2,
            max_output_channels=0,
            default_sample_rate=48000,
        ),
        AudioDeviceInfo(
            index=3,
            name="CABLE Input (VB-Audio Virtual Cable)",
            max_input_channels=0,
            max_output_channels=2,
            default_sample_rate=44100,
            is_cable=True,
        ),
        AudioDeviceInfo(
            index=4,
            name="CABLE Output (VB-Audio Virtual Cable)",
            max_input_channels=2,
            max_output_channels=0,
            default_sample_rate=44100,
            is_cable=True,
        ),
    ]

    loopback = find_default_loopback_device(test_devs)
    assert loopback is not None
    assert loopback.index == 1

    mic = find_microphone_device(test_devs)
    assert mic is not None
    assert mic.index == 2

    cable_in = find_cable_input_device(test_devs)
    assert cable_in is not None
    assert cable_in.index == 3


def test_device_enumeration_runs_without_error():
    devs = get_audio_devices()
    assert isinstance(devs, list)
