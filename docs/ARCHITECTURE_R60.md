# KoeBridge for Zoom — Architecture & Verification Plan (Revision 60)
**Document Identifier:** `KB-ARCH-VERIF-PLAN-R60`  
**Revision:** Revision 60 (Forensic Repair, Canonical Baseline & Release-Gate Reconstruction)  
**Recorded Specification Date:** 2026-10-13 (per literal textual date in `SPEC.md` line 4)  
**Approved Decisions Date:** 2026-10-13 (all 27 ADRs D-001 through D-027 in `DECISIONS.md` dated 2026-10-13)  
**Document Revision Date:** 14 October 2026 (grounded in host filesystem timestamp)  
**Forensic Audit Date:** 14 October 2026 (grounded in active host system calendar date)  
**Status:** PLANNING-ONLY REVIEW — PENDING EXPLICIT OWNER APPROVAL  
**Target Platform:** Microsoft Windows 10 / 11 x64 (Build 19041+)  
**Hardware Baseline:** Intel Core i7-8750H (6C/12T, 2.20 GHz base), 32 GB DDR4 RAM, Plugged-In AC Power (`ACLineStatus == 1`)  
**Authoritative Technical Specifications:** `SPEC.md` (Governing Specification), `CLAUDE.md`, `DECISIONS.md` (ADRs D-001 through D-027)  

---

## 1. Executive Status & Governance Boundary

### 1.1 Governance Summary Table

The table below reports the executive status of all governance dimensions and formal release gates. Every release gate (**G-01, G-02, G-03, G-04**) appears exactly once, fully reconciled against the detailed specifications in Section 7 and Section 9:

| Governance Dimension | Gate / Milestone Name | Current Status | Governing Authority | Mandatory Acceptance Criteria Summary | Outstanding Evidence Required to Close Gate |
|---|---|---|---|---|---|
| **Document State** | Revision 60 Specification | **REVIEWABLE SPECIFICATION** | Project Architecture Plan | Complete, untruncated artifact on disk; 33 nodes, 44 edges, 8 closed subgraphs | Owner formal review and sign-off |
| **Milestone M0** | Milestone M0 (Discovery Execution) | **STRICTLY UNAUTHORIZED** | `SPEC.md` §8; Owner Authority | Formal owner sign-off on discovery scope; isolated venv setup | Explicit project owner authorization to execute discovery |
| **Gate G-01** | Japanese TTS Engine & Voice Licensing | **EMPIRICAL GATE OPEN** | `SPEC.md` §5, `DECISIONS.md` D-003, D-005 | Permissive non-GPL code & voice asset; RTF $\le 0.50$ on CPU (`PROPOSED TARGET`) | License manifest (`THIRD_PARTY_NOTICES.md`), RTF logs (Task M0-2) |
| **Gate G-02** | Direct JA↔EN MT Quality & Latency | **EMPIRICAL GATE OPEN** | `SPEC.md` §5.2, `DECISIONS.md` D-006 | BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$, zero critical errors (`PROPOSED TARGETS`) | 10-sentence dialogue benchmark results, MarianMT comparison (Task M0-3) |
| **Gate G-03** | End-to-End Latency & Thermal/Power | **EMPIRICAL GATE OPEN** | `SPEC.md` §8 (Sole Authority), `DECISIONS.md` D-025 | Inbound $\le 1,800\text{ ms}$, Outbound $\le 2,100\text{ ms}$ (`GOVERNING REQUIREMENTS`); AC power check; CPU watchdog | Live latency traces on AC power, watchdog load test (Task M0-6) |
| **Gate G-04** | Audio Topology, Loopback & PTT Safety | **EMPIRICAL GATE OPEN** | `SPEC.md` §4.1–§4.3, `DECISIONS.md` D-016, D-023 | Tests 1, 2A, 2B, 3, 4 pass; $E_{\text{delivery}} \le 50.0\text{ PPM}$; $R_{\text{iso}} \ge 60\text{ dB}$; PTT halts | 60-min loopback log, AES-17 isolation log, PTT timing traces (Tasks M0-4, M0-5) |

*(Note: Proposed amendments C-01 through C-04 and proposed decisions D-028 through D-033 are documented in Section 10 as proposals marked PROPOSED — NOT APPLIED. Proposed ADR D-028 is not an approved governing authority; the governing authority for host power safety is strictly SPEC.md §8.)*

### 1.2 Mandatory Planning-Only Governance Boundary

All activities under Revision 60 are strictly restricted to architectural analysis, specification baseline reconciliation, and verification protocol design. The following eight governance rules are actively enforced:
1. **Accurate Categorized Filesystem Accounting:** Exactly two new documentation files (`docs/ARCHITECTURE_R60.md` and `docs/ARCHITECTURE_R60_REVIEW.md`) are created. Predecessor plans and reviews (`R44` through `R59`) remain strictly unmodified. Governing project files (`SPEC.md`, `CLAUDE.md`, `DECISIONS.md`, and the absent `LICENSE` file) remain completely untouched. Zero application source code, prototype scripts, automated test fixtures, or configuration files are created.
2. **Zero Package or Dependency Installation:** No external software, Python packages, pre-compiled wheels, or runtime dependencies are installed via `pip`, `winget`, `conda`, or manual download.
3. **Zero Model Asset Downloads:** No neural network weights, acoustic checkpoints, vocoder models, tokenizers, or voice data (including Silero VAD, `faster-whisper`, Argos Translate, MarianMT, Piper, or Kokoro) are downloaded from Hugging Face, GitHub, or any remote registry.
4. **Zero Hardware Probing or Device Access:** No physical or virtual audio endpoints (WASAPI playback, loopback taps, microphone inputs, or VB-CABLE drivers) are opened, queried, or initialized.
5. **Zero Execution of Milestone 0 (M0):** Milestone M0 remains strictly UNAUTHORIZED. All nine discovery tasks (M0-1 through M0-9) and five concrete deliverables (DEL-01 through DEL-05) remain planned procedures.
6. **Strict Gate Preservation:** All four release gates (**G-01, G-02, G-03, G-04**) remain strictly **EMPIRICAL GATES OPEN**.
7. **Explicit Disclaimer of Automated Tooling:** Verification claims distinguish manual textual review from mechanical tooling; no automated parser or test runner is falsely reported as active.
8. **Subordination to Governing Documents:** In any conflict between this planning document and `SPEC.md`, `SPEC.md` takes precedence.

---

## 2. Forensic Change & Repair Log (Revisions 45 through 60)

### 2.1 Reconciled Historical Forensic Repairs (R45 through R59)

| Repair Range | Target Area | Forensic Scope & Summary of Corrections | Status |
|---|---|---|---|
| **R45–R50** | Specification Consistency & Rigor | Date dimension reconciliation; operating mode privacy codification; AES-17 mathematical rigor; loopback frame discrepancy metric renaming; PTT bifurcation; laptop shutdown risk grounded in SPEC §8; defect arithmetic reconciliation (28 Corrected, 5 Protocol Specified, sum = 33). | **CORRECTED IN REVISION HISTORY** |
| **R51–R55** | Formatting, Hashes & Baseline Grounding | Elimination of fragmented text; 1:1:1 graph parity (33 nodes, 44 edges, 8 subgraphs); direct physical cryptographic hashing (SHA-256); SPEC.md line 436 verbatim verification; 6-category filesystem accounting established. | **CORRECTED IN REVISION HISTORY** |
| **R56–R57** | Findings Restructuring & Non-Git Qualification | Findings register un-truncation; discovery that workspace lacks `.git` metadata, qualifying historical commit baseline comparison as UNVERIFIED; checklist completeness audit. | **CORRECTED IN REVISION HISTORY** |
| **R58** | Delimiter, Debris & Structure Repairs | Elimination of broken delimiters; restoration of F-08; clean separation of F-01 and F-03 authorities; restoration of full F-09 description; 5-tier status taxonomy on CHK-01..CHK-14; complete debris elimination. | **CORRECTED IN REVISION HISTORY** |
| **R59** | Canonical Findings Register Alignment | Aligned F-01..F-15 1:1:1 with GAP-01..GAP-15 and U-01..U-15; eliminated duplicate TTS finding; restored F-10..F-12 records; disentangled loopback delivery accounting from DAC crystal drift; defined $T_{\text{driver\_dma}} < 100\text{ ms}$. | **CORRECTED IN REVISION HISTORY** |

### 2.2 Revision 60 Forensic Repairs (`R60-01` through `R60-08`)

| Repair ID | Target Area | Forensic Defect Addressed in Revision 60 | Forensic Correction Applied in Revision 60 | Verification Evidence |
|---|---|---|---|---|
| **R60-01** | Rebuild Release-Gate Register (G-01..G-04) | Missing comprehensive standalone records for Gates G-01..G-04; corrupted G-02/G-03 table boundary in prior revisions | Reconstructed complete canonical records for G-01 through G-04 in §9.0 with unique ID, full title, governing authority, gap mappings, status, specific closure criteria, required evidence, empirical vs documentary verification, and explicit remaining blockers | Inspected R60 §1.1, §7.1–§7.4, §9.0; R60 Review §2 |
| **R60-02** | Reconcile Canonical Findings Register (F-01..F-15) | Prior summaries lacked complete fields; F-07 privacy, F-08 STT, F-11 GUI records needed full restoration with defined severity scale | Restored complete summary and detailed records for all 15 canonical findings (F-01..F-15) with explicit severity scale (P0/P1/P2/P3), subsystem, governing authority, gap/U/gate cross-references, evidence locations, description, remediation, and status | Inspected R60 §12.1, §15.2; R60 Review §3 |
| **R60-03** | Rebuild Artifact Metadata Table | Prior review reports contained placeholder entries (`*Measured on Disk*`, `*Current File*`) in the metadata table | Replaced malformed table with a stable, fully populated Markdown table recording exact relative paths, roles, byte sizes, line counts, full SHA-256 hashes, and verification methods for all accessible artifacts | Inspected R60 §13.0; R60 Review §4 |
| **R60-04** | Revalidate Graph & Traceability Parity | Ensuring zero dangling edges, zero orphan nodes, and complete 33-node / 44-edge / 8-subgraph parity under manual audit | Audited Mermaid diagram and registers line-by-line; verified 33 nodes, 44 edges, 8 subgraphs, 0 dangling endpoints, 0 orphans, and complete 15:15:4 traceability mapping; explicitly documented manual audit methodology | Inspected R60 §3.1–§3.3, §12.2, §12.3; R60 Review §5 |
| **R60-05** | Rebuild Integrity Checklist (CHK-01..CHK-14) | Checklist required complete individual records with scope, method, exact evidence location, limitations, and strict 5-tier taxonomy | Reconstructed CHK-01 through CHK-14 with complete fields; recomputed exact taxonomy counts: 8 VERIFIED, 2 PARTIALLY VERIFIED, 4 NOT EMPIRICALLY TESTED, 0 FAILED, 0 BLOCKED | Inspected R60 §14.0; R60 Review §6 |
| **R60-06** | Technical & Privacy Boundary Disclosures | Ensuring rigorous separation between proposed targets, governing requirements, and empirical measurements across all subsystems | Qualified $E_{\text{delivery}} \le 50.0\text{ PPM}$ as user-space buffer pacing; defined $T_{\text{driver\_dma}} < 100\text{ ms}$; distinguished local socket abort from remote cloud cessation; separated digital isolation from acoustic leakage; grounded AC power in SPEC §8 | Inspected R60 §3.4, §6.2, §7.4; R60 Review §7 |
| **R60-07** | Restore Section 9 Gate-Indexed Register | Section 9 required full restoration of gate-to-evidence mappings without omitting G-01 or merging G-02/G-03 | Fully restored all 4 release gates in Section 9 with detailed criteria, planned milestone tasks, and empirical gate open statuses | Inspected R60 §9.0; R60 Review §2 |
| **R60-08** | Proposal Register Integrity (Exactly 10 Unique IDs) | Ensuring exact 1:1 representation of all canonical proposals without missing, duplicate, or phantom IDs | Verified exactly 10 unique proposal IDs: C-01..C-04 and D-028..D-033, all marked PROPOSED — NOT APPLIED; governing files completely untouched | Inspected R60 §10.1, §10.2, §15.4; R60 Review §8 |

---

## 3. Canonical Architecture Model

### 3.1 Architecture Diagram

```mermaid
flowchart TD
    %% =========================================================================
    %% SUBGRAPH 1: INBOUND AUDIO CAPTURE & HARDWARE ENDPOINTS
    %% =========================================================================
    subgraph Inbound_Capture["Inbound Audio Capture & Endpoints"]
        N-01["Browser_Audio<br/>(Zoom Web Meeting Session)"]:::hwNode
        N-02["Dev_Playback<br/>(WASAPI Default Playback Device)"]:::hwNode
        N-03["Dev_Headphones<br/>(Physical Headphones - User Ears)"]:::hwNode
        N-04["Loopback_Cap<br/>(PyAudioWPatch Loopback Client - Candidate)"]:::workerNode
        N-05["Inbound_Audio_Queue<br/>(Raw Loopback PCM Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 2: INBOUND VAD, STT & DISPATCH
    %% =========================================================================
    subgraph Inbound_Processing["Inbound Recognition & Processing"]
        N-06["Inbound_VAD<br/>(Silero VAD ONNX Segmenter)"]:::workerNode
        N-07["Inbound_Speech_Queue<br/>(Voiced Speech Segment Queue)"]:::queueNode
        N-08["Inbound_STT<br/>(faster-whisper int8 JA Worker)"]:::workerNode
        N-09["Inbound_Text_Queue<br/>(Transcribed JA Text Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 3: INBOUND TRANSLATION & USER INTERFACE
    %% =========================================================================
    subgraph Inbound_Translation["Inbound Translation & Presentation"]
        N-10["Inbound_MT<br/>(Local Argos/Marian JA→EN)"]:::workerNode
        N-11["Inbound_Trans_Queue<br/>(Translated EN Text Queue)"]:::queueNode
        N-12["Caption_UI<br/>(Tkinter Overlay Window)"]:::uiNode
    end

    %% =========================================================================
    %% SUBGRAPH 4: OUTBOUND CAPTURE & SPEECH PROCESSING
    %% =========================================================================
    subgraph Outbound_Processing["Outbound Capture & Speech Processing"]
        N-13["User_Mic<br/>(Physical User Speech)"]:::hwNode
        N-14["Mic_Cap<br/>(PyAudioWPatch Mic Capture - Candidate)"]:::workerNode
        N-15["Outbound_Mic_Queue<br/>(Raw Mic PCM Queue)"]:::queueNode
        N-16["Outbound_VAD<br/>(Silero VAD ONNX Segmenter)"]:::workerNode
        N-17["Outbound_Speech_Queue<br/>(Voiced EN Speech Queue)"]:::queueNode
        N-18["Outbound_STT<br/>(faster-whisper int8 EN Worker)"]:::workerNode
        N-19["Outbound_Text_Queue<br/>(Transcribed EN Text Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 5: OUTBOUND TRANSLATION & SYNTHESIS
    %% =========================================================================
    subgraph Outbound_Synthesis["Outbound Translation & Voice Synthesis"]
        N-20["Outbound_MT<br/>(Local Argos/Marian EN→JA)"]:::workerNode
        N-21["Outbound_TTS_Queue<br/>(Target JA Text Queue)"]:::queueNode
        N-22["Outbound_TTS<br/>(Permissive JA TTS Worker)"]:::workerNode
        N-23["Outbound_Render_Queue<br/>(Synthesized JA PCM Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 6: OUTBOUND VIRTUAL AUDIO INJECTION
    %% =========================================================================
    subgraph Outbound_Injection["Outbound Virtual Routing to Zoom"]
        N-24["Cable_Render<br/>(WASAPI Render to VB-CABLE)"]:::workerNode
        N-25["Dev_CableIn<br/>(VB-CABLE Virtual Input)"]:::hwNode
        N-26["Dev_CableOut<br/>(VB-CABLE Virtual Output)"]:::hwNode
        N-27["Z_MicIn<br/>(Zoom Web Mic Ingestion)"]:::hwNode
    end

    %% =========================================================================
    %% SUBGRAPH 7: PUSH-TO-TALK SUPERVISION & CANCELLATION
    %% =========================================================================
    subgraph Control_PTT["Push-to-Talk Supervision & Control"]
        N-28["PTT_Input<br/>(User Hotkey KeyPress/Release)"]:::ctrlNode
        N-29["PTT_Hook<br/>(Win32 WH_KEYBOARD_LL Hook)"]:::ctrlNode
        N-30["PTT_Poller<br/>(50 ms GetAsyncKeyState Poller)"]:::ctrlNode
        N-31["PTT_Controller<br/>(PTT Epoch & Cancellation Engine)"]:::ctrlNode
        N-32["Watchdog_Timer<br/>(CPU & Heartbeat Watchdog)"]:::ctrlNode
    end

    %% =========================================================================
    %% SUBGRAPH 8: CLOUD TRANSLATION ADAPTER (OPT-IN ONLY)
    %% =========================================================================
    subgraph Cloud_Integration["Cloud Translation (Opt-In Only)"]
        N-33["Cloud_MT_Adapter<br/>(Google Gemini REST/SDK Worker)"]:::cloudNode
    end

    %% =========================================================================
    %% DATA FLOW EDGES: INBOUND PIPELINE
    %% =========================================================================
    N-01 -->|E-01: Playback Audio| N-02
    N-02 -->|E-02: Acoustic Output| N-03
    N-02 -.->|E-03: WASAPI Loopback Tap| N-04
    N-04 -->|E-04: 16kHz PCM Frames| N-05
    N-05 -->|E-05: 30ms Audio Chunks| N-06
    N-06 -->|E-06: Voiced JA Audio| N-07
    N-07 -->|E-07: Audio Segments| N-08
    N-08 -->|E-08: JA Transcripts| N-09
    N-09 -->|E-09: JA Text Tokens| N-10
    N-10 -->|E-10: Local EN Text| N-11
    N-11 -->|E-11: Caption Tokens| N-12

    %% =========================================================================
    %% DATA FLOW EDGES: OUTBOUND PIPELINE
    %% =========================================================================
    N-13 -->|E-12: Physical Speech| N-14
    N-14 -->|E-13: 16kHz Mic PCM| N-15
    N-15 -->|E-14: 30ms Mic Chunks| N-16
    N-16 -->|E-15: Voiced EN Audio| N-17
    N-17 -->|E-16: Audio Segments| N-18
    N-18 -->|E-17: EN Transcripts| N-19
    N-19 -->|E-18: EN Text Tokens| N-20
    N-20 -->|E-19: Local JA Text| N-21
    N-21 -->|E-20: Target JA Text| N-22
    N-22 -->|E-21: 22.05kHz JA PCM| N-23
    N-23 -->|E-22: Render PCM Chunks| N-24
    N-24 -->|E-23: WASAPI Render| N-25
    N-25 ===|E-24: Virtual Driver DMA Transfer| N-26
    N-26 ===|E-25: Virtual Mic Stream| N-27

    %% =========================================================================
    %% CONTROL EDGES: PTT SUPERVISION & DOWNSTREAM CANCELLATION
    %% =========================================================================
    N-28 -->|E-26: Key Down/Up Events| N-29
    N-28 -.->|E-27: Physical Key Polling| N-30
    N-29 -->|E-28: Hook Events| N-31
    N-30 -->|E-29: Heartbeat Signals| N-31
    N-31 ==>|E-30: Capture Gate Control| N-14
    N-31 ==>|E-31: Purge Signal| N-15
    N-31 ==>|E-32: Purge Signal| N-17
    N-31 ==>|E-33: Epoch Invalidation| N-18
    N-31 ==>|E-34: Purge Signal| N-19
    N-31 ==>|E-35: Epoch Invalidation| N-20
    N-31 ==>|E-36: Purge Signal| N-21
    N-31 ==>|E-37: Epoch Invalidation| N-22
    N-31 ==>|E-38: Purge Signal| N-23
    N-31 ==>|E-39: Stream Flush / Reset| N-24
    N-32 -.->|E-40: Watchdog Heartbeat| N-31

    %% =========================================================================
    %% CLOUD INTEGRATION EDGES: OPT-IN ONLY
    %% =========================================================================
    N-09 -.->|E-41: JA Text (Opt-In)| N-33
    N-33 -.->|E-42: EN Text Result| N-11
    N-19 -.->|E-43: EN Text (Opt-In)| N-33
    N-33 -.->|E-44: JA Text Result| N-21

    %% =========================================================================
    %% STYLING DEFINITIONS
    %% =========================================================================
    classDef hwNode fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef workerNode fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef queueNode fill:#fffde7,stroke:#fbc02d,stroke-width:2px;
    classDef uiNode fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef ctrlNode fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef cloudNode fill:#ede7f6,stroke:#512da8,stroke-width:2px,stroke-dasharray: 5 5;
```

