# KoeBridge

**Local-First Real-Time Japanese ↔ English Meeting Translator for Windows**

KoeBridge is a personal desktop real-time meeting translator designed for Windows 10/11 x64. It translates spoken Japanese from web meetings into English captions, and translates spoken English into natural Japanese speech injected directly into your meeting's microphone input.

KoeBridge operates **100% offline in Local Mode**: zero audio, transcripts, or telemetry are transmitted over the network.

> **Status — Post-Audit / Live Zoom Acceptance Pending (v0.1.1):** Core speech recognition, machine translation, speech synthesis, and push-to-talk state machine safeguards have been verified in local automated unit and acceptance test suites. **Initial real-world live Zoom meeting testing exposed significant defects** in overlay placement/click-blocking, speech transcription/VAD truncation, and translation hallucinations. While technical repairs and hallucination safety filters have now been implemented in the codebase and verified through automated test suites, **formal post-repair live Zoom meeting acceptance has not yet been conducted and remains pending.** Compatibility with other meeting platforms (Microsoft Teams, Google Meet, Webex) has not been verified.

---

## Architecture & Features

```
[ INBOUND PIPELINE: Japanese Meeting Audio -> English Captions ]
Zoom/Browser Web Audio
       │
       ▼ (WASAPI Loopback Capture via PyAudioWPatch)
Audio Inbound RingBuffer (16 kHz Mono)
       │
       ▼ (faster-whisper tiny int8 - Direct JA -> EN Translation)
English Text Captions
       │
       ▼
Tkinter Desktop Caption Overlay (Semi-transparent, Always-on-Top)


[ OUTBOUND PIPELINE: English Speech -> Japanese Meeting Audio ]
User Physical Microphone
       │
       ▼ (Microphone Capture via PyAudioWPatch, guarded by PTT State Machine)
Recorded English Audio Buffer
       │
       ▼ (faster-whisper tiny int8 - English Transcription)
English Text
       │
       ▼ (argostranslate - EN -> JA Neural Machine Translation)
Japanese Text
       │
       ▼ (sherpa-onnx MeloTTS-JA - Local Japanese ONNX Synthesis)
Synthesized Japanese Audio (44.1 kHz / 16 kHz Float32)
       │
       ▼ (Audio Output Renderer via PyAudioWPatch)
CABLE Input (VB-Audio Virtual Cable) -> Zoom Audio Input (CABLE Output)
```

### 1. Inbound Pipeline (Japanese → English Captions)
- **Audio Capture:** Windows WASAPI loopback capture using `PyAudioWPatch` captures browser audio from Zoom meetings without requiring Zoom SDKs, APIs, or browser extensions. Energy VAD threshold calibrated to `0.005` to capture low-amplitude conversational speech.
- **Dual-Track Transcription & Translation:** Local `faster-whisper` (`tiny` quantized int8) performs both Japanese speech transcription (`task="transcribe"`) and English translation (`task="translate"`).
- **Prompt Conditioning & Hallucination Filtering:** Applies domain meeting prompt context and conversational normalization to eliminate Whisper `tiny` translation head hallucinations on short conversational greetings.
- **Caption Presentation:** Displays real-time captions in both the main application log and a floating, translucent overlay. The overlay supports dynamic screen positioning, size bounding, focus protection (`WS_EX_NOACTIVATE`), and non-blocking click-through (`WS_EX_TRANSPARENT`).

### 2. Outbound Pipeline (English → Japanese Speech Injection)
- **Speech Recognition:** Captures user English speech via microphone with prompt-conditioned `faster-whisper`.
- **Conversational Machine Translation:** Combines local `argostranslate` neural translation with a domain-specific conversational meeting phrase dictionary and hallucination filtering, preventing web scrape artifacts ("お問い合わせ", website boilerplate).
- **Japanese Speech Synthesis:** Synthesizes Japanese speech locally using quantized MeloTTS Japanese ONNX model weights with punctuation-based pause insertion (`、`, `？`) and duration variance tuning (`length_scale = 0.95`, `noise_scale_w = 0.85`). Speech synthesis provides deterministic timing and tone adjustments; expressive emotional prosody is not claimed without empirical perceptual evaluation.
- **Virtual Audio Routing:** Transmits synthesized Japanese speech into `CABLE Input (VB-Audio Virtual Cable)`, which the Zoom web client detects as its microphone input (`CABLE Output`). Alternatively routes to physical speakers for local testing.

