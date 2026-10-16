# DECISIONS.md — Architecture & Implementation Decisions Log

Every technical decision, dependency selection, architectural trade-off, or deviation from `SPEC.md` must be recorded in this log with the date, context, decision, and rationale.

---

| Date | ID | Topic | Decision | Rationale | Deviation from SPEC? |
|---|---|---|---|---|---|
| 2026-10-13 | D-001 | Settings scope | Limit settings to defined, testable options; identify settings requiring restart. | Avoid promising live reconfiguration for stateful audio/model components. | No (from SPEC §12) |
| 2026-10-13 | D-002 | GUI Framework | Use Tkinter/ttk as the initial GUI candidate; require a prototype gate before considering alternatives. | Avoids PySide6's LGPLv3/GPLv3 license complications; strictly honors permissive-first policy. | No (from SPEC §12) |
| 2026-10-13 | D-003 | English TTS Candidate | Exclude Piper by default until artifact-level license verification; OHF-Voice/piper1-gpl is GPL-3.0. | Avoids viral copyleft licenses under permissive-first policy. | No (from SPEC §12) |
| 2026-10-13 | D-004 | VOICEVOX Candidate | Do not select VOICEVOX by default without explicit owner approval. | VOICEVOX engine is LGPLv3 and voices carry individual character licensing terms. | No (from SPEC §12) |
| 2026-10-13 | D-005 | Japanese TTS License Gate | Make exact permissively licensed Japanese voice/model identification a mandatory M0 gate. | Local Japanese TTS is required for outbound MVP, but cannot violate license policy. | No (from SPEC §12) |
| 2026-10-13 | D-006 | Machine Translation Engine | Select Argos Translate for initial evaluation; prohibit pivot translation unless explicitly tested/documented. | Offline simplicity, MIT/CC0 code; direct package availability and quality remain gates. | No (from SPEC §12) |
| 2026-10-13 | D-007 | STT Model Selection | Start with `faster-whisper` small/int8 candidate on CPU before evaluating base. | CPU capability and concurrency on i7-8750H must be empirically benchmarked. | No (from SPEC §12) |
| 2026-10-13 | D-008 | VAD Integration | Treat Silero VAD (ONNX) as an experimental speech-gating candidate, not guaranteed speedup. | False cuts and latency overhead must be measured against direct STT. | No (from SPEC §12) |
| 2026-10-13 | D-009 | Cloud API Architecture | Optional Gemini mode, strictly opt-in, disabled by default, no automatic silent fallback. | Protects user privacy, avoids unexpected billing or free-tier data sharing with Google. | No (from SPEC §12) |
| 2026-10-13 | D-010 | Single Engine Mode | MVP supports Local or Cloud (opt-in); mixed per-stage mode deferred. | Simplifies failure recovery, privacy boundaries, and testing. | No (from SPEC §12) |
| 2026-10-13 | D-011 | Cloud Error Handling | Fail visibly on cloud quota/auth failure; only fall back to local if user explicitly toggled it and local models are ready. | Prevents silent audio loss or silent privacy boundary shifts. | No (from SPEC §12) |
| 2026-10-13 | D-012 | Inbound Output Default | Default inbound output to captions only; English TTS is opt-in. | Keeps initial pipeline lightweight and avoids loading unnecessary models onto CPU. | No (from SPEC §12) |
| 2026-10-13 | D-013 | Output Volume Default | Default translated audio volume to 80% (configurable 0-100%). | Prevents hearing damage from loud synthesized audio without modifying original Zoom volume. | No (from SPEC §12) |
| 2026-10-13 | D-014 | Per-app Audio & Ducking | Defer per-application volume control and auto-ducking beyond MVP. | Avoids brittle low-level Windows audio session hooks not essential for MVP. | No (from SPEC §12) |
| 2026-10-13 | D-015 | Cable Audio Mixing | Do not mix raw English into VB-CABLE during MVP. | Eliminates acoustic leakage and echo back into the meeting. | No (from SPEC §12) |
| 2026-10-13 | D-016 | Echo / Feedback Defense | Primary defense is explicit device separation (Headphones + CABLE Input). Suppression window is secondary defense. | Timing windows alone cannot prevent acoustic feedback. | No (from SPEC §12) |
| 2026-10-13 | D-017 | Chunking & Partials | Start with sentence-level finalized output; defer partial streaming until stability is proven. | Prevents unstable hypothesis flicker and duplicate TTS synthesis. | No (from SPEC §12) |
| 2026-10-13 | D-018 | Staged Milestone Gates | Establish M0 discovery/license prototype before implementing full app skeleton. | High-risk items (audio routing and Japanese TTS license) must be verified first. | No (from SPEC §12) |
| 2026-10-13 | D-019 | Quality Presets | Presets (Light/Balanced/Quality) map strictly to benchmarked model/thread configs. | Names must reflect measured performance rather than marketing terms. | No (from SPEC §12) |
| 2026-10-13 | D-020 | Measurement Protocol | Mandatory empirical measurement protocol (median, p95, CPU %, RAM MB, thermal state). | No benchmark claims permitted without real hardware measurement data. | No (from SPEC §12) |
| 2026-10-13 | D-021 | Model Management | Explicit user download workflow with progress, sha256 checksums, and license display. | Keeps installation transparent and avoids unexpected background network usage. | No (from SPEC §12) |
| 2026-10-13 | D-022 | Driver Installation | VB-CABLE is installed manually by the user from official website; app never bundles or auto-installs. | Complies with VB-Audio licensing terms and prevents unexpected driver crashes. | No (from SPEC §12) |
| 2026-10-13 | D-023 | Outbound Trigger | Push-to-Talk (PTT) with global hotkey is primary MVP outbound mode; VAD always-on is secondary. | Eliminates accidental transmission of background noise or private speech to meeting. | No (from SPEC §12) |
| 2026-10-13 | D-024 | Benchmark Reporting | Benchmarks table in documentation must contain only empirically measured data. | Prevents misleading portfolio/performance claims. | No (from SPEC §12) |
| 2026-10-13 | D-025 | Laptop Power Safety | Mandatory benchmarking on AC power only; document sudden shutdown behavior as hardware risk. | Prevents battery cutoff and thermal throttling distortions during tests. | No (from SPEC §12) |
| 2026-10-13 | D-026 | Audio Capture Candidate | Select `PyAudioWPatch` (MIT) as primary WASAPI loopback capture candidate; evaluate `SoundCard` (BSD) as fallback. | PyAudioWPatch provides direct Windows WASAPI loopback support, endpoint enumeration, and device notification hooks. | No |
| 2026-10-13 | D-027 | Secret Storage | Store Gemini API keys via `keyring` (Windows Credential Manager / DPAPI), never in plaintext JSON or `.env`. | Adheres strictly to security and anti-credential-leakage rules. | No |