---

### 3.2 Authoritative Node Register

The table below enumerates all 33 uniquely declared nodes (`N-01` through `N-33`), corresponding exactly to the diagram above:

| Node ID | Canonical Diagram Identifier | Subsystem Classification | Functional Role & Architecture Responsibilities | Execution Boundary & Lifetime |
|---|---|---|---|---|
| **N-01** | `Browser_Audio` | Inbound Capture & Endpoints | Google Chrome / Microsoft Edge Zoom web client rendering meeting audio | User-space Browser Host Process |
| **N-02** | `Dev_Playback` | Inbound Capture & Endpoints | Windows WASAPI default audio playback endpoint (Speakers / Headphone DAC) | Windows Audio Engine (audiodg.exe) |
| **N-03** | `Dev_Headphones` | Inbound Capture & Endpoints | Physical wired/wireless headphones worn by user (mandatory primary feedback defense) | Physical Hardware / User Ears |
| **N-04** | `Loopback_Cap` | Inbound Capture & Endpoints | PyAudioWPatch loopback client (Candidate; subject to M0-1 wheel verification) | KoeBridge Process (Background Audio Thread) |
| **N-05** | `Inbound_Audio_Queue` | Inbound Capture & Endpoints | Bounded thread-safe queue buffering raw captured 16 kHz mono 16-bit PCM chunks | Thread-safe Python Queue (`maxsize=100`) |
| **N-06** | `Inbound_VAD` | Inbound Recognition | Silero VAD ONNX Runtime engine detecting speech in 30 ms (512-sample) chunks | Background Worker Thread (CPU ONNX Engine) |
| **N-07** | `Inbound_Speech_Queue` | Inbound Recognition | Bounded queue holding contiguous voiced Japanese speech segments | Thread-safe Python Queue (`maxsize=20`) |
| **N-08** | `Inbound_STT` | Inbound Recognition | `faster-whisper` `small` `int8` CPU transcription worker converting JA speech to text | Background Worker Thread (CTranslate2 Engine) |
| **N-09** | `Inbound_Text_Queue` | Inbound Recognition | Bounded queue holding transcribed Japanese text strings with timing metadata | Thread-safe Python Queue (`maxsize=50`) |
| **N-10** | `Inbound_MT` | Inbound Translation | Local Argos Translate / MarianMT JA→EN translation worker | Background Worker Thread (Local MT Engine) |
| **N-11** | `Inbound_Trans_Queue` | Inbound Translation | Bounded queue holding translated English text strings ready for display | Thread-safe Python Queue (`maxsize=50`) |
| **N-12** | `Caption_UI` | Presentation UI | Tkinter / ttk desktop overlay window displaying real-time English captions | Main GUI Thread (Tkinter Event Pump) |
| **N-13** | `User_Mic` | Outbound Processing | Physical user microphone acoustic input capturing spoken English speech | Physical Hardware / Environment |
| **N-14** | `Mic_Cap` | Outbound Processing | PyAudioWPatch mic capture worker (Candidate; gated by PTT state machine) | Background Audio Thread (WASAPI Input Client) |
| **N-15** | `Outbound_Mic_Queue` | Outbound Processing | Bounded queue holding raw 16 kHz mono 16-bit PCM chunks from physical mic | Thread-safe Python Queue (`maxsize=100`) |
| **N-16** | `Outbound_VAD` | Outbound Processing | Silero VAD ONNX engine segmenting voiced English speech chunks | Background Worker Thread (CPU ONNX Engine) |
| **N-17** | `Outbound_Speech_Queue`| Outbound Processing | Bounded queue holding contiguous voiced English speech segments | Thread-safe Python Queue (`maxsize=20`) |
| **N-18** | `Outbound_STT` | Outbound Processing | `faster-whisper` `small` `int8` CPU worker transcribing English speech to text | Background Worker Thread (CTranslate2 Engine) |
| **N-19** | `Outbound_Text_Queue` | Outbound Processing | Bounded queue holding transcribed English text segments | Thread-safe Python Queue (`maxsize=50`) |
| **N-20** | `Outbound_MT` | Outbound Synthesis | Local Argos Translate / MarianMT EN→JA translation worker | Background Worker Thread (Local MT Engine) |
| **N-21** | `Outbound_TTS_Queue` | Outbound Synthesis | Bounded queue holding translated Japanese text segments awaiting voice synthesis | Thread-safe Python Queue (`maxsize=50`) |
| **N-22** | `Outbound_TTS` | Outbound Synthesis | Permissive local Japanese text-to-speech engine synthesizing 22.05 kHz PCM | Background Worker Thread (TTS Engine) |
| **N-23** | `Outbound_Render_Queue`| Outbound Synthesis | Bounded queue holding synthesized Japanese audio PCM frames ready for injection | Thread-safe Python Queue (`maxsize=50`) |
| **N-24** | `Cable_Render` | Outbound Injection | WASAPI shared-mode render client streaming synthesized audio to VB-CABLE Input | Background Audio Thread (WASAPI Render) |
| **N-25** | `Dev_CableIn` | Outbound Injection | VB-CABLE virtual audio device Input endpoint (Windows playback device) | Kernel Virtual Audio Driver (CABLE-A / VB) |
| **N-26** | `Dev_CableOut` | Outbound Injection | VB-CABLE virtual audio device Output endpoint (Windows recording device) | Kernel Virtual Audio Driver (CABLE-A / VB) |
| **N-27** | `Z_MicIn` | Outbound Injection | Zoom web client microphone input selecting VB-CABLE Output as meeting audio | User-space Browser WebRTC Client |
| **N-28** | `PTT_Input` | Push-to-Talk Control | Physical keyboard hardware generating KeyDown and KeyUp scan codes | Windows Kernel Keyboard Subsystem |
| **N-29** | `PTT_Hook` | Push-to-Talk Control | Win32 `WH_KEYBOARD_LL` low-level global keyboard hook monitoring hotkey | Dedicated Win32 Message Loop Thread |
| **N-30** | `PTT_Poller` | Push-to-Talk Control | 50 ms polling heartbeat using `GetAsyncKeyState` for fail-safe key state verification | Background Polling Timer Thread |
| **N-31** | `PTT_Controller` | Push-to-Talk Control | State machine supervising PTT epochs, queue purging, and cancellation tokens | Core Control State Machine Thread |
| **N-32** | `Watchdog_Timer` | Push-to-Talk Control | Host health, CPU load ($\ge 95\%$), and heartbeat watchdog timer | Background Supervisor Thread |
| **N-33** | `Cloud_MT_Adapter` | Cloud Integration | Optional Google Gemini REST/SDK adapter for MT (disabled default, opt-in only) | Async Network Worker Thread (Volatile Memory) |

---

### 3.3 Authoritative Edge Register

The table below enumerates all 44 uniquely declared edges (`E-01` through `E-44`), corresponding exactly to the diagram above:

| Edge ID | Source Node | Target Node | Data Payload / Control Signal | Direction | Functional Purpose & Protocol Mechanism |
|---|---|---|---|---|---|
| **E-01** | `Browser_Audio` | `Dev_Playback` | 48 kHz stereo PCM audio | Unidirectional | Zoom meeting audio rendered to default playback device |
| **E-02** | `Dev_Playback` | `Dev_Headphones` | Acoustic headphone output | Unidirectional | Physical acoustic delivery to user ears (feedback defense) |
| **E-03** | `Dev_Playback` | `Loopback_Cap` | Shared-mode loopback audio | Unidirectional | WASAPI loopback capture tap tapping default playback device |
| **E-04** | `Loopback_Cap` | `Inbound_Audio_Queue` | 16 kHz mono 16-bit PCM chunks | Unidirectional | Loopback capture worker enqueueing audio chunks (`q.put()`) |
| **E-05** | `Inbound_Audio_Queue`| `Inbound_VAD` | 30 ms (512-sample) audio chunks | Unidirectional | VAD worker pulling chunks for speech energy inference |
| **E-06** | `Inbound_VAD` | `Inbound_Speech_Queue`| Voiced Japanese speech segments | Unidirectional | Contiguous speech segments pushed upon silence threshold |
| **E-07** | `Inbound_Speech_Queue`| `Inbound_STT` | Voiced speech audio segments | Unidirectional | Speech-to-text worker pulling segments for transcription |
| **E-08** | `Inbound_STT` | `Inbound_Text_Queue` | Transcribed Japanese text strings | Unidirectional | Transcribed tokens pushed with segment timestamps |
| **E-09** | `Inbound_Text_Queue`| `Inbound_MT` | Japanese text strings | Unidirectional | Local MT worker pulling text tokens for translation |
| **E-10** | `Inbound_MT` | `Inbound_Trans_Queue` | Translated English text strings | Unidirectional | Local translated text pushed to presentation queue |
| **E-11** | `Inbound_Trans_Queue`| `Caption_UI` | Formatted English text captions | Unidirectional | Tkinter event loop pulling captions for UI rendering |
| **E-12** | `User_Mic` | `Mic_Cap` | Physical acoustic user speech | Unidirectional | Physical microphone hardware acoustic capture |
| **E-13** | `Mic_Cap` | `Outbound_Mic_Queue` | 16 kHz mono 16-bit PCM chunks | Unidirectional | Physical mic capture worker pushing raw audio chunks |
| **E-14** | `Outbound_Mic_Queue`| `Outbound_VAD` | 30 ms (512-sample) audio chunks | Unidirectional | Outbound VAD pulling mic chunks for speech detection |
| **E-15** | `Outbound_VAD` | `Outbound_Speech_Queue`| Voiced English speech segments | Unidirectional | Contiguous voiced English segments pushed upon silence |
| **E-16** | `Outbound_Speech_Queue`| `Outbound_STT`| English speech audio segments | Unidirectional | English STT worker pulling segments for transcription |
| **E-17** | `Outbound_STT` | `Outbound_Text_Queue`| Transcribed English text strings | Unidirectional | Transcribed English text pushed to outbound text queue |
| **E-18** | `Outbound_Text_Queue`| `Outbound_MT` | English text strings | Unidirectional | Local MT worker pulling English text for translation |
| **E-19** | `Outbound_MT` | `Outbound_TTS_Queue` | Translated Japanese text strings | Unidirectional | Translated Japanese text pushed to voice synthesis queue |
| **E-20** | `Outbound_TTS_Queue`| `Outbound_TTS` | Target Japanese text strings | Unidirectional | Local TTS worker pulling text for speech synthesis |
| **E-21** | `Outbound_TTS` | `Outbound_Render_Queue`| Synthesized 22.05 kHz PCM frames | Unidirectional | Synthesized Japanese speech pushed to render queue |
| **E-22** | `Outbound_Render_Queue`| `Cable_Render`| 22.05 kHz PCM audio frames | Unidirectional | Render client pulling audio for virtual driver streaming |
| **E-23** | `Cable_Render` | `Dev_CableIn` | WASAPI shared-mode render stream | Unidirectional | Streaming synthesized Japanese speech to VB-CABLE Input |
| **E-24** | `Dev_CableIn` | `Dev_CableOut` | Kernel virtual driver DMA frames | Unidirectional | Virtual audio driver internal DMA circular buffer transfer |
| **E-25** | `Dev_CableOut` | `Z_MicIn` | Virtual microphone recording stream| Unidirectional | Zoom web client ingesting VB-CABLE Output as microphone |
| **E-26** | `PTT_Input` | `PTT_Hook` | KeyDown / KeyUp physical events | Unidirectional | Win32 low-level keyboard hook intercepting hotkey |
| **E-27** | `PTT_Input` | `PTT_Poller` | Physical key state query | Bidirectional | 50 ms polling heartbeat querying `GetAsyncKeyState` |
| **E-28** | `PTT_Hook` | `PTT_Controller` | Hotkey state transition events | Unidirectional | Asynchronous hook callback notifying PTT state machine |
| **E-29** | `PTT_Poller` | `PTT_Controller` | Polling key state confirmation | Unidirectional | Polling supervisor confirming key state every 50 ms |
| **E-30** | `PTT_Controller` | `Mic_Cap` | Capture enable / disable gate | Unidirectional | Controller opening/closing physical microphone capture |
| **E-31** | `PTT_Controller` | `Outbound_Mic_Queue` | Immediate queue purge signal | Unidirectional | Controller clearing raw mic queue on KeyUp (`q.clear()`) |
| **E-32** | `PTT_Controller` | `Outbound_Speech_Queue`| Immediate queue purge signal | Unidirectional | Controller clearing voiced speech queue on KeyUp |
| **E-33** | `PTT_Controller` | `Outbound_STT` | Epoch invalidation token | Unidirectional | Controller invalidating in-flight English STT inference |
| **E-34** | `PTT_Controller` | `Outbound_Text_Queue`| Immediate queue purge signal | Unidirectional | Controller clearing outbound text queue on KeyUp |
| **E-35** | `PTT_Controller` | `Outbound_MT` | Epoch invalidation token | Unidirectional | Controller invalidating in-flight MT translation epoch |
| **E-36** | `PTT_Controller` | `Outbound_TTS_Queue` | Immediate queue purge signal | Unidirectional | Controller clearing outbound TTS queue on KeyUp |
| **E-37** | `PTT_Controller` | `Outbound_TTS` | Epoch invalidation token | Unidirectional | Controller invalidating in-flight Japanese TTS synthesis |
| **E-38** | `PTT_Controller` | `Outbound_Render_Queue`| Immediate queue purge signal | Unidirectional | Controller clearing audio render queue on KeyUp |
| **E-39** | `PTT_Controller` | `Cable_Render` | Stream flush & reset signal | Unidirectional | Controller resetting WASAPI render client buffer |
| **E-40** | `Watchdog_Timer` | `PTT_Controller` | Watchdog timeout & health alert | Unidirectional | Watchdog resetting PTT state if stuck or CPU $\ge 95\%$ |
| **E-41** | `Inbound_Text_Queue`| `Cloud_MT_Adapter` | Japanese text string (Opt-In) | Unidirectional | Inbound text dispatched to Gemini in Cloud Opt-In Mode |
| **E-42** | `Cloud_MT_Adapter` | `Inbound_Trans_Queue`| Translated English text string | Unidirectional | Cloud translated English text committed to display queue |
| **E-43** | `Outbound_Text_Queue`| `Cloud_MT_Adapter` | English text string (Opt-In) | Unidirectional | Outbound text dispatched to Gemini in Cloud Opt-In Mode |
| **E-44** | `Cloud_MT_Adapter` | `Outbound_TTS_Queue` | Translated Japanese text string | Unidirectional | Cloud translated Japanese text committed to TTS queue |