### 3. Push-to-Talk (PTT) Reliability State Machine
- **Hold-to-Speak:** Triggered by mouse hold on the PTT button or pressing the Spacebar when the window is focused.
- **Typematic Auto-Repeat Debounce:** Prevents duplicate worker thread creation from rapid keyboard auto-repeat events.
- **Focus Guarding:** Spacebar does not accidentally trigger PTT when interacting with child widgets (combobox dropdowns, text log, or other buttons).
- **Safety Cancellation:** If the window loses OS focus (`<FocusOut>`) or the user presses `Escape` (`<KeyPress-Escape>`), recording is immediately cancelled, buffers are purged, and zero speech is processed or injected.

---

## Prerequisites & Environment

- **Operating System:** Windows 10 / Windows 11 (64-bit).
- **Python Version:** Python 3.13 x64 (verified on Python 3.13.15 AMD64).
- **Hardware Target:** Multi-core x64 CPU (tested on Intel Core i7-8750H with 32 GB RAM).
- **Power Configuration:** Recommended plugged into AC power during inference to avoid CPU thermal throttling or battery safety cutoff.
- **Audio Drivers (Optional for Zoom injection):** [VB-CABLE Driver](https://vb-audio.com/Cable/) by VB-Audio. Must be installed manually from the official vendor website.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/KishanR-dev/KoeBridge.git
cd KoeBridge
```

### 2. Set Up Python Environment
Create and activate a virtual environment:
```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 3. Verify Hardware & Audio Endpoints
Run the environment probe to inspect available audio devices, AC power status, and installed voices:
```powershell
python probe_env.py
```
*(Optionally run `run_probe.bat` on Windows).*

### 4. Install Dependencies
Install the required prebuilt binary packages:
```powershell
# Install audio capture and Whisper inference backends
python install_stage1.py

# Install machine translation and TTS runtime backends
pip install argostranslate sherpa-onnx
```

### 5. Download Required Local Models
All models run completely locally. Download the verified model assets using the included scripts:

```powershell
# 1. Download and register the Argos English-to-Japanese translation package (~120 MB)
python install_argos_en_ja.py

# 2. Download Japanese MeloTTS ONNX assets to models/tts_melotts_ja/ (~130 MB)
python download_melotts_ja.py
```

*Note: Faster-Whisper `tiny` models are automatically retrieved by the library on first launch and cached in your local user directory (`~/.cache/huggingface/hub/`).*

---

## Running the Application

Launch the desktop GUI:
```powershell
python src/main.py
```

### Windows Audio Device Configuration

1. **Inbound Setup (Listening to Zoom):**
   - Ensure Zoom or your web browser is playing audio through your primary speakers or headphones.
   - In KoeBridge, select that device from the **Loopback Device (Inbound)** dropdown.
   - Click **Start Inbound Translation**. The live caption feed will begin processing audio.

2. **Outbound Setup (Speaking Japanese into Zoom):**
   - Select your physical microphone under **Microphone (Outbound)**.
   - Select **CABLE Input (VB-Audio Virtual Cable)** under **Output Device (Outbound)**. *(Select physical speakers if you want to preview the Japanese audio locally first).*
   - In Zoom's Audio Settings, select **CABLE Output (VB-Audio Virtual Cable)** as your microphone.

3. **Operating Push-to-Talk (PTT):**
   - Click and hold **🎙 HOLD TO SPEAK ENGLISH (PTT)** or hold `Spacebar` while the application window is active.
   - The indicator turns red: `🔴 RECORDING ENGLISH...`. Speak your message in English.
   - Release the button or Spacebar to translate and synthesize. The status will display `PROCESSING` and then `INJECTED` once the Japanese audio is transmitted.
   - To abort recording without translating or transmitting, press `Escape` or switch windows (`Alt+Tab`).

4. **Caption Overlay & Click-Through Mode:**
   - Click **Show/Hide Overlay Window** to open the floating, semi-transparent caption bar. It automatically positions itself centered near the bottom of your screen work area.
   - Click **Click-Through: OFF (Draggable)** to toggle click-through mode:
     - **OFF (Draggable):** You can freely click and drag the caption window to your preferred screen location.
     - **ON (Pass Clicks to Zoom):** Enables Windows `WS_EX_TRANSPARENT`. All mouse clicks pass directly through the overlay to Zoom or applications beneath it without trapping input.
   - Dual-line captions display both the recognized Japanese speech (`[JA]`) in amber and the English translation (`[EN]`) in cyan. Focus protection (`WS_EX_NOACTIVATE`) prevents incoming captions from interrupting your active meeting or taking typing focus away.

---

## Running Tests

KoeBridge includes unit, integration, and GUI acceptance test suites:

```powershell
# Run all unit and integration tests (22 tests)
python run_tests.py
# Or run directly with pytest:
pytest tests -v

# Run the dedicated PTT reliability and state-machine regression suite (8 tests)
pytest tests/test_ptt_state_machine.py -v

# Run the integrated desktop GUI acceptance test suite (5 tests)
pytest test_gui_acceptance.py -v

# Run Ruff code quality checks
ruff check src tests
ruff format --check src tests
```

---

## Troubleshooting Common Issues

- **No loopback audio detected:** Ensure the target playback device is set as your default Windows sound device and actively playing audio before starting inbound translation.
- **VB-CABLE Input not listed:** Reboot Windows after installing VB-CABLE to ensure the WASAPI driver is registered.
- **Model file not found:** Verify that `python install_argos_en_ja.py` and `python download_melotts_ja.py` completed successfully without network errors.
- **Keyboard focus trapping:** If typing into text fields or selecting dropdowns, Spacebar will interact with the widget rather than activating PTT. Focus the window background or the PTT button to use Spacebar for voice.

---

## Privacy & Local-First Guarantees

- **100% Offline Processing:** In Local mode, zero audio samples, speech recordings, or translated text leave your machine.
- **Zero Background Telemetry:** KoeBridge does not collect analytics or error telemetry.
- **Local Settings Storage:** User preferences and device configurations are saved locally in `%LOCALAPPDATA%\KoeBridge\config.json`.

---

## Third-Party Components & Licenses

KoeBridge builds upon the following open-source libraries and model architectures:

| Component | Upstream Project | License | Purpose |
|---|---|---|---|
| **faster-whisper** | [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2) | MIT | Quantized local STT & direct speech translation |
| **PyAudioWPatch** | [intxcc/pyaudiowpatch](https://github.com/intxcc/pyaudiowpatch) | MIT | Windows WASAPI loopback capture & output routing |
| **Argos Translate** | [argosopentech/argos-translate](https://github.com/argosopentech/argos-translate) | MIT | Offline neural machine translation |
| **sherpa-onnx** | [k2-fsa/sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | Apache 2.0 | ONNX-based speech synthesis runtime |
| **MeloTTS-ONNX** | [MiaoMint/MeloTTS-ONNX](https://huggingface.co/MiaoMint/MeloTTS-ONNX) | MIT | Permissively licensed Japanese ONNX voice model |
| **Tkinter** | Standard Python Library | Tcl/Tk (BSD-style) | Desktop graphical interface and caption overlay |

---

## Project License Notice

**A project license has not yet been selected.** This repository is currently published for preview and evaluation purposes. No open-source reuse rights, warranties, or commercial licenses are granted at this time.
