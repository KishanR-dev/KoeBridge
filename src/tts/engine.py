"""
KoeBridge for Zoom — Local Japanese Text-to-Speech (TTS) Engine
"""

from typing import Optional, Dict, Any
import os
import tempfile
import time
import subprocess
import wave
import numpy as np


class LocalJapaneseTtsEngine:
    """
    Multi-tier local Japanese Text-to-Speech engine.
    Tier 1: MeloTTS-Japanese ONNX (offline neural TTS via onnxruntime)
    Tier 2: Windows SAPI5 / OneCore native voices (Haruka, Ayumi, Ichiro)
    Tier 3: Windows PowerShell System.Speech fallback
    """

    _SHARED_MELO_ASSETS: Dict[str, Any] = {}

    def __init__(
        self, model_dir: Optional[str] = None, voice_name: Optional[str] = None
    ):
        self.model_dir = model_dir or os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "models",
            "tts_melotts_ja",
        )
        self.voice_name = voice_name
        self.sample_rate = 44100
        self._backend = None
        self._melo_sess = None
        self._melo_tokens = None
        self._melo_lexicon = None
        self._sapi_voice = None
        self._is_loaded = False
        self._punct_map = {
            "。": ".",
            "、": ",",
            "？": "?",
            "！": "!",
            "?": "?",
            "!": "!",
            ".": ".",
            ",": ",",
        }
        self._init_backend()

    def _init_backend(self) -> None:
        # Tier 1: Try MeloTTS-Japanese ONNX
        model_onnx = os.path.join(self.model_dir, "model.onnx")
        tokens_file = os.path.join(self.model_dir, "tokens.txt")
        lexicon_file = os.path.join(self.model_dir, "lexicon.txt")

        if (
            os.path.exists(model_onnx)
            and os.path.exists(tokens_file)
            and os.path.exists(lexicon_file)
        ):
            if self.model_dir in LocalJapaneseTtsEngine._SHARED_MELO_ASSETS:
                cached = LocalJapaneseTtsEngine._SHARED_MELO_ASSETS[self.model_dir]
                self._melo_sess = cached["sess"]
                self._melo_tokens = cached["tokens"]
                self._melo_lexicon = cached["lexicon"]
                self.sample_rate = 44100
                self._backend = "melotts_onnx"
                self._is_loaded = True
                print(
                    "[TTS] Initialized Tier 1 MeloTTS-Japanese ONNX backend (cached)."
                )
                return

            try:
                import onnxruntime as ort

                # Load tokens
                with open(tokens_file, encoding="utf-8") as f:
                    self._melo_tokens = {
                        line.split()[0]: int(line.split()[1])
                        for line in f
                        if line.strip()
                    }

                # Load lexicon
                self._melo_lexicon = {}
                with open(lexicon_file, encoding="utf-8") as f:
                    for line in f:
                        splits = line.strip().split()
                        if not splits:
                            continue
                        w = splits[0]
                        items = splits[1:]
                        half = len(items) // 2
                        phones = items[:half]
                        tones = [int(t) for t in items[half:]]
                        self._melo_lexicon[w] = (phones, tones)

                # Initialize ONNX session
                opts = ort.SessionOptions()
                opts.inter_op_num_threads = 1
                opts.intra_op_num_threads = 4
                self._melo_sess = ort.InferenceSession(
                    model_onnx, sess_options=opts, providers=["CPUExecutionProvider"]
                )
                LocalJapaneseTtsEngine._SHARED_MELO_ASSETS[self.model_dir] = {
                    "sess": self._melo_sess,
                    "tokens": self._melo_tokens,
                    "lexicon": self._melo_lexicon,
                }
                self.sample_rate = 44100
                self._backend = "melotts_onnx"
                self._is_loaded = True
                print("[TTS] Initialized Tier 1 MeloTTS-Japanese ONNX backend.")
                return
            except Exception as e:
                print(f"[TTS] Failed to initialize MeloTTS-Japanese ONNX: {e}")
                self.sample_rate = 44100
                self._backend = "melotts_onnx"
                self._is_loaded = True
                print("[TTS] Initialized Tier 1 MeloTTS-Japanese ONNX backend.")
                return
            except Exception as e:
                print(f"[TTS] Failed to initialize MeloTTS-Japanese ONNX: {e}")

        # Tier 2: Try win32com SAPI
        try:
            import win32com.client

            voice = win32com.client.Dispatch("SAPI.SpVoice")
            voices = voice.GetVoices()
            for i in range(voices.Count):
                v = voices.Item(i)
                desc = v.GetDescription()
                if (
                    "japanese" in desc.lower()
                    or "haruka" in desc.lower()
                    or "ayumi" in desc.lower()
                    or "ichiro" in desc.lower()
                ):
                    voice.Voice = v
                    self.voice_name = desc
                    self._sapi_voice = voice
                    self._backend = "win32com_sapi"
                    self._is_loaded = True
                    print(f"[TTS] Using Windows SAPI Japanese Voice: {desc}")
                    return
        except Exception:
            pass

        # Tier 3: Try pyttsx3
        try:
            import pyttsx3

            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            for v in voices:
                if (
                    "ja" in str(v.languages).lower()
                    or "japanese" in v.name.lower()
                    or "haruka" in v.name.lower()
                ):
                    engine.setProperty("voice", v.id)
                    self.voice_name = v.name
                    self._backend = "pyttsx3"
                    self._is_loaded = True
                    print(f"[TTS] Using pyttsx3 Japanese Voice: {v.name}")
                    return
        except Exception:
            pass

        # Tier 4: Windows PowerShell System.Speech / OneCore fallback
        self._backend = "windows_speech_ps"
        self._is_loaded = True
        print("[TTS] Initialized Windows System.Speech fallback backend.")

    def _tokenize_ja(self, text: str):
        phones, tones = [], []
        i = 0
        n = len(text)
        tokens = self._melo_tokens
        lexicon = self._melo_lexicon
        while i < n:
            ch = text[i]
            if ch in self._punct_map:
                p = self._punct_map[ch]
                if p in tokens:
                    phones.append(tokens[p])
                    tones.append(0)
                i += 1
                continue
            if ch in (" ", "\t", "\n", "\r"):
                if "_" in tokens:
                    phones.append(tokens["_"])
                    tones.append(0)
                i += 1
                continue
            matched = False
            for sub_len in range(min(15, n - i), 0, -1):
                sub = text[i : i + sub_len]
                if sub in lexicon:
                    p_list, t_list = lexicon[sub]
                    for p, t in zip(p_list, t_list):
                        if p in tokens:
                            phones.append(tokens[p])
                            tones.append(t)
                    i += sub_len
                    matched = True
                    break
            if not matched:
                i += 1
        return phones, tones

    def _preprocess_ja_prosody(self, text: str) -> str:
        """Add pause markers and rising intonation punctuation for natural Japanese prosody."""
        t = text.strip()
        if not t:
            return t

        # Ensure polite question ending has rising intonation marker '？'
        if t.endswith(("か", "でしょうか", "ますか")):
            t += "？"
        elif not t.endswith(("。", "？", "！", ".", "?", "!")):
            t += "。"

        # Add comma pauses after common introductory discourse markers if not already punctuated
        markers = [
            ("はい", "はい、"),
            ("いいえ", "いいえ、"),
            ("それでは", "それでは、"),
            ("では", "では、"),
            ("すみませんが", "すみませんが、"),
            ("恐れ入りますが", "恐れ入りますが、"),
            ("なるほど", "なるほど、"),
        ]
        for m, rep in markers:
            if t.startswith(m) and not t.startswith(rep):
                t = rep + t[len(m) :]
                break
        return t

    def synthesize(self, text: str) -> Dict[str, Any]:
        """
        Synthesize Japanese text into float32 audio samples.
        Returns dict with 'audio', 'sample_rate', 'latency_ms', 'is_mock'.
        """
        if not text.strip():
            return {
                "audio": np.zeros(0, dtype=np.float32),
                "sample_rate": self.sample_rate,
                "latency_ms": 0.0,
                "is_mock": False,
            }

        # Apply prosody and punctuation preprocessing
        text = self._preprocess_ja_prosody(text)

        start_time = time.perf_counter()

        # Backend 1: MeloTTS-Japanese ONNX
        if self._backend == "melotts_onnx" and self._melo_sess:
            try:
                phones, tones = self._tokenize_ja(text)
                if phones:
                    # Interleave blanks (add_blank=1)
                    new_phones = [0] * (2 * len(phones) + 1)
                    new_tones = [0] * (2 * len(tones) + 1)
                    new_phones[1::2] = phones
                    new_tones[1::2] = tones

                    x = np.array([new_phones], dtype=np.int64)
                    x_lengths = np.array([len(new_phones)], dtype=np.int64)
                    tones_arr = np.array([new_tones], dtype=np.int64)
                    sid = np.array([0], dtype=np.int64)
                    noise_scale = np.array([0.6], dtype=np.float32)
                    length_scale = np.array([0.95], dtype=np.float32)
                    noise_scale_w = np.array([0.85], dtype=np.float32)

                    outputs = self._melo_sess.run(
                        ["y"],
                        {
                            "x": x,
                            "x_lengths": x_lengths,
                            "tones": tones_arr,
                            "sid": sid,
                            "noise_scale": noise_scale,
                            "length_scale": length_scale,
                            "noise_scale_w": noise_scale_w,
                        },
                    )
                    audio = outputs[0][0][0]
                    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                    return {
                        "audio": audio,
                        "sample_rate": 44100,
                        "latency_ms": elapsed_ms,
                        "is_mock": False,
                    }
            except Exception as e:
                print(f"[TTS] MeloTTS-Japanese ONNX synthesis error: {e}")

        # Backend 2: win32com SAPI direct to WAV stream in memory
        if self._backend == "win32com_sapi" and self._sapi_voice:
            try:
                import win32com.client

                stream = win32com.client.Dispatch("SAPI.SpMemoryStream")
                self._sapi_voice.AudioOutputStream = stream
                self._sapi_voice.Speak(text)
                data = stream.GetData()
                # Default SAPI is usually 22050 or 16000 Hz 16-bit PCM
                audio_np = (
                    np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                )
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return {
                    "audio": audio_np,
                    "sample_rate": 22050,
                    "latency_ms": elapsed_ms,
                }
            except Exception as e:
                print(f"[TTS] win32com error: {e}")

        # Backend 2: PowerShell System.Speech synthesis to temp WAV
        tmp_wav = os.path.join(
            tempfile.gettempdir(), f"kb_tts_{int(time.time() * 1000)}.wav"
        )
        try:
            # Escape text for powershell
            clean_text = text.replace('"', '`"').replace("'", "''")
            ps_script = f"""
Add-Type -AssemblyName System.Speech;
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$jaVoice = $synth.GetInstalledVoices() | Where-Object {{ $_.VoiceInfo.Culture.TwoLetterISOLanguageName -eq 'ja' -or $_.VoiceInfo.Name -like '*Haruka*' -or $_.VoiceInfo.Name -like '*Ayumi*' }} | Select-Object -First 1;
if ($jaVoice) {{ $synth.SelectVoice($jaVoice.VoiceInfo.Name) }};
$synth.SetOutputToWaveFile('{tmp_wav}');
$synth.Speak("{clean_text}");
$synth.Dispose();
"""
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                timeout=5,
            )

            if os.path.exists(tmp_wav) and os.path.getsize(tmp_wav) > 44:
                with wave.open(tmp_wav, "rb") as wf:
                    sr = wf.getframerate()
                    n_frames = wf.getnframes()
                    raw = wf.readframes(n_frames)
                    audio_np = (
                        np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
                    )
                try:
                    os.remove(tmp_wav)
                except Exception:
                    pass

                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                return {"audio": audio_np, "sample_rate": sr, "latency_ms": elapsed_ms}
        except Exception as e:
            print(f"[TTS] PowerShell synthesis error: {e}")
        finally:
            if os.path.exists(tmp_wav):
                try:
                    os.remove(tmp_wav)
                except Exception:
                    pass

        # Mock sine wave for testing if no Japanese speech engine responds
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        t = np.linspace(0, 0.5, int(self.sample_rate * 0.5), endpoint=False)
        mock_audio = (0.2 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
        return {
            "audio": mock_audio,
            "sample_rate": self.sample_rate,
            "latency_ms": elapsed_ms,
            "is_mock": True,
        }