---

### 3.4 Operational Protocols & Boundary Safety

#### 3.4.1 Directional Pipeline Decoupling & Virtual Routing Topology
KoeBridge strictly decouples inbound (meeting listening) and outbound (speech injection) pipelines into isolated execution domains:
1. **Inbound Pipeline:** Captured browser audio flows exclusively from `Dev_Playback` through `Loopback_Cap` to `Inbound_VAD` $\to$ `Inbound_STT` (Japanese) $\to$ `Inbound_MT` (JA→EN) $\to$ `Caption_UI`. Inbound audio is NEVER routed to VB-CABLE, physical speakers, or external microphones.
2. **Outbound Pipeline:** Spoken English audio flows exclusively from `User_Mic` through `Mic_Cap` to `Outbound_VAD` $\to$ `Outbound_STT` (English) $\to$ `Outbound_MT` (EN→JA) $\to$ `Outbound_TTS` (Japanese) $\to$ `Cable_Render` $\to$ `Dev_CableIn` $\to$ `Dev_CableOut` $\to$ `Z_MicIn`.
3. **Primary Feedback Defense:** Explicit physical device separation is mandatory (`DECISIONS.md` D-016). Meeting participants must use physical headphones (`Dev_Headphones`). Open laptop speakers must not be used during meeting operation.
4. **No Cross-Talk Frame Suppression:** Inbound loopback capture must never be unconditionally suppressed during outbound push-to-talk speech (`SPEC.md` §4.3). Meeting participants must be able to hear overlapping meeting dialogue continuously.

#### 3.4.2 Privacy Governance, Definitive Arbitration & Network Boundaries

KoeBridge enforces two mutually exclusive, deterministic operating modes strictly governed by `SPEC.md` §5.2 and §6 (`DECISIONS.md` D-010, D-011):

```
+--------------------------------------------------------------------------------------------------+
|                                    OPERATING MODE GOVERNANCE                                     |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|  [MODE 1: LOCAL MODE (DEFAULT)]                                                                  |
|    - 100% Offline Execution: Zero socket creation, zero network egress, zero cloud SDK calls.    |
|    - Strict Data Confinement: Zero audio, transcripts, or telemetry ever leaves the host.        |
|    - Translation Engine: Local Argos Translate / MarianMT only.                                  |
|    - Failure Semantics: Engine failure produces explicit UI error ("Local MT Unavailable").      |
|    - Silent Fallback: AUTOMATIC SILENT FALLBACK TO CLOUD IS STRICTLY PROHIBITED.                 |
|    - Local Slowness / Load: High CPU or slow processing NEVER triggers cloud offloading.         |
|                                                                                                  |
|  [MODE 2: CLOUD OPT-IN MODE (DISABLED BY DEFAULT)]                                               |
|    - Pre-Activation Consent: Explicit informed consent dialog disclosing exact provider terms.  |
|    - Payload Restriction: Plain text transcripts ONLY (never raw or compressed audio).           |
|    - Credential Storage: Google Gemini API key stored in Windows Credential Manager via keyring. |
|    - Canonical Sequential Execution:                                                             |
|        1. Cloud MT is invoked first. Request tagged with CorrID = <SessionID, EpochID, Seq>.     |
|        2. Strict 2.50 s client timeout enforced on HTTP request (PROPOSED TARGET).               |
|        3. If Cloud responds within 2.50 s for current EpochID: Commit result immediately.        |
|        4. If Cloud fails (auth, quota, network error, or timeout > 2.50 s):                      |
|             a. If user enabled "Local fallback on cloud failure" setting (SPEC §6):              |
|                Sequentially dispatch to local MT and commit result if local models ready.        |
|             b. If "Cloud fallback: Off" setting active (Default per SPEC §6):                   |
|                Surface visible UI error. Do NOT invoke local MT.                                 |
|        5. If PTT KeyUp occurs (EpochID invalidated): Immediately abort client HTTP socket        |
|           and DISCARD any late-arriving cloud response. Late responses never enter queues.       |
|    - Concurrent Dispatch Rejection: Concurrent dual-dispatch is rejected because running local   |
|      MT on every segment burns duplicate CPU cycles, increasing laptop shutdown risk (§8).       |
|    - Network Boundary Disclosures:                                                               |
|        Closing a client HTTP socket cancels local response processing, but DOES NOT guarantee    |
|        that the remote cloud provider ceased processing a request already received over network. |
|    - Unresolved Provider Terms Gate: Tracking Google Gemini free-tier data logging policies      |
|      remains an OPEN release blocker.                                                            |
+--------------------------------------------------------------------------------------------------+
```

#### 3.4.3 Outbound Push-to-Talk Lifecycle & Downstream Cancellation Architecture

Push-to-Talk (PTT) is the primary outbound transmission control mechanism (`DECISIONS.md` D-023). To ensure safety and prevent stuck transmit states, PTT enforces dual-signal supervision and multi-stage downstream cancellation:

1. **Dual-Signal Supervision:**
   - Primary: Win32 `WH_KEYBOARD_LL` low-level keyboard hook (`N-29`) intercepts physical KeyDown and KeyUp events globally across all desktop windows.
   - Secondary: A 50 ms timer thread (`N-30`) continuously queries physical key state using `GetAsyncKeyState`. If the hook drops a KeyUp event due to UI focus transitions or message loop starvation, the poller detects key release within $\le 50\text{ ms}$ and triggers fail-safe release.
2. **KeyDown State Transition (`IDLE` $\to$ `ACTIVE`):**
   - Monotonic epoch ID increments: `EpochID = N + 1`.
   - Microphone capture worker (`N-14`) is unmuted.
   - Audio chunks flow to `Outbound_Mic_Queue`.
3. **KeyUp State Transition (`ACTIVE` $\to$ `INVALIDATED`):**
   - **Hotkey Ingestion Latency ($T_1 \le 30\text{ ms}$, `PROPOSED TARGET`):** Start = physical KeyUp scan code generated by keyboard controller; End = Win32 `WH_KEYBOARD_LL` hook callback receives `WM_KEYUP`; Mechanism = high-resolution QPC timestamp diff ($\Delta T = t_{\text{hook}} - t_{\text{event}}$).
   - **Cancellation Token Dispatch Latency ($T_2 \le 60\text{ ms}$, `PROPOSED TARGET`):** Start = PTT controller receives KeyUp event; End = atomic cancellation token set on all worker queues; Mechanism = timestamp diff.
   - **Microphone Capture Halt Latency ($T_3 \le 10\text{ ms}$, `PROPOSED TARGET`):** Start = PTT controller issues halt signal; End = capture thread stops reading WASAPI mic endpoint; Mechanism = packet audit confirming zero audio frames captured after halt ($N_{\text{post\_close\_mic}} == 0$).
   - **All Outbound Queues Immediately Purged:** Software queues (`Outbound_Mic_Queue`, `Outbound_Speech_Queue`, `Outbound_Text_Queue`, `Outbound_TTS_Queue`, `Outbound_Render_Queue`) cleared immediately (`q.clear()`, `qsize() == 0`).
   - **Audio Render Reset Latency ($T_4 \le 50\text{ ms}$, `PROPOSED TARGET`):** Start = PTT controller issues stream flush; End = `IAudioClient::Reset` returns; Mechanism = COM method duration timer.
   - **Stale Worker Outputs Discarded:** Stale worker outputs matching prior epochs are discarded ($N_{\text{stale\_rendered}} == 0$).
4. **Physical & OS Boundary Disclosures:**
   - **Driver Circular DMA Buffer Latency ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$):** User-space software cannot recall or purge audio frames already committed to the VB-CABLE virtual driver DMA circular buffer ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$, estimated from standard driver buffer sizing). Enforcing `qsize() == 0` purges software queues but cannot silence audio already transferred to the driver.
   - **Non-Preemptible Native C++ Inference:** In-flight CTranslate2 or ONNX Runtime tensor execution cannot be safely preempted mid-inference without thread termination or heap corruption. Cancellation is cooperative: the worker completes its current tensor operation, checks the epoch token, and discards the result.
   - **Secure Desktop Hook Suspension:** Win32 `WH_KEYBOARD_LL` hooks stop receiving input during secure desktop transitions (UAC prompts, Winlogon, lock screen). The secondary poller and a 15-second maximum transmit watchdog ensure fail-safe release upon return to the user desktop.

#### 3.4.4 Host Stability, AC Power Preflight & CPU Watchdog Thresholds
1. **Observed Hardware Risk Grounding:** Target hardware (Intel Core i7-8750H laptop) has an observed history of sudden hardware shutdowns under heavy load when operating on battery power (`SPEC.md` §8). All benchmarking and live pipeline execution require verified plugged-in AC power (`ACLineStatus == 1`, `GOVERNING REQUIREMENT`). If AC power is disconnected during operation, the pipeline must cleanly abort. The exact failure mechanism (battery cell voltage sag vs thermal protection) is an observed stability concern and is not asserted as a single proven cause without empirical instrumentation.
2. **Provisional CPU Watchdog Policy:** A background watchdog monitors host CPU load. If CPU utilization reaches $\ge 95\%$ sustained for $\ge 15\text{ s}$ (`PROPOSED TARGET`), the watchdog alerts the user and temporarily throttles VAD/STT processing to protect host stability. Governing authority for host power safety is strictly `SPEC.md` §8; proposed ADR D-028 remains unapplied.

---

## 4. Planned Repository Layout & Module Boundaries

```
KoeBridge-for-Zoom/
├── CLAUDE.md                   # Developer instructions & workflow rules (checked in)
├── DECISIONS.md                # Approved Architecture Decision Records D-001..D-027 (checked in)
├── SPEC.md                     # Authoritative system specification (checked in)
├── LICENSE                     # Project license file (Target: MIT; missing on disk, GAP-15)
├── docs/                       # Architecture plans, benchmarks, and licensing manifests
│   ├── ARCHITECTURE_R60.md     # Current Architecture & Verification Plan (Revision 60)
│   ├── ARCHITECTURE_R60_REVIEW.md # Current Forensic Acceptance Review (Revision 60)
│   ├── BENCHMARKS.md           # Empirical benchmark records (planned M0-1..M0-6)
│   ├── M0_DISCOVERY_REPORT.md  # Milestone 0 discovery findings dossier (planned M0-9)
│   └── THIRD_PARTY_NOTICES.md  # Multi-tier software & model asset license manifest (planned M0-2)
├── prototypes/                 # Isolated discovery prototype scripts (planned M0 execution)
│   └── m0_discovery/           # 7 planned discovery scripts (PROTO-01 through PROTO-07)
├── src/                        # Core application package (planned post-M0)
│   └── koebridge/
│       ├── __init__.py
│       ├── audio/              # WASAPI loopback capture, mic input, VB-CABLE render
│       ├── vad/                # Silero VAD chunk segmenter
│       ├── stt/                # faster-whisper speech recognition workers
│       ├── mt/                 # Argos / MarianMT local translation & cloud adapter
│       ├── tts/                # Local Japanese voice synthesis engine
│       ├── ptt/                # Win32 hook, polling heartbeat & cancellation coordinator
│       └── ui/                 # Tkinter caption overlay window & settings dialog
└── tests/                      # Automated test suite (planned post-M0)
    ├── unit/                   # State machine, queue, and text processing unit tests
    └── mocks/                  # Mock audio devices and synthetic engine stubs
```

---

## 5. Five-Tier Auditable Evidence Matrix

| Evidence Tier | Designation | Verification Standard | Current Scope & Status |
|---|---|---|---|
| **Tier 1 (T-1)** | Plan Text Inspection | Direct manual line-by-line inspection of current document text | Used for verifying textual completeness, mathematical validity, and node/edge registers |
| **Tier 2 (T-2)** | Static Code / Spec Audit | Automated AST, syntax, or schema analysis of checked-in files | Used for auditing `SPEC.md`, `DECISIONS.md`, and `CLAUDE.md` requirements |
| **Tier 3 (T-3)** | Synthetic Unit Test | Deterministic execution in isolated mock harness without hardware | Used for PTT state machine Phase 4A testing and text parsing |
| **Tier 4 (T-4)** | Live Windows Host Test | Execution on physical Windows 10/11 x64 host with actual hardware | Required for WASAPI loopback, VB-CABLE, and PTT Phase 4B testing (Deferred to M0) |
| **Tier 5 (T-5)** | Empirical Benchmark Record| Timestamped hardware measurements on target i7-8750H on AC power | Required for clearing Gates G-01, G-02, G-03, G-04 (Deferred to M0) |

---

## 6. Multi-Tier Licensing Framework & Translation Evaluation

### 6.0 Multi-Tier Software & Model Asset Licensing Matrix

| Component / Asset | Candidate Project | Code License | Weights / Voice License | Licensing Status & Evaluation Guidance |
|---|---|---|---|---|
| **VAD Engine** | Silero VAD (ONNX) | MIT | MIT / Permissive | **APPROVED CANDIDATE** (`DECISIONS.md` D-008). Permissive commercial runtime. |
| **Speech Recognition** | `faster-whisper` | MIT | MIT / Apache 2.0 (OpenAI) | **APPROVED CANDIDATE** (`DECISIONS.md` D-007). CTranslate2 engine is MIT. |
| **Local MT (Primary)** | Argos Translate | MIT | CC0 / Permissive | **APPROVED CANDIDATE** (`DECISIONS.md` D-006). Direct JA↔EN model required. |
| **Local MT (Fallback)**| MarianMT (CTranslate2)| Apache 2.0 | CC-BY-4.0 / MIT | **APPROVED FALLBACK**. Evaluated if Argos translation fails accuracy thresholds. |
| **Japanese TTS Engine**| Piper (`piper-tts` core)| MIT | Varies by voice | **CONDITIONALLY APPROVED CORE**. Core C++ runtime is MIT. |
| **Japanese TTS Fork** | `OHF-Voice/piper1-gpl` | **GPL-3.0-or-later** | Varies by voice | **STRICTLY UNAPPROVED BY DEFAULT** (`SPEC.md` §5). Copyleft violation risk. |
| **Japanese Voice (TTS)**| Candidate JA Voices | N/A (Weights) | UNVERIFIED | **MANDATORY HARD RELEASE GATE (G-01)**. Unapproved voice is a release blocker. |
| **TTS Alternative** | Kokoro-82M | Apache 2.0 | UNVERIFIED CHECKPOINTS | **UNRESOLVED**. Apache 2.0 code license does not clear training provenance. |
| **TTS Alternative** | VOICEVOX Core | LGPLv3 | Character commercial terms | **EXCLUDED BY DEFAULT** (`DECISIONS.md` D-004). Restrictive voice usage terms. |
| **Audio I/O Bindings** | `PyAudioWPatch` | MIT | N/A (Software) | **CANDIDATE ONLY** (`DECISIONS.md` D-026). Subject to wheel availability (GAP-13) & redistribution checks. |
| **GUI Subsystem** | Tkinter / ttk | Python (PSFL) | N/A (Standard Library) | **APPROVED CANDIDATE** (`DECISIONS.md` D-002). Standard library permissive. |
| **Credential Storage** | `keyring` | MIT | N/A (Software) | **APPROVED CANDIDATE** (`DECISIONS.md` D-027). Backed by Windows Credential Manager. |
| **Python Runtime** | CPython 3.11 / 3.12 / 3.13| PSFL | N/A (Runtime) | **PRIORITIZE 3.11/3.12**. Python 3.13 binary wheels unverified (GAP-13). |

