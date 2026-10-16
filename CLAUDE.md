# CLAUDE.md — KoeBridge for Zoom

## Project Overview
KoeBridge for Zoom is a local-first, personal desktop real-time Japanese ↔ English meeting translator for Windows 10/11 x64, designed for Zoom web meetings joined in Chrome/Edge. It captures browser audio via WASAPI loopback, performs local speech recognition and translation, presents English captions, and injects translated Japanese speech into Zoom via VB-CABLE with global push-to-talk.

**Source of Truth:** All architecture, constraints, license gates, and milestone definitions are governed strictly by `SPEC.md`. Follow `SPEC.md` over any external assumption.

## Key Constraints & Policies
- **License Target:** MIT for project-owned code. Dependencies and model assets must be permissively licensed (MIT / Apache 2.0 / BSD). Copyleft (GPL, AGPL), LGPL, or restrictive/non-commercial licenses require explicit owner approval.
- **Privacy & Local-First:** In Local mode, zero audio or transcript data leaves the machine. No background telemetry or silent cloud fallback. Model downloads are explicit setup actions.
- **Audio Routing:** Captures via Windows WASAPI loopback. Injects outbound Japanese speech into VB-CABLE Input (which Zoom sees as CABLE Output mic). Never bundle or auto-install drivers; VB-CABLE is installed separately by the user.
- **No Invented Metrics:** Never claim real-time, low-CPU, or latency benchmarks without empirical measurements recorded on the target hardware (Intel Core i7-8750H, 32 GB RAM, plugged-in).
- **Decisions Log:** Any implementation decision, trade-off, or deviation from `SPEC.md` must be logged in `DECISIONS.md` with a date and rationale.

## Technology Stack
- **Language / Runtime:** Python 3.13 (or pinned Windows-compatible version)
- **GUI:** Tkinter / ttk (standard library, permissive Tcl/Tk license)
- **Audio I/O:** Windows WASAPI via `PyAudioWPatch` (PortAudio WASAPI loopback fork, MIT) / `SoundCard`
- **VAD:** Silero VAD (ONNX Runtime, MIT)
- **STT:** `faster-whisper` (CTranslate2, MIT) with quantized `int8` models
- **MT:** `argostranslate` (OpenNMT / CTranslate2, MIT) direct JA↔EN or local approved models
- **Japanese TTS:** Local engine with verified permissively licensed voice (Hard Gate in M0)
- **Cloud (Optional):** Google Gemini API via official SDK/REST (disabled by default, explicit opt-in, API key stored in Windows Credential Manager via `keyring`)

## Project Workflow & Conventions
- **One Milestone at a Time:** Deliver strictly by milestones defined in `SPEC.md` (M0 through M7). Do not skip ahead. Keep the application runnable after every milestone.
- **Git Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `perf:`, `chore:`).
- **Code Quality:**
  - Formatting & Linting: `ruff check .` and `ruff format .`
  - Type Checking: `mypy` or `pyright`
  - Testing: `pytest` with mocked audio devices and mocked engine interfaces
- **Safe Handling:** Never commit secrets, API keys, private meeting transcripts, or captured raw audio.
- **Milestone Reporting:** Conclude each milestone report with the mandatory template:
  ```
  MILESTONE: <id and name>
  DONE: <bullets>
  HOW TO TEST: <steps>
  MEASURED: <latency/CPU/RAM with machine details, or "not measured">
  DEVIATIONS FROM SPEC: <bullets or none>
  KNOWN ISSUES: <bullets>
  NEXT: <proposed next milestone>
  ```
