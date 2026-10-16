"""
Test script for end-to-end Outbound Pipeline verification:
English Audio -> English Whisper STT -> Argos EN-JA MT -> MeloTTS Japanese TTS -> Audio Output / WAV
"""

import os
import sys
import time
import wave
import subprocess
import numpy as np
import av

from src.stt.engine import SttEngine
from src.mt.engine import MachineTranslationEngine
from src.tts.engine import LocalJapaneseTtsEngine
from src.audio.output import AudioOutputRenderer


def generate_english_speech_wav(text: str, out_wav: str) -> bool:
    """Generate English speech audio using Windows System.Speech (David/Zira)."""
    clean_text = text.replace('"', '`"').replace("'", "''")
    ps_cmd = f"""
Add-Type -AssemblyName System.Speech;
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$synth.SetOutputToWaveFile('{out_wav}');
$synth.Speak("{clean_text}");
$synth.Dispose();
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    return os.path.exists(out_wav) and os.path.getsize(out_wav) > 44


def load_audio_16k_mono(wav_path: str) -> np.ndarray:
    """Load WAV audio and resample to float32 16kHz mono using PyAV."""
    container = av.open(wav_path)
    resampler = av.audio.resampler.AudioResampler(
        format="fltp", layout="mono", rate=16000
    )
    frames = []
    for frame in container.decode(audio=0):
        for resampled_frame in resampler.resample(frame):
            frames.append(resampled_frame.to_ndarray()[0])
    container.close()
    if frames:
        return np.concatenate(frames)
    return np.zeros(0, dtype=np.float32)


def main():
    print("=" * 60)
    print("KoeBridge Outbound Pipeline End-to-End Verification")
    print("=" * 60)

    # Step 0: Generate English speech
    en_phrase = "Thank you very much. Let us start the meeting."
    en_wav = "test_en_input.wav"
    print(f"[Step 0] Generating English speech WAV for: '{en_phrase}'...")
    generate_english_speech_wav(en_phrase, en_wav)
    print(f"Generated {en_wav} ({os.path.getsize(en_wav)} bytes)")

    # Load English audio
    audio_16k = load_audio_16k_mono(en_wav)
    duration_s = len(audio_16k) / 16000.0
    print(f"Loaded {len(audio_16k)} samples ({duration_s:.2f} s) at 16 kHz")

    # Step 1: English STT
    print("\n[Step 1] Initializing faster-whisper STT...")
    stt = SttEngine(model_size="tiny")
    t0 = time.perf_counter()
    stt_res = stt.transcribe(audio_16k, language="en", task="transcribe")
    t1 = time.perf_counter()
    stt_ms = (t1 - t0) * 1000.0
    transcribed_en = stt_res.get("text", "").strip()
    print(f"STT Result: '{transcribed_en}' in {stt_ms:.1f} ms")

    # Step 2: Argos Machine Translation (EN -> JA)
    print("\n[Step 2] Initializing Argos Translate (EN -> JA)...")
    mt = MachineTranslationEngine(from_code="en", to_code="ja")
    # Warm up
    mt.translate("Hello.")
    t2 = time.perf_counter()
    mt_res = mt.translate(transcribed_en)
    t3 = time.perf_counter()
    mt_ms = (t3 - t2) * 1000.0
    translated_ja = mt_res.get("translated_text", "").strip()
    print(f"MT Result: '{translated_ja}' in {mt_ms:.1f} ms")

    # Step 3: MeloTTS Japanese Speech Synthesis
    print("\n[Step 3] Initializing MeloTTS Japanese TTS...")
    tts = LocalJapaneseTtsEngine()
    print(f"TTS Backend: {tts._backend}, Sample Rate: {tts.sample_rate}")
    t4 = time.perf_counter()
    tts_res = tts.synthesize(translated_ja)
    t5 = time.perf_counter()
    tts_ms = (t5 - t4) * 1000.0
    ja_audio = tts_res.get("audio")
    sr = tts_res.get("sample_rate", 44100)
    rms = float(np.sqrt(np.mean(ja_audio**2))) if len(ja_audio) > 0 else 0.0
    ja_dur = len(ja_audio) / sr if sr > 0 else 0.0
    print(f"TTS Result: {len(ja_audio)} samples ({ja_dur:.2f} s, RMS: {rms:.4f}) in {tts_ms:.1f} ms")

    # Step 4: Audio Output & WAV export
    print("\n[Step 4] Exporting synthesized Japanese audio and testing playback...")
    renderer = AudioOutputRenderer()
    out_wav = "test_outbound_ja_output.wav"
    renderer.save_wav(out_wav, ja_audio, sample_rate=sr)
    print(f"Saved synthesized speech to {out_wav} ({os.path.getsize(out_wav)} bytes)")

    # Test playback to default output (physical speakers)
    t6 = time.perf_counter()
    playback_ok = renderer.play_audio(ja_audio, sample_rate=sr)
    t7 = time.perf_counter()
    inject_ms = (t7 - t6) * 1000.0
    print(f"Audio playback completed: {playback_ok} in {inject_ms:.1f} ms")

    total_pipeline_ms = stt_ms + mt_ms + tts_ms + inject_ms
    print("\n" + "=" * 60)
    print("PIPELINE PERFORMANCE SUMMARY:")
    print(f"  English STT:    {stt_ms:7.1f} ms -> '{transcribed_en}'")
    print(f"  Argos EN->JA MT:{mt_ms:7.1f} ms -> '{translated_ja}'")
    print(f"  MeloTTS JA TTS: {tts_ms:7.1f} ms -> {ja_dur:.2f}s audio (RMS {rms:.4f})")
    print(f"  Audio Output:   {inject_ms:7.1f} ms")
    print(f"  Total Latency:  {total_pipeline_ms:7.1f} ms")
    print("=" * 60)

    # Save summary report
    with open("outbound_e2e_report.txt", "w", encoding="utf-8") as f:
        f.write("OUTBOUND PIPELINE VERIFICATION REPORT\n")
        f.write(f"Input English Audio: {en_wav} ({duration_s:.2f} s)\n")
        f.write(f"Transcribed EN: {transcribed_en} ({stt_ms:.1f} ms)\n")
        f.write(f"Translated JA: {translated_ja} ({mt_ms:.1f} ms)\n")
        f.write(f"Synthesized JA Audio: {out_wav} ({ja_dur:.2f} s, RMS {rms:.4f}, {tts_ms:.1f} ms)\n")
        f.write(f"Playback Result: {playback_ok} ({inject_ms:.1f} ms)\n")
        f.write(f"Total Latency: {total_pipeline_ms:.1f} ms\n")


if __name__ == "__main__":
    main()