### 6.1 Direct JA↔EN Machine Translation Benchmark Suite

The 10-sentence dialogue benchmark suite (TC-01 through TC-10) serves as an initial **screening smoke test** for pre-filtering candidate MT models in M0-3. Full model validation requires a domain-specific corpus of 100+ dialogue turns.

```
TC-01 (Architecture):
  JA: 本日のアジェンダは、マイクロサービスのレイテンシ改善とDBのコネクションプール最適化です。
  EN: Today's agenda is microservice latency improvement and database connection pool optimization.
TC-02 (Negation):
  JA: このAPIエンドポイントは非同期処理に対応していません。
  EN: This API endpoint does not support asynchronous processing.
TC-03 (Numbers & Units):
  JA: タイムアウト値を500ミリ秒から2.5秒に延長し、リトライ回数を3回に設定してください。
  EN: Please extend the timeout value from 500 milliseconds to 2.5 seconds and set the retry count to 3.
TC-04 (Technical Jargon):
  JA: キャッシュヒット率が低下しているため、Redisのメモリ使用量を監視する必要があります。
  EN: Because the cache hit rate is declining, we need to monitor Redis memory usage.
TC-05 (Urgency):
  JA: 本番環境でメモリリークが発生しているため、直ちにロールバックを実施してください。
  EN: A memory leak has occurred in production, so please execute a rollback immediately.
TC-06 (Action Item):
  JA: 明日の午前10時までに、プルリクエストのレビューとマージを完了させてください。
  EN: Please complete the pull request review and merge by 10:00 AM tomorrow.
TC-07 (Condition):
  JA: CPU使用率が85%を超過した場合、自動的にオートスケーリングが発動します。
  EN: If CPU utilization exceeds 85%, autoscaling is triggered automatically.
TC-08 (Security):
  JA: APIキーをソースコードにハードコードせず、環境変数から読み込んでください。
  EN: Do not hardcode API keys into source code; please load them from environment variables.
TC-09 (Meeting Protocol):
  JA: 画面共有を開始しますので、スライドが見えているか確認していただけますか。
  EN: I will start screen sharing, so could you please confirm if you can see the slides?
TC-10 (Agreement):
  JA: その設計方針で問題ありませんので、実装を進めてください。
  EN: There is no problem with that design policy, so please proceed with implementation.
```

### 6.2 Quantitative Translation Scoring Rubric
- **Corpus Level:** SacreBLEU $\ge 25.0$ (`PROPOSED TARGET`), chrF++ $\ge 0.50$ (`PROPOSED TARGET`), inference latency $\le 600\text{ ms}$ on CPU (`GOVERNING REQUIREMENT` per `SPEC.md` §5.2).
- **Sentence Level:**
  1. *Complete Inversion:* Translating negation as affirmation (or vice versa) is a catastrophic failure (`GOVERNING REQUIREMENT`).
  2. *Numerical Corruption:* Mistranslating numeric parameters, scale, or units is a critical failure (`GOVERNING REQUIREMENT`).
  3. *Hallucinatory Text:* Generating repetitive loops or unrelated phrases (`GOVERNING REQUIREMENT`).

---

## 7. Release Gates & Technical Protocols

### 7.1 Gate G-01: Permissive Japanese TTS Engine & Voice Asset License Clearance
- **Status:** **EMPIRICAL GATE OPEN**
- **Governing Authority:** `SPEC.md` §5, `DECISIONS.md` D-003, D-004, D-005.
- **Mandatory Criteria:**
  1. Standalone TTS engine runnable locally on Windows 10/11 x64 on CPU (`GOVERNING REQUIREMENT`).
  2. Engine code licensed under permissive terms (MIT, Apache 2.0, BSD). `OHF-Voice/piper1-gpl` (GPL-3.0) is unapproved by default (`GOVERNING REQUIREMENT`).
  3. Japanese acoustic weights, phonemizer, and voice checkpoint independently verified under permissive commercial license (`GOVERNING REQUIREMENT`).
  4. Real-time factor $\text{RTF} \le 0.50$ ($500\text{ ms}$ compute for $1,000\text{ ms}$ speech) on Intel Core i7-8750H (`PROPOSED TARGET`).
- **Required Evidence to Close Gate:** Delivery of `docs/THIRD_PARTY_NOTICES.md` with complete license manifest, RTF benchmark logs on AC power, and PyPI binary wheel availability verification.
- **Planned Milestone Tasks:** Milestone M0 Task M0-2.

### 7.2 Gate G-02: Direct JA↔EN Machine Translation Quality & Latency Clearance
- **Status:** **EMPIRICAL GATE OPEN**
- **Governing Authority:** `SPEC.md` §5.2, `DECISIONS.md` D-006.
- **Mandatory Criteria:**
  1. Direct JA$\leftrightarrow$EN translation without intermediate pivot languages (`GOVERNING REQUIREMENT` per `DECISIONS.md` D-006).
  2. Passing score on 10-sentence dialogue benchmark suite (BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$ on CPU, `PROPOSED TARGETS`).
  3. Zero catastrophic errors on negation, numerical parameters, or technical terminology (`GOVERNING REQUIREMENT`).
- **Required Evidence to Close Gate:** Empirical benchmark records in `docs/BENCHMARKS.md` evaluating Argos Translate and MarianMT, and verification of offline Local Mode execution default.
- **Planned Milestone Tasks:** Milestone M0 Task M0-3.

### 7.3 Gate G-03: End-to-End Pipeline Latency & Host Hardware Thermal/Power Guardrails
- **Status:** **EMPIRICAL GATE OPEN**
- **Governing Authority:** `SPEC.md` §8 (Sole Governing Authority), `DECISIONS.md` D-025. *(Note: Proposed ADR D-028 is unapplied; SPEC.md §8 is the sole governing authority.)*
- **Mandatory Criteria:**
  1. Inbound translation latency budget $\le 1,800\text{ ms}$ target ($2,400\text{ ms}$ max, `GOVERNING REQUIREMENTS` per `SPEC.md` §5).
  2. Outbound translation & speech injection budget $\le 2,100\text{ ms}$ target ($2,900\text{ ms}$ max, `GOVERNING REQUIREMENTS` per `SPEC.md` §5).
  3. All benchmarking executed under verified plugged-in AC power (`ACLineStatus == 1`, `GOVERNING REQUIREMENT` per `SPEC.md` §8).
  4. Background watchdog throttling pipeline if CPU utilization $\ge 95\%$ sustained for $\ge 15\text{ s}$ (`PROPOSED TARGET`).
- **Required Evidence to Close Gate:** Live execution traces on AC power, watchdog load test logs in `docs/BENCHMARKS.md`, and Gemini DPAPI keyring storage verification.
- **Planned Milestone Tasks:** Milestone M0 Task M0-6.

### 7.4 Gate G-04: Audio Endpoint Topology, Loopback Stability & PTT Safety Verification
- **Status:** **EMPIRICAL GATE OPEN**
- **Governing Authority:** `SPEC.md` §4.1, §4.2, §4.3, `DECISIONS.md` D-016, D-023.
- **Mandatory Criteria:**
  1. Enumeration and format negotiation across `Dev_Playback`, `Dev_Microphone`, and `Dev_CableIn` (`GOVERNING REQUIREMENT`).
  2. 60-minute continuous loopback stream stability satisfying $E_{\text{delivery}} \le 50.0\text{ PPM}$ (`PROPOSED TARGET`), zero buffer discontinuities ($N_{\text{discontinuity}} == 0$, `GOVERNING REQUIREMENT`), zero stream restarts ($N_{\text{restarts}} == 0$, `GOVERNING REQUIREMENT`), and $T_{\text{stall\_max}} \le 250\text{ ms}$ (`PROPOSED TARGET`).
  3. Digital route isolation achieving relative isolation $R_{\text{iso}} \ge 60.0\text{ dB}$ ($L_{\text{cap}} \le -80.0\text{ dBFS}$, `PROPOSED TARGET`) under AES-17 sine stimulus testing.
  4. Physical acoustic leakage screening verifying background-corrected leakage $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ (`PROPOSED TARGET`), reinforced by mandatory physical headphones (`Dev_Headphones`, `GOVERNING REQUIREMENT`).
  5. Bifurcated PTT lifecycle verification: KeyUp queue purge ($qsize() == 0$, `GOVERNING REQUIREMENT`), microphone halt $\le 10\text{ ms}$ (`PROPOSED TARGET`), render reset $\le 50\text{ ms}$ (`PROPOSED TARGET`), and fail-safe 50 ms polling heartbeat fallback (`GOVERNING REQUIREMENT`).
  6. Tkinter caption overlay rendering at $\ge 30\text{ FPS}$ without stealing user input focus (`GOVERNING REQUIREMENT` per `SPEC.md` §5.4).
- **Required Evidence to Close Gate:** 60-minute loopback log, AES-17 digital isolation log, acoustic screening log, live PTT timing traces, and Tkinter 30 FPS responsiveness log.
- **Planned Milestone Tasks:** Milestone M0 Tasks M0-4, M0-5, and M0-7.

#### Test 1: Audio Endpoint Enumeration & Verification Protocol
- Verify enumeration of `Dev_Playback`, `Dev_Microphone`, and `Dev_CableIn` via `PyAudioWPatch` (Candidate).
- Ensure VB-CABLE Input and Output virtual endpoints are detected with matching sample rates (44.1 kHz / 48 kHz).

#### Test 2A: WASAPI Loopback Capture Fidelity & Buffer Negotiation Protocol
- Capture 16 kHz mono 16-bit PCM stream from `Dev_Playback` in shared mode.
- Verify buffer size negotiation between 10 ms and 25 ms without audio underruns.

#### Test 2B: 60-Minute Continuous Loopback Stability & Aggregate Frame-Delivery Accounting Protocol
- **Measured Metric:** **Aggregate Frame-Delivery Discrepancy** ($E_{\text{delivery}}$) over observation window $T_{\text{obs}} = 3,600.0\text{ s}$ ($1.0\text{ hour}$).
- **Dimensional Qualification — Audio Frame vs Channel Sample:**
  - In PCM digital audio, an **audio frame** represents a single discrete slice of time containing exactly one sample for each active channel ($C$).
  - For a mono stream ($C = 1$), $1\text{ frame} = 1\text{ sample}$. At 16-bit signed integer depth (`paInt16`), $1\text{ frame} = 2\text{ bytes}$.
  - For a stereo stream ($C = 2$), $1\text{ frame} = 2\text{ samples}$ (Left + Right). At 16-bit depth, $1\text{ frame} = 4\text{ bytes}$. At 32-bit float depth (`paFloat32`), $1\text{ frame} = 8\text{ bytes}$.
  - In WASAPI shared-mode loopback capture, the engine typically runs at the endpoint's native mix format: $48,000\text{ Hz}$ stereo 32-bit float ($8\text{ bytes/frame}$).
  - When captured audio is converted/resampled to the target internal pipeline format ($16,000\text{ Hz}$ mono 16-bit int16), $1\text{ frame} = 1\text{ sample} = 2\text{ bytes}$.
  - The frame-delivery discrepancy metric strictly counts **audio frames** (time slices), NOT individual raw channel samples or raw bytes, avoiding $2\times$ or $4\times$ dimensional errors.
- **Time Reference & Elapsed Time Calculation:**
  $$\Delta T_{\text{QPC}} = \frac{\text{QPC}_{\text{end}} - \text{QPC}_{\text{start}}}{\text{QPF}}$$
  where $\text{QPF}$ is the QueryPerformanceFrequency (typically $10,000,000\text{ counts/s}$ on Windows 10/11 x64).
- **Expected Frames Formula:**
  $$N_{\text{expected}} = f_s \times \Delta T_{\text{QPC}}$$
  - For nominal resampled pipeline format ($f_s = 16,000\text{ frames/s}$) over $T_{\text{obs}} = 3,600.0\text{ s}$, $N_{\text{expected}} = 57,600,000\text{ frames}$.
  - If measured on native WASAPI capture tap ($f_s = 48,000\text{ frames/s}$) prior to downsampling, $N_{\text{expected}} = 172,800,000\text{ frames}$.
- **Delivered Frames Accounting:**
  $$N_{\text{delivered}} = \sum_{k=1}^{M} n_k - N_{\text{duplicate}}$$
  where $n_k$ is the count of valid captured audio frames delivered in callback iteration $k$, and $N_{\text{duplicate}}$ is the count of duplicate/padding frames inserted during recovery.
- **Discrepancy Formula (PPM):**
  $$E_{\text{delivery}} = \frac{|N_{\text{delivered}} - N_{\text{expected}}|}{N_{\text{expected}}} \times 10^6 \quad [\text{Parts Per Million (PPM)}]$$
- **Discontinuity, Drop, Stall & Restart Accounting:**
  1. *Buffer Discontinuities:* Any occurrence of the `AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY` flag in `IAudioCaptureClient::GetBuffer` indicates dropped frames from glitching or thread starvation. Pass criterion mandates $N_{\text{discontinuity}} == 0$ (`GOVERNING REQUIREMENT`).
  2. *Silent Padding:* Flag `AUDCLNT_BUFFERFLAGS_SILENT` indicates generated silence padding; frames must be audited for gap recovery.
  3. *Callback Stalls:* Maximum inter-callback interval must satisfy $T_{\text{stall\_max}} \le 250\text{ ms}$ (`PROPOSED TARGET`).
  4. *Stream Restarts:* Zero stream restarts or re-initializations permitted ($N_{\text{restarts}} == 0$, `GOVERNING REQUIREMENT`).
- **Pass Threshold:** $E_{\text{delivery}} \le 50.0\text{ PPM}$ (`PROPOSED TARGET`), $N_{\text{discontinuity}} == 0$ (`GOVERNING REQUIREMENT`), $N_{\text{restarts}} == 0$ (`GOVERNING REQUIREMENT`), and $T_{\text{stall\_max}} \le 250\text{ ms}$ (`PROPOSED TARGET`).
- **Physical vs User-Space Limitations:**
  1. User-space frame delivery measures the rate at which the Windows audio engine (`audiodg.exe`) and user-mode buffers deliver audio to the Python worker thread.
  2. Frame discrepancy reflects thread scheduling jitter, DPC latency, and buffer queue cycling, NOT physical hardware crystal oscillator drift.
  3. Direct physical DAC crystal drift measurement requires native COM `IAudioClock::GetPosition` and `IAudioClock::GetFrequency` or external digital audio analyzer hardware, which are not accessible via standard user-mode Python bindings.
  4. Therefore, $E_{\text{delivery}}$ is an **aggregate user-space delivery discrepancy metric**, not a physical clock drift measurement.

#### Test 3: Digital Route Isolation & Physical Acoustic Leakage Screening Protocol
1. **Digital Route Isolation (Virtual Audio Driver Separation — Governed by Gate G-04):**
   - *Governing Authority:* `SPEC.md` §4.3 (Audio Routing and Feedback Prevention, Item 7).
   - *Signal Path & Routing Topology Analysis:*
     - Outbound synthesized Japanese audio is rendered to `Dev_CableIn` (VB-CABLE Input, playback endpoint).
     - VB-CABLE driver kernel-level DMA transfer bridges audio to `Dev_CableOut` (VB-CABLE Output, recording endpoint).
     - Zoom Web Client ingests `Dev_CableOut` as its microphone (`Z_MicIn`).
     - Zoom Meeting audio plays back through `Dev_Playback` (default Windows playback endpoint).
     - KoeBridge captures meeting audio via `Loopback_Cap` tapping `Dev_Playback`.
     - Under normal operation, `Dev_CableIn` and `Dev_Playback` are distinct endpoints; audio rendered to `Dev_CableIn` should produce zero digital signal on `Dev_Playback`.
     - *Leakage Failure Modes:*
       a. Windows "Listen to this device" enabled on `CABLE Output` directed to `Dev_Playback`.
       b. Realtek "Stereo Mix" or third-party audio routing suites bridging endpoints.
       c. Zoom WebRTC echo cancellation failure leaking meeting audio.
   - *Stimulus:* 1,000 Hz pure sine tone at $A_{\text{stim}} = 0.10 \implies RMS_{\text{stim}} = 0.07071$ ($L_{\text{stim}} = -20.0\text{ dBFS}$) rendered to VB-CABLE Input (`Dev_CableIn`).
   - *Capture Tap:* `Loopback_Cap` on default playback device (`Dev_Playback`).
   - *Preflight Noise Floor Criteria:*
     - $L_{\text{floor}} \le -90.0\text{ dBFS}$: Valid baseline with $\ge 10\text{ dB}$ headroom below $-80.0\text{ dBFS}$ (`GOVERNING REQUIREMENT`).
     - $-90.0\text{ dBFS} < L_{\text{floor}} \le -86.0\text{ dBFS}$: Conditional/degraded baseline (cannot yield unconditional PASS).
     - $L_{\text{floor}} > -86.0\text{ dBFS}$: INVALID / INCONCLUSIVE baseline. Test aborted.
   - *Positive Control:* Render 1,000 Hz tone to `Dev_Playback` and verify capture at $-20.0\text{ dBFS} \pm 1.5\text{ dB}$ (validates analyzer responsiveness and calibration).
   - *Isolation Calculation:* Captured level $L_{\text{cap}} \le -80.0\text{ dBFS}$ yields relative digital isolation $R_{\text{iso}} = L_{\text{stim}} - L_{\text{cap}} \ge 60.0\text{ dB}$ (`PROPOSED TARGET`).
   - *Boundary Disclosure:* High digital isolation in software drivers does not establish physical acoustic isolation in the room.
2. **Physical Acoustic Leakage Screening (Microphone Feedback Prevention — Governed by Gate G-04):**
   - *Governing Authority:* `SPEC.md` §4.3 (Audio Routing and Feedback Prevention, Item 7) & `DECISIONS.md` D-016 (Acoustic Feedback Prevention).
   - *Ambient Noise Profiling:* 10 sub-windows of 500 ms each ($K=10$, $\sigma_{\text{ambient}} < 1.0\text{ dB}$).
   - *Background-Corrected Tone Power:*
     $$P_{\text{leakage\_corrected}} = \max(0.0, RMS_{\text{playback, 1kHz}}^2 - RMS_{\text{ambient, 1kHz}}^2)$$
   - *Acoustic Leakage Ratio:*
     $$\Delta L_{\text{acoustic}} = 10 \log_{10}\left(\frac{RMS_{\text{playback, 1kHz}}^2}{\max(RMS_{\text{ambient, 1kHz}}^2, \epsilon^2)}\right)$$
     with near-zero denominator floor $\epsilon = 10^{-5}$.
   - *Screening Heuristic:* $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ over ambient noise floor (`PROPOSED TARGET`).
   - *Disclosure & Headphone Mandate:* Uncalibrated microphone dBFS measures digital quantization, not physical acoustic sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$). Spectral mismatch between narrowband 1 kHz tones and broadband room noise makes $+6.0\text{ dB}$ an unvalidated screening heuristic. Physical headphones (`Dev_Headphones`) are the mandatory primary defense (`DECISIONS.md` D-016, `GOVERNING REQUIREMENT`).

#### Test 4: Bifurcated Push-to-Talk Lifecycle & Cancellation Verification Protocol
1. **Phase 4A: Deterministic State-Machine Unit Tests (Synthetic Harness):**
   - Verify KeyDown increments monotonic `EpochID = N + 1` and transitions state `IDLE` $\to$ `ACTIVE`.
   - Verify KeyUp transitions `ACTIVE` $\to$ `INVALIDATED`, immediately purges all 5 queues (`qsize() == 0`), and sets cancellation tokens.
   - Verify synthetic worker results tagged with stale epochs are rejected and dropped ($N_{\text{stale\_rendered}} == 0$).
2. **Phase 4B: Live Windows Host Integration Tests (Live Hardware Post-M0):**
   - Hotkey ingestion target: $T_1 \le 30\text{ ms}$ (`PROPOSED TARGET`).
   - Cancellation token propagation target: $T_2 \le 60\text{ ms}$ (`PROPOSED TARGET`).
   - Microphone capture halt target: $T_3 \le 10\text{ ms}$ ($N_{\text{post\_close\_mic}} == 0$, `PROPOSED TARGET`).
   - WASAPI render buffer reset target: $T_4 \le 50\text{ ms}$ via `IAudioClient::Reset` (`PROPOSED TARGET`).
   - Polling heartbeat fallback: Terminate hook thread and verify key release detected via `GetAsyncKeyState` within $\le 50\text{ ms}$ (`GOVERNING REQUIREMENT`).
   - Circular buffer disclosure: Software queue purge (`qsize() == 0`) does not recall audio already in driver DMA buffer ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$). Non-preemptible native C++ inference will finish current tensor compute before discarding results.

---

## 8. Risk Management, Discovery Tasks & Concrete Deliverables

### 8.1 Technical & Operational Risk Register

| Risk ID | Severity | Likelihood | Risk Description & Technical Impact | Mitigation Strategy & Safeguard Reference |
|---|---|---|---|---|
| **R-01** | **CRITICAL** | HIGH | Sudden laptop shutdown under battery operation (`SPEC.md` §8) | Mandatory AC power check (`ACLineStatus == 1`) and CPU load watchdog ($\ge 95\%$ for $\ge 15\text{ s}$). Sole governing authority: SPEC §8. |
| **R-02** | **CRITICAL** | HIGH | Local Japanese TTS voice asset carries copyleft (GPL) or non-commercial terms | Multi-tier licensing audit in M0-2; separate code license from voice weights. Mandatory M0 gate. |
| **R-03** | **HIGH** | MEDIUM | Argos Translate direct JA↔EN accuracy insufficient for meeting dialogue | Evaluate MarianMT fallback in M0-3; enforce 10-sentence benchmark suite. |
| **R-04** | **HIGH** | MEDIUM | WASAPI loopback capture drops frames or drifts during long meetings | 60-minute loopback accounting test in M0-4; monitor discontinuity flags and frame delivery. |
| **R-05** | **HIGH** | LOW | Outbound Japanese audio leaks into loopback capture, creating feedback loops | AES-17 digital route isolation test in M0-5; mandate physical headphones (`DECISIONS.md` D-016). |

### 8.2 Milestone M0 Discovery Tasks (M0-1 through M0-9)

| Task ID | Task Scope | Engineering Objective & Target Outcome | Primary Output |
|---|---|---|---|
| **M0-1** | Baseline Benchmarking | Measure idle, VAD, and STT inference CPU/RAM/latency on target i7-8750H on AC power; audit wheel availability | Benchmarking logs & baseline data |
| **M0-2** | License Verification | Audit Piper, Kokoro, and Style-Bert-VITS2 voice licenses for permissive commercial terms | `docs/THIRD_PARTY_NOTICES.md` |
| **M0-3** | Direct MT Evaluation | Benchmark Argos Translate vs MarianMT on 10-sentence suite (BLEU, chrF, latency) | `docs/BENCHMARKS.md` MT section |
| **M0-4** | WASAPI Loopback Probe | Execute 60-minute continuous loopback stream stability test ($E_{\text{delivery}} \le 50.0\text{ PPM}$) | `proto_03_loopback_stress.py` log |
| **M0-5** | Route Isolation & PTT | Execute AES-17 digital isolation test and measure PTT cancellation timing | `proto_04_route_isolation.py` log |
| **M0-6** | Power & Thermal Watchdog| Implement Win32 AC power preflight check and CPU utilization watchdog | `proto_05_power_guard.py` script |
| **M0-7** | Tkinter UI Prototype | Validate Tkinter caption overlay rendering at 30 FPS without stealing focus | `proto_06_overlay_fps.py` log |
| **M0-8** | Credential Security | Validate Gemini API key storage in Windows Credential Manager via `keyring` DPAPI | `proto_07_credential_dpapi.py` log |
| **M0-9** | Discovery Synthesis | Consolidate empirical results and present formal recommendations for Gate Clearance | `docs/M0_DISCOVERY_REPORT.md` |

### 8.3 Concrete Milestone M0 Deliverables (DEL-01 through DEL-05)
- **DEL-01:** `docs/M0_DISCOVERY_REPORT.md` (Comprehensive findings dossier covering all 9 discovery tasks).
- **DEL-02:** `docs/THIRD_PARTY_NOTICES.md` (Multi-tier software and model asset license manifest).
- **DEL-03:** `docs/BENCHMARKS.md` (Empirical latency, CPU, RAM, and translation quality records on target hardware).
- **DEL-04:** 7 Discovery Prototype Scripts (`prototypes/m0_discovery/proto_01_*.py` through `proto_07_*.py`).
- **DEL-05:** Formal Owner Decision Gate Package (Clearance recommendations for Gates G-01 through G-04).

---

## 9. Canonical Gate-Indexed Unresolved Evidence Register

All four release gates remain strictly **EMPIRICAL GATES OPEN** pending empirical measurement. The table below reconstructs the complete release-gate register:

| Target Gate | Gate Name & Governing Authority | Mapped Gaps & Items | Mandatory Closure Criteria | Required Verification Evidence | Empirical vs Documentary Requirements | Current Status & Blockers |
|---|---|---|---|---|---|---|
| **Gate G-01** | Permissive Japanese TTS Engine & Voice Licensing Clearance (`SPEC.md` §5, `DECISIONS.md` D-003, D-005) | GAP-01, GAP-13, GAP-15 (Items U-01, U-13, U-15) | 1. Standalone TTS runnable locally on CPU.<br/>2. Code licensed under MIT/Apache/BSD.<br/>3. Voice weights independently verified permissive.<br/>4. RTF $\le 0.50$ on i7-8750H.<br/>5. Python wheels verified for Win x64.<br/>6. Repository MIT `LICENSE` committed. | 1. `docs/THIRD_PARTY_NOTICES.md` license manifest.<br/>2. RTF CPU benchmark log.<br/>3. PyPI wheel verification log.<br/>4. Committed `LICENSE` file. | Documentary: License text verification.<br/>Empirical: RTF latency on AC power. | **EMPIRICAL GATE OPEN**.<br/>Blockers: No permissive voice cleared; M0 unauthorized. |
| **Gate G-02** | Direct JA↔EN Machine Translation Quality & Latency Clearance (`SPEC.md` §5.2, `DECISIONS.md` D-006) | GAP-02, GAP-07 (Items U-02, U-07) | 1. Direct JA↔EN translation (no pivot).<br/>2. SacreBLEU $\ge 25.0$, chrF++ $\ge 0.50$ on 10-sentence dialogue suite.<br/>3. Latency $\le 600\text{ ms}$ on CPU.<br/>4. Zero catastrophic mistranslations.<br/>5. Offline Local Mode default verified.<br/>6. Sequential Cloud Opt-In fallback verified. | 1. `docs/BENCHMARKS.md` MT section with BLEU/chrF logs.<br/>2. MarianMT comparison logs.<br/>3. Socket audit confirming zero egress in Local Mode.<br/>4. Cloud 2.50 s timeout log. | Documentary: Prompt/model architecture review.<br/>Empirical: BLEU/chrF/latency on hardware. | **EMPIRICAL GATE OPEN**.<br/>Blockers: Unmeasured MT quality; M0 unauthorized. |
| **Gate G-03** | End-to-End Pipeline Latency & Host Hardware Thermal/Power Guardrails (`SPEC.md` §8, `DECISIONS.md` D-025) | GAP-03, GAP-08, GAP-09, GAP-10, GAP-12 (Items U-03, U-08, U-09, U-10, U-12) | 1. Inbound budget $\le 1,800\text{ ms}$ ($2,400\text{ ms}$ max).<br/>2. Outbound budget $\le 2,100\text{ ms}$ ($2,900\text{ ms}$ max).<br/>3. STT latency $\le 800\text{ ms}$ on CPU.<br/>4. VAD latency $\le 5.0\text{ ms}$ on CPU.<br/>5. AC power preflight (`ACLineStatus == 1`).<br/>6. CPU watchdog ($\ge 95\%$ for $\ge 15\text{ s}$).<br/>7. Gemini key DPAPI storage. | 1. Timestamped pipeline latency traces in `BENCHMARKS.md`.<br/>2. STT/VAD component logs.<br/>3. Win32 AC power preflight test log.<br/>4. Watchdog load test log.<br/>5. `keyring` DPAPI verification log. | Documentary: Code review of watchdog & DPAPI.<br/>Empirical: End-to-end latency on AC power. | **EMPIRICAL GATE OPEN**.<br/>Blockers: Unmeasured pipeline latency; M0 unauthorized. |
| **Gate G-04** | Audio Endpoint Topology, Loopback Stability & PTT Safety Verification (`SPEC.md` §4.1–§4.3, `DECISIONS.md` D-016, D-023) | GAP-04, GAP-05, GAP-06, GAP-11, GAP-14 (Items U-04, U-05, U-06, U-11, U-14) | 1. Device enumeration and negotiation.<br/>2. 60-min loopback stream: $E_{\text{delivery}} \le 50.0\text{ PPM}$, zero discontinuities, zero restarts, $T_{\text{stall\_max}} \le 250\text{ ms}$.<br/>3. AES-17 digital isolation $R_{\text{iso}} \ge 60.0\text{ dB}$.<br/>4. Acoustic leakage $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$.<br/>5. PTT: queue purge (`qsize() == 0`), mic halt $\le 10\text{ ms}$, reset $\le 50\text{ ms}$, 50 ms polling fallback.<br/>6. Tkinter overlay rendering at $\ge 30\text{ FPS}$ without focus loss. | 1. 60-minute loopback log.<br/>2. AES-17 sine test log.<br/>3. Acoustic screening log.<br/>4. PTT timing traces ($T_1..T_4$).<br/>5. Polling fallback test log.<br/>6. Tkinter 30 FPS overlay log. | Documentary: State-machine test review.<br/>Empirical: 60-min audio streaming & PTT timing. | **EMPIRICAL GATE OPEN**.<br/>Blockers: Unmeasured audio stability; M0 unauthorized. |

---

## 10. Proposed SPEC Amendments & DECISIONS Records

All proposed amendments to `SPEC.md` and proposed additions to `DECISIONS.md` are documented below. Every item is formally classified as **PROPOSED — NOT APPLIED**, pending explicit review and approval by the project owner. Exactly **10 unique proposal IDs** are defined across these categories (4 SPEC amendments + 6 ADRs).

### 10.1 Proposed SPEC.md Amendments (Pending Owner Review — 4 Unique Items)

1. **Amendment C-01: Explicit Host Power & CPU Preflight Guardrail (`SPEC.md` §1)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Affected Authority:* `SPEC.md` §1 (System Architecture & Principles).
   - *Proposed Text & Rationale:* "Host execution requires verified plugged-in AC power (`ACLineStatus == 1`). If the host is running on battery power, benchmarking and live translation pipelines must abort immediately to prevent sudden system power shutdown (`SPEC.md` §8). A background watchdog must monitor CPU load and abort or throttle the pipeline if CPU utilization reaches $\ge 95\%$ sustained for $\ge 15\text{ s}$."

2. **Amendment C-02: Quantitative Direct Translation Evaluation Protocol (`SPEC.md` §5.2)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Affected Authority:* `SPEC.md` §5.2 (Machine Translation Engine Requirements).
   - *Proposed Text & Rationale:* "Machine translation engines must be evaluated using the 10-sentence dialogue benchmark suite (TC-01 through TC-10) in M0. Direct JA$\leftrightarrow$EN models must achieve BLEU $\ge 25.0$, chrF $\ge 0.50$, inference latency $\le 600\text{ ms}$ on CPU, and zero catastrophic mistranslations on negations, numbers, and technical terms. Pivot translation via intermediate languages is prohibited (`DECISIONS.md` D-006). If Argos Translate fails these thresholds, MarianMT must be evaluated as an immediate local fallback."

3. **Amendment C-03: Acoustic Feedback & Virtual Routing Disentanglement (`SPEC.md` §4.3)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Affected Authority:* `SPEC.md` §4.3 (Audio Routing & Virtual Mic Delivery).
   - *Proposed Text & Rationale:* "Physical headphones (`Dev_Headphones`) are mandatory for all meeting participants using KoeBridge to physically isolate inbound playback from outbound microphone capture (`DECISIONS.md` D-016). Inbound WASAPI loopback capture must never be unconditionally suppressed during outbound push-to-talk speech (`SPEC.md` §4.3). Virtual audio injection into VB-CABLE Input must achieve $\ge 60\text{ dB}$ digital isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) against the loopback capture tap under AES-17 sine stimulus testing."

4. **Amendment C-04: Strict Local-First Privacy & Opt-In Cloud Governance Protocol (`SPEC.md` §1, §5.3)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Affected Authority:* `SPEC.md` §1 (Local-First Privacy) and §5.3 (Optional Cloud LLM Enhancement).
   - *Proposed Text & Rationale:* "The application must operate in one of two mutually exclusive modes:
     1. Local Mode (Default): Strictly offline; zero socket egress; zero external telemetry or transcript transmission; local MT only; local translation failures produce explicit user-visible error states; automatic silent fallback to cloud is strictly prohibited. Local processing slowness or load must never trigger cloud offloading.
     2. Cloud Opt-In Mode (Disabled Default): Requires explicit, informed user consent; provider data terms must be tracked as an open release gate; requests enforce a 2.50 s timeout and monotonic correlation IDs ($\text{CorrID} = \langle \text{SessionID}, \text{EpochID}, \text{SegmentSeq} \rangle$); sequential fallback to local on cloud failure if user enabled fallback setting; late cloud responses for invalidated epochs must be cancelled and discarded."

### 10.2 Proposed DECISIONS.md Records (Pending Owner Approval — 6 Unique Items)

1. **Decision D-028: Preflight AC Power Check and CPU Load-Abort Watchdog**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records). *(Not an approved governing decision; SPEC.md §8 is the sole governing authority.)*
   - *Context & Rationale:* Target hardware (i7-8750H) exhibits sudden battery power loss under high load. Plugged-in AC power must be verified via Win32 `GetSystemPowerStatus` (`ACLineStatus == 1`) prior to benchmark or pipeline execution. A software watchdog must enforce a $\ge 95\%$ CPU threshold for $\ge 15\text{ s}$ to protect host operating system stability.

2. **Decision D-029: Comparative Argos Translate vs MarianMT Evaluation Protocol**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records).
   - *Context & Rationale:* Direct JA$\leftrightarrow$EN translation quality must be quantitatively verified using the 10-sentence dialogue benchmark suite (TC-01..TC-10). If Argos Translate fails accuracy or latency thresholds, MarianMT (`Helsinki-NLP/opus-mt-ja-en` / `en-jap`) must be evaluated as local fallback before considering any external API.

3. **Decision D-030: Acoustic Feedback Policy Mandating Physical Headphones**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records).
   - *Context & Rationale:* Primary defense against acoustic feedback is physical device separation via headphones (`Dev_Headphones`). Inbound loopback capture must never be unconditionally suppressed during outbound speech to ensure meeting participants can hear overlapping cross-talk (`SPEC.md` §4.3). Digital route isolation must be verified via AES-17 sine stimulus testing.

4. **Decision D-031: Dual-Signal PTT Supervision & Downstream Cancellation Architecture**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records).
   - *Context & Rationale:* Global push-to-talk hotkeys must be supervised using both Win32 `WH_KEYBOARD_LL` low-level hooks and a 50 ms `GetAsyncKeyState` polling heartbeat to prevent stuck transmit states. KeyUp events must increment the monotonic epoch ID, immediately purge all outbound speech queues ($qsize() == 0$), halt microphone capture within $\le 10\text{ ms}$, reset audio render within $\le 50\text{ ms}$, and discard stale worker outputs.

5. **Decision D-032: Multi-Tier Licensing & Independent Model Asset Clearance Policy**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records).
   - *Context & Rationale:* Runtime code wrapper licenses must be evaluated independently from neural network model weights, acoustic checkpoints, and training data provenance. The maintained `OHF-Voice/piper1-gpl` package is GPL-3.0-or-later and unapproved by default (`SPEC.md` §5). Permissive local Japanese TTS voice clearance is a mandatory M0 release gate. Kokoro voice checkpoints require independent clearance regardless of Apache 2.0 code licenses. Python runtime must be selected based on pre-compiled wheel availability (3.11/3.12 vs 3.13).

6. **Decision D-033: Strict Local-First Privacy & Explicit Opt-In Cloud Governance Protocol**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Affected Authority:* `DECISIONS.md` (Architecture Decision Records).
   - *Context & Rationale:* Formalizes the separation between Local Mode (100% offline default, zero socket egress, explicit error states) and Cloud Opt-In Mode (disabled by default, explicit consent, provider terms tracked as gate, 2.50 s timeout, local fallback option, cancellation on epoch invalidation, monotonic correlation IDs).

---

## 11. Reconciled Historical Defect Register (D-01 through D-33)

The table below reconciles all 33 historical defects, applying a strict 5-tier status taxonomy:
- **CORRECTED IN DOCUMENT:** Exactly 28 unique items (84.8%: D-01 through D-12, D-16 through D-23, D-25 through D-29, D-31 through D-33).
- **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED:** Exactly 5 unique items (15.2%: D-13, D-14, D-15, D-24, D-30).
- **EMPIRICALLY TESTED — EVIDENCE ATTACHED:** Exactly 0 items (0.0%).
- **OWNER-APPROVED:** Exactly 0 items (0.0%).
- **UNVERIFIED / UNRESOLVED:** Exactly 0 items (0.0%).

| Defect ID | Historical Defect Description | Location in Plan | Verification Method | Grounded Status | Evidence, Justification & Remaining Limitations |
|---|---|---|---|---|---|
| **D-01** | Missing AC power requirement and thermal safety protocol | §1.1, §7.3, §8.1, §10.1 (C-01), §10.2 (D-028) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Factually grounded in `SPEC.md` §8 as an observed hardware risk (`ACLineStatus == 1`). C-01 and D-028 documented and marked NOT APPLIED. Speculative thermal overload assertions eliminated. |
| **D-02** | Unclear machine translation evaluation criteria and quality gates | §6.1, §7.2 (G-02), §10.1 (C-02), §10.2 (D-029) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | 10-sentence dialogue benchmark suite (TC-01..TC-10) with 4-tier rubric fully specified. Disclosed as a preliminary smoke test, with 100+ dialogue corpus required for full validation. |
| **D-03** | Incomplete audio routing and acoustic feedback isolation rules | §3.4.1, §7.4 (Test 3), §10.1 (C-03), §10.2 (D-030) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Physical headphones mandated as primary defense (`DECISIONS.md` D-016). Unconditional loopback suppression during cross-talk strictly prohibited (`SPEC.md` §4.3). Disentanglement rules fully codified. |
| **D-04** | Ambiguous push-to-talk state machine and queue purging semantics | §3.4.3, §7.4 (Test 4), §10.2 (D-031) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Dual-signal supervision (`WH_KEYBOARD_LL` + 50 ms polling) specified. KeyUp transitions to `INVALIDATED` epoch, purging all queues ($qsize() == 0$). Driver DMA buffer limits ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$) disclosed. |
| **D-05** | Licensing ambiguity regarding TTS voices and Piper GPL status | §6.0, §7.1 (G-01), §10.2 (D-032) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Aligned with `SPEC.md` §5 and `DECISIONS.md` D-003/D-005. `OHF-Voice/piper1-gpl` identified as GPL-3.0 and unapproved by default. Local Japanese TTS identified as a mandatory MVP hard gate. |
| **D-06** | Undefined cloud translation opt-in protocol and privacy boundaries | §3.4.2, §7.2, §10.1 (C-04), §10.2 (D-033) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Two distinct operating modes established: Local Mode (strictly offline default, zero socket egress, no silent fallback) and Cloud Opt-In Mode (sequential fallback, explicit consent, provider terms tracked as gate, correlation IDs, 2.50 s timeout). |
| **D-07** | Incomplete M0 task breakdown and missing discovery deliverables | §8.2, §8.3 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Nine specific discovery tasks (M0-1 through M0-9) and five concrete deliverables (DEL-01 through DEL-05) fully defined with acceptance criteria. |
| **D-08** | Inconsistent release gate definitions across document sections | §7.1–§7.4, §9.0 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | All four release gates (G-01 through G-04) standardized with identical criteria, verification procedures, and EMPIRICAL GATE OPEN statuses across all sections. |
| **D-09** | Missing quantitative pass/fail thresholds for latency and quality | §7.1–§7.4 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Quantitative thresholds established: TTS RTF $\le 0.50$, MT latency $\le 600\text{ ms}$, STT latency $\le 800\text{ ms}$, VAD latency $\le 5.0\text{ ms}$, inbound pipeline budget $\le 1,800\text{ ms}$, outbound budget $\le 2,100\text{ ms}$, digital isolation $\ge 60\text{ dB}$. |
| **D-10** | Unrealistic zero-latency claims for virtual audio driver injection | §3.4.3, §7.4 (Test 4) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Explicitly acknowledges that audio committed to kernel virtual driver DMA circular buffers ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$) cannot be recalled by user-space code. Zero-latency claims eliminated. |
| **D-11** | Conflation of runtime code licenses with neural network weights | §6.0, §10.2 (D-032) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Multi-tier licensing framework explicitly separates Python runtime code licenses from neural network model weights, acoustic checkpoints, and training data provenance. |
| **D-12** | Missing fallback strategy if Argos Translate quality is unacceptable | §6.1, §7.2 (G-02) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | MarianMT (`Helsinki-NLP/opus-mt-ja-en` and `en-jap`) explicitly specified as local fallback candidate if Argos fails accuracy thresholds, evaluated under the same 10-sentence benchmark. |
| **D-13** | Lack of explicit preflight checks for physical audio hardware | §7.4 (Test 1, Test 2A, Test 3) | Plan Text Inspection | **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED** | Preflight procedures for WASAPI endpoint enumeration, format negotiation, and noise floor calibration are fully specified in the plan, but physical execution is deferred to M0 discovery. |
| **D-14** | Absence of 60-minute loopback capture stream stability test | §7.4 (Test 2B) | Plan Text Inspection | **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED** | 60-minute loopback stability protocol measuring aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$), buffer discontinuities, and callback stalls is fully specified, but execution awaits M0-4 on live hardware. |
| **D-15** | Incomplete AES-17 digital route isolation test protocol | §7.4 (Test 3) | Plan Text Inspection | **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED** | AES-17 1,000 Hz sine stimulus ($-20.0\text{ dBFS}$) rendered to `Dev_CableIn` with capture tap on `Loopback_Cap` on `Dev_Playback` fully specified. Preflight noise floor criteria and positive control defined. Physical test execution awaits M0-5. |
| **D-16** | Unsubstantiated claims of machine verification in integrity audits | §14.0 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Integrity audit explicitly reports manual document inspection methods, formally disclaims automated mechanical tooling, and records grounded statuses. |
| **D-17** | Mismatched node identifiers between architecture diagram and text | §3.1, §3.2, §3.3 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | 1:1:1 mathematical parity achieved across diagram, node register, and edge register: exactly 33 unique nodes (`N-01`..`N-33`) and 44 unique edges (`E-01`..`E-44`). |
| **D-18** | Missing edge identifiers and incomplete connection declarations | §3.3 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | All 44 edges (`E-01` through `E-44`) uniquely declared with explicit source, target, data type, protocol/mechanism, and directional pipeline classification. |
| **D-19** | Truncation of Section 15 milestone blockers and technical gaps | §15.1, §15.2 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Complete text restored: all milestone blockers (M0 through M7) including M1 row restored in full; all 15 canonical gaps (GAP-01 through GAP-15) fully articulated. |
| **D-20** | Broken acoustic leakage background correction formula | §7.4 (Test 3) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Repaired formula to $P_{\text{leakage\_corrected}} = \max(0.0, RMS_{\text{playback, 1kHz}}^2 - RMS_{\text{ambient, 1kHz}}^2)$ with near-zero denominator floor $\epsilon = 10^{-5}$. Narrowband vs broadband spectral mismatch disclosed. |
| **D-21** | Ambiguous baseline noise floor threshold criteria in audio tests | §7.4 (Test 3) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Categorized noise floor into three unambiguous ranges: $\le -90\text{ dBFS}$ valid; $-90$ to $-86\text{ dBFS}$ conditional/degraded (cannot yield unconditional PASS); $> -86\text{ dBFS}$ invalid/inconclusive. |
| **D-22** | Conflation of digital ADC dBFS with physical sound pressure (dB SPL) | §7.4 (Test 3) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Explicitly discloses that uncalibrated microphone dBFS measures digital quantization, not physical acoustic sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$). Headphone mandate reinforced. |
| **D-23** | Attributing aggregate frame discrepancies directly to hardware clock drift | §7.4 (Test 2B) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Metric designated as **aggregate frame-delivery discrepancy** ($E_{\text{delivery}} \le 50.0\text{ PPM}$). Discloses that user-space code lacks native COM `IAudioClock` access. Marked threshold as provisional. |
| **D-24** | Conflation of PTT unit test assertions with Windows integration tests | §7.4 (Test 4) | Plan Text Inspection | **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED** | PTT testing bifurcated into Phase 4A (deterministic state-machine unit tests in mock harness) and Phase 4B (live Windows integration tests post-M0). Unit harness fully designed; live validation awaits M0-5. |
| **D-25** | Tautological assertions in PTT test specifications | §7.4 (Test 4) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Replaced tautological self-referential assertions with explicit queue empty assertions (`qsize() == 0`), worker drop counts ($N_{\text{stale\_rendered}} == 0$), and timed state transitions. |
| **D-26** | Lack of disclosure regarding non-preemptible native C++ inference | §3.4.3, §7.4 (Test 4) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Explicitly documents that in-flight CTranslate2 and ONNX Runtime tensor execution cannot be safely interrupted mid-inference without memory corruption, and that downstream epoch invalidation discards output instead. |
| **D-27** | Missing Win32 hook suspension disclosure during secure desktop switches | §3.4.3, §7.4 (Test 4) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Explicitly documents that `WH_KEYBOARD_LL` hooks stop receiving Windows messages during UAC prompts and Winlogon desktop switches, necessitating 50 ms polling heartbeat supervision. |
| **D-28** | Misalignment of Piper licensing status with SPEC.md | §6.0, §7.1 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Aligned strictly with `SPEC.md` §5: `OHF-Voice/piper1-gpl` is GPL-3.0-or-later and unapproved by default under the permissive-first policy. Non-GPL fallback requirement established. |
| **D-29** | Inconsistent definition of local Japanese TTS as optional vs mandatory gate | §6.0, §7.1, §15.2 (GAP-01) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Confirmed as a mandatory MVP release gate per `SPEC.md` §5 and `DECISIONS.md` D-005. An unapproved voice is a hard release blocker. |
| **D-30** | Assuming Python 3.13 binary wheel compatibility without verification | §6.0, §15.2 (GAP-13) | Plan Text Inspection | **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED** | Plan updated to mandate checking CTranslate2, PyAudioWPatch, and onnxruntime pre-compiled wheels for Windows x64 in M0-1, with fallback to pinned Python 3.11/3.12. Physical PyPI audit pending M0-1. |
| **D-31** | Unverifiable claims of repository licensing compliance | §13.0, §15.2 (GAP-15) | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Correctly reports that `LICENSE` is missing on disk. Tracked as open gap GAP-15 / item U-15. Unsubstantiated compliance claims eliminated. |
| **D-32** | Fractured bidirectional traceability between unresolved items and gaps | §12.2, §12.3, §15.2 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | Complete 1:1 bidirectional alignment established across all 15 items (U-01..U-15) and canonical gaps (GAP-01..GAP-15) across forward and reverse matrices. |
| **D-33** | Premature declaration of Milestone M0 authorization | §1.1, §1.2, §15.1, §15.5 | Plan Text Inspection | **CORRECTED IN DOCUMENT** | M0 explicitly declared UNAUTHORIZED pending explicit project owner approval. All release gates maintained strictly EMPIRICAL GATES OPEN. Planning-only boundary enforced. |

**Audit Metrics:**
- **Total Historical Defects Audited:** Exactly 33 unique items (D-01 through D-33).
- **CORRECTED IN DOCUMENT:** Exactly 28 unique items (84.8%: D-01 through D-12, D-16 through D-23, D-25 through D-29, D-31 through D-33).
- **PROTOCOL SPECIFIED — EMPIRICAL EXECUTION DEFERRED:** Exactly 5 unique items (15.2%: D-13, D-14, D-15, D-24, D-30).
- **EMPIRICALLY TESTED — EVIDENCE ATTACHED:** Exactly 0 items (0.0%).
- **OWNER-APPROVED:** Exactly 0 items (0.0%).
- **UNVERIFIED / UNRESOLVED:** Exactly 0 items (0.0%).
- **Total Reconciled:** $28 + 5 = 33$ items (100.0%). Discrepancy eliminated; zero repetition of D-01.

---

## 12. Unresolved Items Register & Bidirectional Traceability

### 12.1 Unresolved Engineering Items Register (U-01 through U-15)

| Item ID | Target Release Gate | Subsystem Domain | Unresolved Technical Challenge & Target Verification Standard | Planned Resolution Task |
|---|---|---|---|---|
| **U-01** | Gate G-01 | Japanese Voice Synthesis | Permissive Japanese TTS engine and voice asset clearance under non-GPL license | Task M0-2 (`THIRD_PARTY_NOTICES.md`) |
| **U-02** | Gate G-02 | Machine Translation | Direct JA↔EN translation accuracy and latency validation on 10-sentence dialogue suite | Task M0-3 (Argos vs MarianMT) |
| **U-03** | Gate G-03 | Host Safety & Power | Plugged-in AC power preflight verification and CPU watchdog threshold enforcement | Task M0-6 (AC check & watchdog) |
| **U-04** | Gate G-04 | Audio Capture Routing | PyAudioWPatch loopback enumeration and 60-minute stream stability ($E_{\text{delivery}} \le 50.0\text{ PPM}$) | Task M0-4 (60-min loopback test) |
| **U-05** | Gate G-04 | Virtual Driver Injection | VB-CABLE render stability and dual-signal PTT hotkey lifecycle verification | Task M0-5 (PTT & VB-CABLE probe) |
| **U-06** | Gate G-04 | Acoustic Feedback Defense | Physical headphone mandate enforcement and acoustic leakage screening verification | Task M0-5 (Acoustic leakage screening) |
| **U-07** | Gate G-02 | Privacy & Translation Mode | Strict Local Mode offline enforcement and Cloud Opt-In Mode sequential arbitration | Task M0-3 / Proposed Decision D-033 |
| **U-08** | Gate G-03 | Speech Recognition | `faster-whisper` `small` `int8` CPU transcription latency ($\le 800\text{ ms}$) on target hardware | Task M0-1 (Whisper benchmark) |
| **U-09** | Gate G-03 | Speech Segmentation | Silero VAD ONNX Runtime chunk processing latency ($\le 5.0\text{ ms}$) on target CPU | Task M0-1 (VAD benchmark) |
| **U-10** | Gate G-03 | Pipeline Budget | Inbound ($\le 1,800\text{ ms}$) and outbound ($\le 2,100\text{ ms}$) end-to-end latency budget clearance | Task M0-6 (End-to-end integration) |
| **U-11** | Gate G-04 | Presentation UI | Tkinter overlay window rendering at $\ge 30\text{ FPS}$ without stealing user input focus | Task M0-7 (Tkinter GUI prototype) |
| **U-12** | Gate G-03 | Credential Security | Secure storage of Gemini API key in Windows Credential Manager via `keyring` DPAPI | Task M0-8 (`keyring` probe) |
| **U-13** | Gate G-01 | Runtime Compatibility | Verification of pre-compiled Windows x64 binary wheels for Python 3.11/3.12 vs 3.13 | Task M0-1 (PyPI wheel audit) |
| **U-14** | Gate G-04 | Audio Isolation | Verification of $\ge 60\text{ dB}$ digital route isolation under AES-17 sine stimulus testing | Task M0-5 (Digital route isolation) |
| **U-15** | Gate G-01 | Repository Governance | Creation and commitment of repository MIT `LICENSE` file on disk | Pre-M1 Owner Review Action |

### 12.2 Forward Traceability Matrix (U-01..U-15 to GAP-01..GAP-15 to Gates)

| Unresolved Item | Canonical Technical Gap | Governing Release Gate | Planned Resolution Task | Milestone Owner | Target Acceptance Standard |
|---|---|---|---|---|---|
| **U-01** | **GAP-01** (Permissive JA TTS & Voice Licensing) | Gate G-01 | Task M0-2 | Milestone M0 | Permissive non-GPL TTS voice verified with $\text{RTF} \le 0.50$ (`PROPOSED TARGET`) |
| **U-02** | **GAP-02** (Direct JA↔EN MT Quality & Latency) | Gate G-02 | Task M0-3 | Milestone M0 | BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$, zero critical errors (`PROPOSED TARGETS`) |
| **U-03** | **GAP-03** (Host Power Mandate & CPU Watchdog) | Gate G-03 | Task M0-6 | Milestone M0 | AC power check (`ACLineStatus == 1`, `GOVERNING REQUIREMENT`); watchdog at $\ge 95\%$ CPU for $\ge 15\text{ s}$ (`PROPOSED TARGET`) |
| **U-04** | **GAP-04** (WASAPI Loopback Capture Stability) | Gate G-04 | Task M0-4 | Milestone M0 | 60-min loopback stream with $E_{\text{delivery}} \le 50.0\text{ PPM}$ (`PROPOSED TARGET`), zero discontinuities (`GOVERNING REQUIREMENT`) |
| **U-05** | **GAP-05** (VB-CABLE Injection & PTT Safety) | Gate G-04 | Task M0-5 | Milestone M0 | Dual-signal PTT; KeyUp queue purge; mic halt $\le 10\text{ ms}$; render reset $\le 50\text{ ms}$ (`PROPOSED TARGETS`) |
| **U-06** | **GAP-06** (Acoustic Feedback & Headphone Mandate) | Gate G-04 | Task M0-5 | Milestone M0 | Physical headphones mandated (`GOVERNING REQUIREMENT`); loopback not suppressed; leakage $\le +6.0\text{ dB}$ (`PROPOSED TARGET`) |
| **U-07** | **GAP-07** (Dual-Mode Privacy & Cloud Arbitration) | Gate G-02 | Task M0-3 | Milestone M0 | Offline Local Mode default (`GOVERNING REQUIREMENT`); sequential cloud fallback; 2.50 s timeout; correlation tokens |
| **U-08** | **GAP-08** (STT Latency & Quantization Clearance) | Gate G-03 | Task M0-1 | Milestone M0 | `faster-whisper` `small` `int8` CPU transcription latency $\le 800\text{ ms}$ (`GOVERNING REQUIREMENT`) |
| **U-09** | **GAP-09** (VAD Latency & Chunk Segmentation) | Gate G-03 | Task M0-1 | Milestone M0 | Silero VAD ONNX Runtime processing 30 ms chunks in $\le 5.0\text{ ms}$ on CPU (`GOVERNING REQUIREMENT`) |
| **U-10** | **GAP-10** (End-to-End Latency Budget Clearance) | Gate G-03 | Task M0-6 | Milestone M0 | Inbound latency $\le 1,800\text{ ms}$ target; outbound speech latency $\le 2,100\text{ ms}$ target (`GOVERNING REQUIREMENTS`) |
| **U-11** | **GAP-11** (Tkinter GUI Responsiveness & Focus) | Gate G-04 | Task M0-7 | Milestone M0 | Tkinter caption overlay rendering at $\ge 30\text{ FPS}$ without stealing user focus (`GOVERNING REQUIREMENT`) |
| **U-12** | **GAP-12** (Secure Credential Storage via DPAPI) | Gate G-03 | Task M0-8 | Milestone M0 | Gemini API key stored in Windows Credential Manager via `keyring` DPAPI backend (`DECISIONS.md` D-027, `GOVERNING REQUIREMENT`) |
| **U-13** | **GAP-13** (Python Runtime & Wheel Compatibility) | Gate G-01 | Task M0-1 | Milestone M0 | Windows x64 binary wheels verified on PyPI; pin 3.11/3.12 if 3.13 lacks wheels |
| **U-14** | **GAP-14** (Digital Route Isolation Verification) | Gate G-04 | Task M0-5 | Milestone M0 | AES-17 1 kHz sine achieving digital isolation $L_{\text{iso}} \le -80.0\text{ dBFS}$ ($\ge 60\text{ dB}$) (`PROPOSED TARGET`) |
| **U-15** | **GAP-15** (Repository License File Absence) | Gate G-01 | Pre-M1 Governance | Project Owner | Commit MIT `LICENSE` file to repository root prior to Milestone M1 (`CLAUDE.md` policy) |

### 12.3 Reverse Traceability Matrix (Release Gates to Canonical Gaps to Items)

| Governing Release Gate | Release Gate Name & Authority | Mapped Canonical Gaps | Mapped Unresolved Items | Target Milestone | Gate Acceptance Standard |
|---|---|---|---|---|---|
| **Gate G-01** | Permissive Japanese TTS & Voice Licensing (`SPEC.md` §5, D-003, D-005) | GAP-01, GAP-13, GAP-15 | U-01, U-13, U-15 | Milestone M0 / Pre-M1 | Permissive non-GPL TTS engine & voice asset manifest (`THIRD_PARTY_NOTICES.md`), wheel audit, and MIT `LICENSE` commit. (3 Gaps) |
| **Gate G-02** | Direct JA↔EN MT Quality & Latency (`SPEC.md` §5.2, D-006) | GAP-02, GAP-07 | U-02, U-07 | Milestone M0 | 10-sentence dialogue benchmark passing scores (BLEU $\ge 25.0$, chrF $\ge 0.50$, $\le 600\text{ ms}$), zero critical errors, and offline Local Mode default. (2 Gaps) |
| **Gate G-03** | End-to-End Latency & Thermal/Power (`SPEC.md` §8, D-025) | GAP-03, GAP-08, GAP-09, GAP-10, GAP-12 | U-03, U-08, U-09, U-10, U-12 | Milestone M0 | Inbound $\le 1,800\text{ ms}$, outbound $\le 2,100\text{ ms}$, AC power verification (`ACLineStatus == 1`), CPU watchdog, and DPAPI keyring. (5 Gaps) |
| **Gate G-04** | Audio Routing, Loopback & PTT Safety (`SPEC.md` §4.1–§4.3, D-016, D-023) | GAP-04, GAP-05, GAP-06, GAP-11, GAP-14 | U-04, U-05, U-06, U-11, U-14 | Milestone M0 | 60-min loopback stability ($E_{\text{delivery}} \le 50.0\text{ PPM}$), AES-17 digital isolation $\ge 60\text{ dB}$, acoustic feedback screening, dual PTT supervision, and 30 FPS UI. (5 Gaps) |

*(Summary: Gate distribution is closed and mutually exclusive: $3 + 2 + 5 + 5 = 15$ canonical gaps mapped to 15 unresolved items across 4 release gates. Acoustic Feedback Prevention GAP-06/U-06 and Digital Route Isolation GAP-14/U-14 are formally reconciled to Gate G-04 per SPEC.md §4.3 and DECISIONS.md D-016.)*

---

## 13. Planning-Only Compliance & Grounded Repository State

Direct inspection of the repository workspace confirms the following facts:
1. **Accurate Categorized Filesystem Accounting:**
   - *New Files Created:* Exactly two new documentation files created during this revision (`docs/ARCHITECTURE_R60.md` and `docs/ARCHITECTURE_R60_REVIEW.md`). Zero application source code files (`src/`), zero prototype scripts (`prototypes/`), and zero automated test files (`tests/`) have been created.
   - *Existing Project Files Modified:* Zero predecessor architecture plans or reviews (`R44` through `R59`) were modified. All predecessors remain preserved on disk.
   - *Governing Files Modified:* ZERO governing files modified. `SPEC.md` (40,372 bytes, 436 lines, SHA-256 `20f2344a34c6a027a118a256d043407cb134511163e45731895e949300dbeb8e`), `DECISIONS.md` (6,661 bytes, 35 lines, SHA-256 `9cde0a3ba26d792504611f75f1374ca64d5aaf0bbd906c7f03121e7a5b81329b`), and `CLAUDE.md` (3,356 bytes, 42 lines, SHA-256 `5d6139eb743cc723103f794b6f033821aaf7a86bac740cf219c313adb89beb0d`) remain completely untouched since October 13, 2026.
   - *Packages Installed:* ZERO packages installed via pip, conda, winget, or manual wheel setup.
   - *Model Assets Downloaded:* ZERO neural network weights, checkpoints, vocoders, or tokenizers downloaded.
   - *Hardware Accessed:* ZERO audio endpoints, loopback taps, or microphone hardware opened or queried.
2. **Missing License File Disclosed:** Direct disk inspection confirms that NO `LICENSE` file exists in the repository root. This absence is tracked as open gap **GAP-15** (item **U-15**) and must be resolved by committing an MIT license upon owner authorization prior to M1.
3. **Absence of Git Repository Disclosed:** Inspection confirms that `E:\Projects\VSCode\PostOmniroute\KoeBridge-for-Zoom` does not contain a `.git` directory (`fatal: not a git repository`). Therefore, independent external git commit baseline evidence is unavailable on disk, and comparisons against external baseline commits are qualified as `UNVERIFIED FROM SUPPLIED EVIDENCE`.

---

## 14. Grounded 14-Check Integrity Audit Table

The table below reports the final integrity audit of Revision 60, applying the strict 5-tier status taxonomy (`VERIFIED`, `PARTIALLY VERIFIED`, `FAILED`, `BLOCKED`, `NOT EMPIRICALLY TESTED`):

| Check ID | Integrity Dimension | Target Scope | Verification Method | Grounded Status | Detailed Finding & Specific Evidence Location | Limitations & Remaining Work |
|---|---|---|---|---|---|---|
| **CHK-01** | Debris & Artifact Purge | Entire Document Text | Manual Regex Search / Visual Scan | **VERIFIED** | Zero reasoning tokens, terminal commands, or conversational artifacts present in saved disk files (`R60`, `R59`, `R58`, `R57`, `R56`, `R55`, `R54`, `R53`, `R52`). Confirmed on physical files on disk. | Limited to text files on disk; session scrollback handled by host. |
| **CHK-02** | Textual Completeness & Flow | Sections 1 through 15 | Manual Line-by-Line Inspection | **VERIFIED** | All 15 sections are fully formed with complete sentences, unbroken table formatting, and clear transitions. Zero truncation markers or cut-off tables exist. Full identifier, metadata, scope, and status present. | Purely textual validation; does not evaluate runtime behavior. |
| **CHK-03** | Architecture Model Parity | Section 3 (§3.1, §3.2, §3.3) | Manual Cross-Reference Count | **VERIFIED** | Exact 1:1:1 mathematical parity: exactly 33 nodes declared in diagram (§3.1), 33 records in node register (§3.2, `N-01`..`N-33`), and 44 edges in edge register (§3.3, `E-01`..`E-44`). Zero dangling endpoints. | Validates static model topology; does not execute audio routing. |
| **CHK-04** | Operating Mode Privacy Governance | §3.4.2, §7.2, §10.1, §10.2 | Cross-Spec Alignment | **VERIFIED** | Local Mode (strictly offline default, zero socket egress, no silent fallback) and Cloud Opt-In Mode (sequential fallback, explicit consent, provider terms tracked as gate, 2.50 s timeout, local fallback option) strictly cross-verified against `SPEC.md` §1, §5.2, §6 and `DECISIONS.md` D-010, D-011. | Validates specification constraints; socket blocking requires M0 test. |
| **CHK-05** | Digital Route Isolation Protocol | §7.4 (Test 3) | Protocol & Math Audit | **NOT EMPIRICALLY TESTED** | Protocol specification passed textual audit (AES-17 1 kHz sine, $L_{\text{stim}} = -20.0\text{ dBFS}$, $L_{\text{cap}} \le -80.0\text{ dBFS}$, $R_{\text{iso}} \ge 60\text{ dB}$, preflight floor $\le -90.0\text{ dBFS}$). Reconciled under Gate G-04. | Physical test execution deferred to M0-5 on live Windows hardware. |
| **CHK-06** | Acoustic Leakage Protocol & Math | §7.4 (Test 3) | Mathematical Formulation Audit | **NOT EMPIRICALLY TESTED** | Mathematical formulation for background-corrected power and acoustic leakage ratio ($\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$) verified with near-zero floor $\epsilon = 10^{-5}$. Reconciled under Gate G-04. | Physical acoustic leakage screening on hardware deferred to M0-5. |
| **CHK-07** | Loopback Stability Protocol & Accounting | §7.4 (Test 2B) | Mathematical Accounting Audit | **NOT EMPIRICALLY TESTED** | Rigorous mathematical accounting for aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$) over QPC reference, audio frame vs sample definition, and discontinuity flags verified in text. | Physical 60-minute hardware test deferred to M0-4. |
| **CHK-08** | PTT Lifecycle & Cancellation Protocol | §3.4.3, §7.4 (Test 4) | Lifecycle Protocol Audit | **NOT EMPIRICALLY TESTED** | Phase 4A unit test harness fully designed in text. Physical Phase 4B Windows integration timing targets ($T_1 \le 30\text{ ms}$, $T_2 \le 60\text{ ms}$, $T_3 \le 10\text{ ms}$, $T_4 \le 50\text{ ms}$) specified. | Live Windows host integration testing deferred to M0-5. |
| **CHK-09** | Licensing Alignment with SPEC.md | §6.0, §7.1, §10.2 | Cross-Document Legal Audit | **PARTIALLY VERIFIED** | Cross-verified against `SPEC.md` §5 and `DECISIONS.md` D-003/D-005: `OHF-Voice/piper1-gpl` identified as GPL-3.0 and unapproved by default. Local Japanese TTS identified as mandatory MVP hard gate. PyAudioWPatch labeled as candidate. Evidence confined strictly to licensing. | Binary wheel availability (GAP-13) and model weight provenance unverified. |
| **CHK-10** | Hardware Safety & Power Grounding | §1.1, §1.2, §7.3, §8.1 | Cross-Document Risk Audit | **PARTIALLY VERIFIED** | Grounded strictly in `SPEC.md` §8 as an observed hardware/battery risk requiring plugged-in AC power (`ACLineStatus == 1`) and CPU load-abort watchdog ($\ge 95\%$ for $\ge 15\text{ s}$). Proposed ADR D-028 not cited as governing authority. Evidence confined strictly to power/host safety. | Live Win32 power API execution and CPU load watchdog deferred to M0-6. |
| **CHK-11** | Defect Audit Honesty | §11.0 | Historical Defect Audit | **VERIFIED** | All 33 historical defects audited individually with grounded statuses (28 Corrected in Document, 5 Protocol Specified, 0 Empirically Tested, 0 Owner-Approved, 0 Unverified). Discrepancy eliminated; zero double-counting. | Purely historical document audit; does not validate runtime code. |
| **CHK-12** | Bidirectional Traceability Integrity | §12.2, §12.3, §15.2 | Cross-Matrix Parity Audit | **VERIFIED** | Forward matrix 1:1 alignment across all 15 unresolved items (U-01..U-15) and canonical technical gaps (GAP-01..GAP-15), and reverse matrix mapping to release gates G-01..G-04 verified. Acoustic feedback reconciled to G-04. | Validates specification traceability; does not close technical gaps. |
| **CHK-13** | Planning-Only Boundary & Filesystem Accounting | §1.1, §1.2, §13.0, §15.5 | Filesystem Inode Audit | **VERIFIED** | Categorized filesystem audit confirms 2 new documentation files created (`R60`), 0 predecessor files modified, 0 governing files modified, 0 packages installed, 0 model weights downloaded, 0 audio hardware accessed. Missing `LICENSE` and absent `.git` repository honestly reported. | Verified against local filesystem state only. |
| **CHK-14** | Release Gate & Milestone Discipline | §1.1, §7.1–§7.4, §9.0, §15.1, §15.5 | Governance Discipline Audit | **VERIFIED** | All four release gates (G-01 through G-04) remain strictly EMPIRICAL GATES OPEN. Milestone M0 remains strictly UNAUTHORIZED pending explicit project owner approval. Proposed amendments (C-01..C-04) and decisions (D-028..D-033) clearly marked NOT APPLIED. | Requires explicit owner sign-off to authorize discovery execution. |

---

## 15. Milestone Blockers, Canonical Gaps, Limitations, Pending Decisions & Final Verdict

### 15.1 Milestone Dependency Chain & Blocking Gates

```
[M0: Discovery & Gate Clearance]  <-- CURRENT EXECUTION BOUNDARY (STRICTLY UNAUTHORIZED)
  │   Blocks on: Gates G-01, G-02, G-03, G-04 (ALL EMPIRICAL GATES OPEN)
  ▼
[M1: Audio Infrastructure & WASAPI Loopback]
  │   Blocks on: Clearance of Gate G-04 (WASAPI Loopback Stability & Endpoint Enumeration)
  ▼
[M2: Inbound Speech Recognition & VAD Pipeline]
  │   Blocks on: M1 delivery + Silero VAD / faster-whisper int8 CPU latency validation
  ▼
[M3: Translation Subsystem (Local MT & Opt-In Cloud)]
  │   Blocks on: M2 delivery + Clearance of Gate G-02 (Direct JA↔EN MT Quality)
  ▼
[M4: Outbound Speech Injection & Global PTT Control]
  │   Blocks on: M3 delivery + Clearance of Gate G-01 (TTS Licensing) & Gate G-04 (PTT Safety)
  ▼
[M5: Presentation UI & Transparent Caption Overlay]
  │   Blocks on: M4 delivery + Tkinter 30 FPS overlay event loop responsiveness
  ▼
[M6: Performance Hardening & End-to-End Latency Verification]
  │   Blocks on: M5 delivery + Clearance of Gate G-03 (End-to-End Latency on AC Power)
  ▼
[M7: Final Packaging, Installer & Operational Documentation]
  │   Blocks on: M6 clearance + PyInstaller Windows x64 build + LICENSE commitment
```

### 15.2 Canonical Open Technical Gaps (GAP-01 through GAP-15)

1. **GAP-01 (Critical - P0): Permissive Japanese TTS Engine & Voice Asset License Clearance:** No standalone, permissively licensed Japanese TTS engine with verified permissive voice weights has been cleared. The maintained `OHF-Voice/piper1-gpl` package is GPL-3.0-or-later and strictly unapproved by default under the permissive-first policy (`SPEC.md` §5). Acoustic weights, phonemizer checkpoints, and voice data require independent license verification. Mandatory MVP hard release gate (Gate G-01).
2. **GAP-02 (Critical - P0): Direct JA↔EN Machine Translation Quality & Latency Clearance:** Argos Translate direct JA↔EN translation accuracy and latency on technical meeting dialogue have not been empirically validated. Pivot translation via intermediate languages is prohibited (`DECISIONS.md` D-006). MarianMT local fallback models (`Helsinki-NLP/opus-mt-ja-en` / `en-jap`) must be benchmarked on the 10-sentence dialogue suite if Argos fails accuracy thresholds (Gate G-02).
3. **GAP-03 (Critical - P0): Laptop AC Power Mandate & CPU Watchdog Thresholds:** Target laptop hardware exhibits sudden system power shutdowns when operated under heavy load on battery power (`SPEC.md` §8). Operation requires verified plugged-in AC power (`ACLineStatus == 1`) and a background CPU watchdog alerting and throttling the pipeline if host CPU utilization reaches $\ge 95\%$ sustained for $\ge 15\text{ s}$ (Gate G-03). Sole governing authority: `SPEC.md` §8; proposed ADR D-028 remains unapplied.
4. **GAP-04 (Critical - P0): WASAPI Loopback Capture Stability & Device Enumeration:** Capturing meeting audio from Chrome/Edge requires stable shared-mode loopback capture on `Dev_Playback` via PyAudioWPatch. The stream must sustain 60 minutes of continuous streaming without frame loss, buffer drift, or clock desynchronization, enforcing $E_{\text{delivery}} \le 50.0\text{ PPM}$ relative to QPC timestamps and zero buffer discontinuity flags (Gate G-04).
5. **GAP-05 (Critical - P0): VB-CABLE Outbound Injection & Push-to-Talk Lifecycle Safety:** Outbound speech must inject cleanly into VB-CABLE Input. Global push-to-talk must enforce dual-signal supervision (Win32 low-level keyboard hook paired with a 50 ms polling heartbeat), KeyDown epoch increment (`EpochID = N + 1`), and KeyUp queue purging (`qsize() == 0`), mic capture halt within $\le 10\text{ ms}$, and render reset within $\le 50\text{ ms}$ (Gate G-04).
6. **GAP-06 (High - P1): Acoustic Feedback Prevention & Mandatory Headphone Policy:** Open speakers cause meeting audio to leak into the user microphone, producing acoustic feedback loops and false STT triggers. Physical headphones (`Dev_Headphones`) are mandatory (`DECISIONS.md` D-016). Loopback capture must never be unconditionally suppressed during outbound cross-talk (`SPEC.md` §4.3). Acoustic leakage screening must verify $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ over ambient noise (Gate G-04).
7. **GAP-07 (High - P1): Dual-Mode Privacy Governance & Opt-In Cloud Protocol:** Local Mode (default) must be strictly offline with zero socket egress and no silent fallback. Cloud Opt-In Mode requires explicit informed user consent, plain text payloads only (never audio), a 2.50 s client HTTP timeout, monotonic correlation IDs ($\text{CorrID} = \langle \text{SessionID}, \text{EpochID}, \text{SegmentSeq} \rangle$), sequential local fallback if enabled, and immediate cancellation upon epoch invalidation (Gate G-02).
8. **GAP-08 (High - P1): Speech Recognition Latency & Model Quantization Clearance:** `faster-whisper` `small` model with `int8` quantization on CPU via CTranslate2 must achieve transcription latency $\le 800\text{ ms}$ for 3.0-second speech segments on Intel Core i7-8750H on AC power (Gate G-03).
9. **GAP-09 (High - P1): Voice Activity Detection Latency & Chunk Ingestion:** Silero VAD (ONNX Runtime) must process 30 ms (512-sample) audio chunks in $\le 5.0\text{ ms}$ on CPU with speech onset threshold $0.50$, trailing silence window $\ge 400\text{ ms}$, and zero memory leaks over extended streaming (Gate G-03).
10. **GAP-10 (High - P1): End-to-End Pipeline Latency Budget Clearance:** Inbound translation budget ($1,800\text{ ms}$ target, $2,400\text{ ms}$ max) and outbound speech budget ($2,100\text{ ms}$ target, $2,900\text{ ms}$ max) must be empirically cleared on target hardware on AC power (Gate G-03).
11. **GAP-11 (Medium - P2): Tkinter GUI Responsiveness & Focus Preservation:** Tkinter caption overlay must render at $\ge 30\text{ FPS}$ without stealing user focus from Chrome/Edge during background inference (Gate G-04).
12. **GAP-12 (Medium - P2): Secure Gemini API Key Storage via Windows Credential Manager:** When Cloud Opt-In Mode is enabled, API key must be stored securely using `keyring` (Windows DPAPI backend) and never written to plaintext configuration files or logs (`DECISIONS.md` D-027) (Gate G-03).
13. **GAP-13 (Medium - P2): Python Runtime & Dependency Compatibility (3.11/3.12 vs 3.13):** `SPEC.md` §1 references Python 3.13, but CTranslate2, PyAudioWPatch, and onnxruntime pre-compiled wheels for Windows x64 must be verified. If 3.13 wheels are unavailable, runtime must pin to 3.11 or 3.12 (Gate G-01).
14. **GAP-14 (Medium - P2): Digital Route Isolation Verification (AES-17 Sine Protocol):** Outbound audio injected into `Dev_CableIn` must achieve $\ge 60\text{ dB}$ digital isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) against the loopback capture tap on `Dev_Playback` under AES-17 1,000 Hz sine stimulus testing (Gate G-04).
15. **GAP-15 (Low - P3): Repository License File Absence on Disk:** `CLAUDE.md` specifies MIT target for project-owned code, but no `LICENSE` file exists on disk. Must be committed prior to M1 upon owner authorization (Gate G-01).

### 15.3 Known Architectural Limitations & Operational Boundaries
1. **Virtual Audio Driver DMA Latency:** User-space software cannot recall or purge audio frames already committed to the VB-CABLE virtual driver DMA circular buffer ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$). Enforcing `qsize() == 0` purges software queues but cannot silence audio already transferred to the driver.
2. **Non-Preemptible Native C++ Inference:** In-flight tensor execution in CTranslate2 or ONNX Runtime cannot be safely interrupted mid-inference without memory corruption. Downstream epoch invalidation discards output instead.
3. **Secure Desktop Hook Suspension:** Win32 `WH_KEYBOARD_LL` low-level keyboard hooks stop receiving Windows messages during UAC prompts, Winlogon, and lock screens. Polling heartbeats and a 15-second watchdog provide fail-safe release upon desktop return.
4. **Physical Acoustic Isolation Dependency:** Software digital isolation cannot prevent acoustic cross-talk if open laptop speakers are used. Physical headphones (`Dev_Headphones`) are mandatory.
5. **No Direct Hardware Clock Access:** User-space audio clients cannot query physical DAC crystal oscillators directly without COM `IAudioClock` interfaces. Aggregate frame delivery is monitored via QPC timestamps.
6. **Microphone dBFS vs Sound Pressure Level:** Uncalibrated microphone dBFS measures digital ADC quantization, not calibrated physical sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$).
7. **Smoke Test Heuristic Boundary:** The 10-sentence dialogue benchmark suite is an initial smoke test for model pre-filtering; full translation validation requires a 100+ dialogue corpus.
8. **HTTP Socket Cancellation Limit:** Closing a client HTTP socket cancels local response processing but does not guarantee that the remote cloud provider ceased processing a request already received.
9. **Single Inbound Playback Endpoint:** Loopback capture taps the default Windows playback device. Audio routed to alternative non-default physical endpoints will bypass the capture client.
10. **Host AC Power Dependency:** Benchmarking and live pipeline execution cannot be performed under battery operation due to target laptop hardware shutdown risks.

### 15.4 Recomputed Pending Governance Items Register (Exactly 10 Unique IDs)

A forensic audit of pending governance items confirms that exactly **10 unique governance proposal IDs** are documented across Sections 10.1 and 10.2:
- Exactly 4 Proposed SPEC.md Amendments: `C-01`, `C-02`, `C-03`, `C-04`.
- Exactly 6 Proposed Architecture Decision Records: `D-028`, `D-029`, `D-030`, `D-031`, `D-032`, `D-033`.
- Recomputed Sum: $4 + 6 = 10$ unique governance IDs.

Milestone M0 discovery authorization is an operational execution milestone boundary, not a numbered specification amendment or ADR proposal ID. No eleventh governance item is invented; the total is precisely 10 unique proposal IDs:

| Unique Item ID | Item Classification | Specific Proposal Title | Target Governing File | Current Governance Status |
|---|---|---|---|---|
| **C-01** | Proposed SPEC Amendment | Explicit Host Power Preflight & CPU Load-Abort Guardrail | `SPEC.md` §1 | **PROPOSED — NOT APPLIED** |
| **C-02** | Proposed SPEC Amendment | Quantitative Direct Translation Evaluation Protocol | `SPEC.md` §5.2 | **PROPOSED — NOT APPLIED** |
| **C-03** | Proposed SPEC Amendment | Acoustic Feedback & Virtual Routing Disentanglement | `SPEC.md` §4.3 | **PROPOSED — NOT APPLIED** |
| **C-04** | Proposed SPEC Amendment | Strict Local-First Privacy & Opt-In Cloud Governance Protocol | `SPEC.md` §1, §5.3 | **PROPOSED — NOT APPLIED** |
| **D-028** | Proposed ADR Record | Preflight AC Power Check and CPU Load-Abort Watchdog | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |
| **D-029** | Proposed ADR Record | Comparative Argos Translate vs MarianMT Evaluation Protocol | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |
| **D-030** | Proposed ADR Record | Acoustic Feedback Policy Mandating Physical Headphones | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |
| **D-031** | Proposed ADR Record | Dual-Signal PTT Supervision & Downstream Cancellation Architecture | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |
| **D-032** | Proposed ADR Record | Multi-Tier Licensing & Independent Model Asset Clearance Policy | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |
| **D-033** | Proposed ADR Record | Strict Local-First Privacy & Explicit Opt-In Cloud Governance Protocol | `DECISIONS.md` | **PROPOSED — NOT APPLIED** |

*Separate Operational Execution Boundary:*
- **Milestone M0 Discovery Authorization:** **STRICTLY UNAUTHORIZED — PENDING EXPLICIT OWNER SIGN-OFF**. Authorizes executing discovery tasks M0-1 through M0-9 in an isolated virtual environment. (Maintained strictly separate from the 10 governance proposal IDs above.)

---

### 15.5 Final Architecture Verdict & Governance Declaration

```
====================================================================================================
                        KOEBRIDGE FOR ZOOM — ARCHITECTURAL REVIEW VERDICT
====================================================================================================
Document Identifier:       KB-ARCH-VERIF-PLAN-R60
Document Revision:         Revision 60 (Forensic Repair, Canonical Baseline & Release-Gate Reconstruction)
Target Platform:           Windows 10/11 x64 (Build 19041+)
Target Hardware Baseline:  Intel Core i7-8750H, 32 GB RAM, Plugged-In AC Power (ACLineStatus == 1)
Governing Specifications:  SPEC.md (Authoritative), CLAUDE.md, DECISIONS.md (D-001..D-027)

CURRENT RELEASE GATE STATUSES:
  [EMPIRICAL GATE OPEN] Gate G-01: Japanese TTS Engine & Voice Licensing Clearance
  [EMPIRICAL GATE OPEN] Gate G-02: Direct JA↔EN Machine Translation Quality & Latency Clearance
  [EMPIRICAL GATE OPEN] Gate G-03: End-to-End Pipeline Latency & Host Hardware Thermal/Power Guardrails
  [EMPIRICAL GATE OPEN] Gate G-04: Audio Endpoint Topology, Loopback Stability & PTT Safety Verification

GOVERNANCE & EXECUTION BOUNDARY:
  Milestone M0 (Discovery): STRICTLY UNAUTHORIZED — AWAITING EXPLICIT PROJECT OWNER APPROVAL
  Pending Governance Items: EXACTLY 10 UNIQUE PROPOSAL IDs (C-01..C-04 and D-028..D-033)
                            ALL MARKED PROPOSED — NOT APPLIED TO SPEC.MD / DECISIONS.MD
  Filesystem Modifications: ZERO application code, prototypes, or test scripts written to disk
  Network Egress / Pip:     ZERO packages installed, ZERO model weights downloaded
  Hardware Probing:         ZERO audio devices accessed, ZERO benchmarks run

FINAL VERDICT:
  NOT APPROVED — PLANNING SPECIFICATION RECONCILED; ALL EMPIRICAL RELEASE GATES OPEN (G-01..G-04)
  The Revision 60 Architecture & Verification Plan is a complete, publication-grade specification,
  canonically reconciled across 33 nodes, 44 edges, 8 closed subgraphs, 33 historical defects,
  14 integrity checks, and 15 canonical gaps. Implementation remains NOT APPROVED because all four
  empirical release gates remain open and Milestone M0 remains strictly unauthorized.
====================================================================================================
```
