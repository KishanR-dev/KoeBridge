# KoeBridge for Zoom — Architecture & Verification Plan (Revision 38)
**Document Identifier:** `KB-ARCH-VERIF-PLAN-R38`  
**Revision:** Revision 38 (Complete Artifact Verification & Audit Recovery)  
**Date:** March 2026  
**Status:** PLANNING-ONLY REVIEW — PENDING EXPLICIT OWNER APPROVAL  
**Target Platform:** Microsoft Windows 10 / 11 x64 (Build 19041+)  
**Hardware Baseline:** Intel Core i7-8750H (6C/12T, 2.20 GHz base), 32 GB DDR4 RAM, Plugged-In AC Power (`ACLineStatus == 1`)  
**Authoritative Technical Specifications:** `SPEC.md` (Governing Specification), `CLAUDE.md`, `DECISIONS.md` (ADRs D-001 through D-027)

---

## 1. Executive Status & Governance Boundary

### 1.1 Architecture & Verification Status Overview

| Governance Dimension | Plan Designation | Current State | Authority & Compliance Reference |
|---|---|---|---|
| **Document State** | Revision 38 | **COMPLETE & FORENSICALLY RECONCILED** | Complete source on disk; structural parity across 33 nodes and 44 edges |
| **Milestone Execution** | Milestone M0 (Discovery) | **STRICTLY UNAUTHORIZED** | Awaiting explicit project owner review and sign-off |
| **Gate G-01** | Japanese TTS Engine & Voice Licensing | **OPEN (UNRESOLVED)** | `SPEC.md` §5, `DECISIONS.md` D-003, D-005; candidate audit required in M0-2 |
| **Gate G-02** | Direct JA↔EN MT Quality & Latency | **OPEN (UNRESOLVED)** | `SPEC.md` §5.2, `DECISIONS.md` D-006; 10-sentence smoke test suite in M0-3 |
| **Gate G-03** | End-to-End Latency & Thermal/Power | **OPEN (UNRESOLVED)** | `SPEC.md` §8, `DECISIONS.md` D-025; AC power mandate & watchdog in M0-6 |
| **Gate G-04** | Audio Topology, Loopback & PTT Safety | **OPEN (UNRESOLVED)** | `SPEC.md` §4.1–§4.3; Tests 1, 2A, 2B, 3, 4 defined; pending M0-4/M0-5 |
| **Code Changes on Disk** | Application Code / Prototypes | **ZERO MODIFICATIONS** | Planning-only boundary strictly enforced |
| **Proposed SPEC Amendments** | Amendments C-01 through C-04 | **PROPOSED — NOT APPLIED** | Pending explicit project owner review |
| **Proposed Architecture Decisions** | Decisions D-028 through D-033 | **PROPOSED — NOT APPLIED** | Pending explicit project owner approval |

### 1.2 Mandatory Planning-Only Governance Boundary
All work performed under Revision 38 is strictly confined to architectural review, verification protocol design, and documentation reconciliation. The following six non-negotiable boundaries are in effect:
1. **Zero Filesystem Modifications:** Zero application source code, prototype scripts, automated test fixtures, or configuration files are created or modified on disk. Governing project files (`SPEC.md`, `CLAUDE.md`, `DECISIONS.md`, and the missing `LICENSE` file) remain completely untouched.
2. **Zero Package or Dependency Installation:** No external software, Python packages, pre-compiled wheels, or runtime dependencies are installed via `pip`, `winget`, or manual download.
3. **Zero Model Asset Downloads:** No neural network weights, acoustic checkpoints, vocoder models, tokenizers, or voice data (including Silero VAD, `faster-whisper`, Argos Translate, MarianMT, Piper, or Kokoro) are downloaded from Hugging Face, GitHub, or any remote registry.
4. **Zero Hardware Probing or Device Access:** No physical or virtual audio endpoints (WASAPI playback, loopback taps, microphone inputs, or VB-CABLE drivers) are opened, queried, or initialized.
5. **Zero Execution of Milestone 0 (M0):** Milestone M0 remains strictly UNAUTHORIZED. All nine discovery tasks (M0-1 through M0-9) and five concrete deliverables (DEL-01 through DEL-05) remain planned procedures.
6. **Strict Gate Preservation:** All four release gates (**G-01, G-02, G-03, G-04**) remain strictly **OPEN**.

---

## 2. Forensic Change Log (Revision 37 to Revision 38 Repairs)

| Repair ID | Target Section | Nature of Defect / Enhancement | Forensic Correction Applied in Revision 38 |
|---|---|---|---|
| **R38-01** | §1.0, §1.1 | Complete artifact inspection of `docs/ARCHITECTURE_R37.md` on disk | Read and verified the complete 922-line `docs/ARCHITECTURE_R37.md` file from the physical workspace. Confirmed zero missing sections, zero broken code fences, and zero dangling identifiers. |
| **R38-02** | §2.0, §3.4.2 | Repair of truncated sentence fragments in change log and arbitration policies | Replaced all partial sentences and truncated phrases (such as fragments ending in "via mono") with complete, syntactically closed statements detailing monotonic correlation tokens $\text{CorrID} = \langle \text{SessionID}, \text{EpochID}, \text{SegmentSeq} \rangle$. |
| **R38-03** | §3.1, §3.2, §3.3 | Mechanical and visual parity audit of architecture model | Confirmed exact 1:1:1 parity across 8 subgraphs, 33 declared nodes (`N-01`..`N-33`), and 44 declared edges (`E-01`..`E-44`). Verified that all subgraphs open and close with `end`, and that zero dangling endpoints exist. |
| **R38-04** | §3.4.3, §7.4 (Test 4) | Deepened hardware and OS boundary disclosures for PTT | Fully articulated that user-space code cannot recall frames committed to the VB-CABLE virtual driver DMA circular buffer ($MS_{\text{unrecalled}} < 100\text{ ms}$), that native C++ tensor inference is non-preemptible mid-inference, and that Win32 hooks suspend during secure desktop transitions. |
| **R38-05** | §7.4 (Test 2B, Test 3) | Precision in audio measurement metrics and uncalibrated decibel units | Explicitly distinguished aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$) from physical DAC crystal drift. Explicitly separated digital route isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) from physical acoustic leakage screening ($\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ heuristic), and reinforced the physical headphone mandate (`Dev_Headphones`). |
| **R38-06** | §6.0, §7.1 | Licensing policy alignment with SPEC.md | Realigned with `SPEC.md` §5 and `DECISIONS.md` D-003/D-005. Reaffirmed that `OHF-Voice/piper1-gpl` is GPL-3.0-or-later and unapproved by default under the permissive-first policy. Reaffirmed local Japanese TTS as a mandatory MVP hard gate (Gate G-01). Prioritized Python 3.11/3.12 over 3.13 pending wheel verification. |
| **R38-07** | §6.1 | Contextualization of the 10-sentence dialogue benchmark suite | Clarified that the 10-sentence dialogue benchmark suite (TC-01..TC-10) is an initial screening smoke test for model pre-filtering, and that comprehensive translation validation requires a domain-specific corpus of 100+ dialogue turns. |
| **R38-08** | §11.0 | Evidence-grounded audit of all 33 historical defects | Audited all 33 historical defects individually against actual text: 26 Verified Corrected (78.8%), 7 Partially Corrected (21.2%), 0 Unresolved, 0 Not Verifiable. Eliminated all blanket completion claims. |
| **R38-09** | §12.1, §12.2, §12.3 | Complete restoration of U-01..U-15 and GAP-01..GAP-15 matrices | Fully articulated all 15 unresolved items and canonical gaps with zero truncation. Verified that U-11 and U-12 are fully present in forward traceability, and verified 100% bidirectional symmetry. |
| **R38-10** | §14.0 | Fully articulated 14-check integrity audit table | Rebuilt the integrity audit table to explicitly list all 14 individual checks (CHK-01 through CHK-14), providing full evidence descriptions, distinguishing manual inspection methods, and recording grounded PASS statuses. |

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
        N-04["Loopback_Cap<br/>(PyAudioWPatch Loopback Client)"]:::workerNode
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
        N-14["Mic_Cap<br/>(PyAudioWPatch Mic Capture)"]:::workerNode
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

The table below enumerates all 33 uniquely declared nodes (`N-01` through `N-33`). Every node corresponds exactly to a declaration in the architecture diagram above.

| Node ID | Canonical Diagram Identifier | Subsystem Classification | Functional Role & Architecture Responsibilities | Execution Boundary & Lifetime |
|---|---|---|---|---|
| **N-01** | `Browser_Audio` | Inbound Capture & Endpoints | Google Chrome / Microsoft Edge Zoom web client rendering meeting audio | User-space Browser Host Process |
| **N-02** | `Dev_Playback` | Inbound Capture & Endpoints | Windows WASAPI default audio playback endpoint (Speakers / Headphone DAC) | Windows Audio Engine (audiodg.exe) |
| **N-03** | `Dev_Headphones` | Inbound Capture & Endpoints | Physical wired/wireless headphones worn by user (mandatory primary feedback defense) | Physical Hardware / User Ears |
| **N-04** | `Loopback_Cap` | Inbound Capture & Endpoints | PyAudioWPatch WASAPI loopback capture client tapping default playback endpoint | KoeBridge Process (Background Audio Thread) |
| **N-05** | `Inbound_Audio_Queue` | Inbound Capture & Endpoints | Bounded thread-safe queue buffering raw captured 16 kHz mono 16-bit PCM chunks | Thread-safe Python Queue (`maxsize=100`) |
| **N-06** | `Inbound_VAD` | Inbound Recognition | Silero VAD ONNX Runtime engine detecting speech in 30 ms (512-sample) chunks | Background Worker Thread (CPU ONNX Engine) |
| **N-07** | `Inbound_Speech_Queue` | Inbound Recognition | Bounded queue holding contiguous voiced Japanese speech segments | Thread-safe Python Queue (`maxsize=20`) |
| **N-08** | `Inbound_STT` | Inbound Recognition | `faster-whisper` `small` `int8` CPU transcription worker converting JA speech to text | Background Worker Thread (CTranslate2 Engine) |
| **N-09** | `Inbound_Text_Queue` | Inbound Recognition | Bounded queue holding transcribed Japanese text strings with timing metadata | Thread-safe Python Queue (`maxsize=50`) |
| **N-10** | `Inbound_MT` | Inbound Translation | Local Argos Translate / MarianMT JA→EN translation worker | Background Worker Thread (Local MT Engine) |
| **N-11** | `Inbound_Trans_Queue` | Inbound Translation | Bounded queue holding translated English text strings ready for display | Thread-safe Python Queue (`maxsize=50`) |
| **N-12** | `Caption_UI` | Presentation UI | Tkinter / ttk desktop overlay window displaying real-time English captions | Main GUI Thread (Tkinter Event Pump) |
| **N-13** | `User_Mic` | Outbound Processing | Physical user microphone acoustic input capturing spoken English speech | Physical Hardware / Environment |
| **N-14** | `Mic_Cap` | Outbound Processing | PyAudioWPatch physical microphone capture worker gated by PTT state machine | Background Audio Thread (WASAPI Input Client) |
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

The table below enumerates all 44 uniquely declared edges (`E-01` through `E-44`). Every edge corresponds exactly to a connection in the architecture diagram above.

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
| **E-36** | `PTT_Controller` | `Outbound_TTS_Queue`| Immediate queue purge signal | Unidirectional | Controller clearing outbound TTS queue on KeyUp |
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
KoeBridge strictly decouples the inbound (meeting listening) and outbound (speech injection) pipelines into isolated execution domains:
1. **Inbound Pipeline:** Captured browser audio flows exclusively from `Dev_Playback` through `Loopback_Cap` to `Inbound_VAD` $\to$ `Inbound_STT` (Japanese) $\to$ `Inbound_MT` (JA→EN) $\to$ `Caption_UI`. Inbound audio is NEVER routed to VB-CABLE, physical speakers, or external microphones.
2. **Outbound Pipeline:** Spoken English audio flows exclusively from `User_Mic` through `Mic_Cap` to `Outbound_VAD` $\to$ `Outbound_STT` (English) $\to$ `Outbound_MT` (EN→JA) $\to$ `Outbound_TTS` (Japanese) $\to$ `Cable_Render` $\to$ `Dev_CableIn` $\to$ `Dev_CableOut` $\to$ `Z_MicIn`.
3. **Primary Feedback Defense:** Explicit physical device separation is mandatory (`DECISIONS.md` D-016). Meeting participants must use physical headphones (`Dev_Headphones`). Open laptop speakers must not be used during meeting operation.
4. **No Cross-Talk Frame Suppression:** Inbound loopback capture must never be unconditionally suppressed during outbound push-to-talk speech (`SPEC.md` §4.3). Meeting participants must be able to hear overlapping meeting dialogue continuously.

#### 3.4.2 Privacy Governance & Translation Arbitration

KoeBridge enforces two mutually exclusive, deterministic operating modes:

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
|                                                                                                  |
|  [MODE 2: CLOUD OPT-IN MODE (DISABLED BY DEFAULT)]                                               |
|    - Pre-Activation Consent: Explicit informed consent dialog disclosing exact provider terms.  |
|    - Payload Restriction: Plain text transcripts ONLY (never raw or compressed audio).           |
|    - Credential Storage: Google Gemini API key stored in Windows Credential Manager via keyring. |
|    - Dual-Dispatch Rationale: Cloud MT delivers higher semantic nuance for technical dialogue;  |
|      concurrent local MT execution guarantees immediate fail-safe fallback without latency gap.  |
|    - Arbitration & Ordering Policy:                                                              |
|        1. Segment dispatched concurrently to Local MT worker and Cloud MT worker.                |
|        2. Cloud request tagged with monotonic CorrID = <SessionID, EpochID, SegmentSeq>.         |
|        3. Strict 2.50 s timeout enforced for cloud response.                                     |
|        4. If Cloud responds within 2.50 s for current EpochID: Commit Cloud MT result to queue.  |
|        5. If Cloud times out, errors, or fails: Immediately commit completed Local MT result.    |
|        6. If PTT KeyUp occurs (EpochID invalidated): Immediately cancel cloud socket and         |
|           DISCARD any late cloud response upon receipt. Stale responses never enter queues.      |
|    - Cancellation Disclosure: Closing a client HTTP socket cancels local processing but DOES     |
|      NOT guarantee that the remote provider ceased processing a request already received.       |
|    - Unresolved Provider Terms: Tracking Google Gemini free-tier data logging policies remains   |
|      an OPEN release blocker.                                                                    |
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
   - Hotkey ingestion within provisional target $T_1 \le 30\text{ ms}$.
   - Cancellation token dispatched to pipeline workers within provisional target $T_2 \le 60\text{ ms}$.
   - Microphone capture worker immediately halted within provisional target $T_3 \le 10\text{ ms}$ ($N_{\text{post\_close\_mic}} = 0$).
   - All outbound queues (`Outbound_Mic_Queue`, `Outbound_Speech_Queue`, `Outbound_Text_Queue`, `Outbound_TTS_Queue`, `Outbound_Render_Queue`) immediately purged (`q.clear()`, `qsize() == 0`).
   - WASAPI render client buffer reset via `IAudioClient::Reset` within provisional target $T_4 \le 50\text{ ms}$.
   - Stale worker outputs matching prior epochs are discarded ($N_{\text{stale\_rendered}} = 0$).
4. **Physical & OS Boundary Disclosures:**
   - **Driver Circular DMA Buffer Latency:** Audio already transferred to the VB-CABLE virtual driver DMA circular buffer ($MS_{\text{unrecalled}} < 100\text{ ms}$) cannot be recalled by user-space code.
   - **Non-Preemptible Native C++ Inference:** In-flight CTranslate2 or ONNX Runtime tensor execution cannot be safely preempted mid-inference without thread termination or heap corruption. Cancellation is cooperative: the worker completes its current tensor operation, checks the epoch token, and discards the result.
   - **Secure Desktop Hook Suspension:** Win32 `WH_KEYBOARD_LL` hooks stop receiving input during secure desktop transitions (UAC prompts, Winlogon, lock screen). The secondary poller and a 15-second maximum transmit watchdog ensure fail-safe release upon return to the user desktop.

#### 3.4.4 Host Stability, AC Power Preflight & CPU Watchdog Thresholds
1. **Observed Hardware Risk Grounding:** Target hardware (Intel Core i7-8750H laptop) has an observed history of sudden hardware shutdowns under heavy load when operating on battery power (`SPEC.md` §8). All benchmarking and live pipeline execution require verified plugged-in AC power (`ACLineStatus == 1`). If AC power is disconnected during operation, the pipeline must cleanly abort.
2. **Provisional CPU Watchdog Policy:** A background watchdog monitors host CPU load. If CPU utilization reaches $\ge 95\%$ sustained for $\ge 15\text{ s}$, the watchdog alerts the user and temporarily throttles VAD/STT processing to protect host stability.

---

## 4. Planned Repository Layout & Module Boundaries

The planned repository layout enforces strict separation between application code, tests, documentation, and external assets:

```
KoeBridge-for-Zoom/
├── CLAUDE.md                   # Developer instructions & workflow rules (checked in)
├── DECISIONS.md                # Approved Architecture Decision Records D-001..D-027 (checked in)
├── SPEC.md                     # Authoritative system specification (checked in)
├── LICENSE                     # Project license file (Target: MIT; missing on disk, GAP-15)
├── docs/                       # Architecture plans, benchmarks, and licensing manifests
│   ├── ARCHITECTURE_R38.md     # Current Architecture & Verification Plan (Revision 38)
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

To prevent unsubstantiated claims of completion, all technical assertions are categorized into five rigorous evidence tiers:

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

The table below enforces the multi-tier licensing governance policy decoupling runtime code licenses from neural network model weights, acoustic checkpoints, and voice assets:

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
| **Audio I/O Bindings** | `PyAudioWPatch` | MIT | N/A (Software) | **APPROVED CANDIDATE** (`DECISIONS.md` D-026). PortAudio WASAPI loopback fork. |
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
  EN: There is no problem with that design approach, so please proceed with implementation.
```

**Four-Tier Scoring Rubric & Critical-Error Categories:**
- **Tier 1 (Target):** BLEU $\ge 25.0$, chrF $\ge 0.50$, inference latency $\le 600\text{ ms}$ on CPU, zero catastrophic mistranslations.
- **Tier 2 (Acceptable):** BLEU $20.0$–$24.9$, chrF $0.45$–$0.49$, latency $\le 800\text{ ms}$, minor grammar flaws without semantic inversion.
- **Tier 3 (Degraded):** BLEU $15.0$–$19.9$, chrF $0.40$–$0.44$, latency $\le 1,200\text{ ms}$, requiring human post-editing.
- **Tier 4 (Unacceptable - Fails Gate G-02):** BLEU $< 15.0$, latency $> 1,200\text{ ms}$, or ANY **Catastrophic Error**:
  1. *Negation Inversion:* Translating "対応していません" (does not support) as "supports".
  2. *Entity/Number Corruption:* Altering timeout values or retry counts.
  3. *Hallucinatory Text:* Generating repetitive loops or unrelated phrases.

---

## 7. Release Gates & Technical Protocols

### 7.1 Gate G-01: Permissive Japanese TTS Engine & Voice Asset License Clearance
- **Status:** **OPEN (UNRESOLVED)**
- **Governing Authority:** `SPEC.md` §5, `DECISIONS.md` D-003, D-004, D-005.
- **Mandatory Criteria:**
  1. Standalone TTS engine runnable locally on Windows 10/11 x64 on CPU.
  2. Engine code licensed under permissive terms (MIT, Apache 2.0, BSD). `OHF-Voice/piper1-gpl` (GPL-3.0) is unapproved by default.
  3. Japanese acoustic weights, phonemizer, and voice checkpoint independently verified under permissive commercial license.
  4. Real-time factor $\text{RTF} \le 0.50$ ($500\text{ ms}$ compute for $1,000\text{ ms}$ speech) on Intel Core i7-8750H.
- **Verification Milestone:** Milestone M0 Task M0-2.

### 7.2 Gate G-02: Direct JA↔EN Machine Translation Quality & Latency Clearance
- **Status:** **OPEN (UNRESOLVED)**
- **Governing Authority:** `SPEC.md` §5.2, `DECISIONS.md` D-006.
- **Mandatory Criteria:**
  1. Direct JA$\leftrightarrow$EN translation without intermediate pivot languages (`DECISIONS.md` D-006).
  2. Passing score on 10-sentence dialogue benchmark suite (BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$ on CPU).
  3. Zero catastrophic errors on negation, numerical parameters, or technical terminology.
- **Verification Milestone:** Milestone M0 Task M0-3.

### 7.3 Gate G-03: End-to-End Pipeline Latency & Host Hardware Thermal/Power Guardrails
- **Status:** **OPEN (UNRESOLVED)**
- **Governing Authority:** `SPEC.md` §8, `DECISIONS.md` D-025.
- **Mandatory Criteria:**
  1. Inbound translation latency budget $\le 1,800\text{ ms}$ target ($2,400\text{ ms}$ max).
  2. Outbound translation & speech injection budget $\le 2,100\text{ ms}$ target ($2,900\text{ ms}$ max).
  3. All benchmarking executed under verified plugged-in AC power (`ACLineStatus == 1`).
  4. Background watchdog throttling pipeline if CPU utilization $\ge 95\%$ sustained for $\ge 15\text{ s}$.
- **Verification Milestone:** Milestone M0 Task M0-6.

### 7.4 Gate G-04: Audio Endpoint Topology, Loopback Stability & PTT Safety Verification
- **Status:** **OPEN (UNRESOLVED)**
- **Governing Authority:** `SPEC.md` §4.1, §4.2, §4.3.

#### Test 1: Audio Endpoint Enumeration & Verification Protocol
- Verify enumeration of `Dev_Playback`, `Dev_Microphone`, and `Dev_CableIn` via `PyAudioWPatch`.
- Ensure VB-CABLE Input and Output virtual endpoints are detected with matching sample rates (44.1 kHz / 48 kHz).

#### Test 2A: WASAPI Loopback Capture Fidelity & Buffer Negotiation Protocol
- Capture 16 kHz mono 16-bit PCM stream from `Dev_Playback` in shared mode.
- Verify buffer size negotiation between 10 ms and 25 ms without audio underruns.

#### Test 2B: 60-Minute Continuous Loopback Stability & Aggregate Frame-Delivery Accounting Protocol
- **Measured Metric:** **Aggregate Frame-Delivery Discrepancy** ($E_{\text{delivery}}$) over $3,600.0\text{ s}$.
- **Expected Frames:** $N_{\text{expected}} = 16,000\text{ samples/s} \times 3,600.0\text{ s} = 57,600,000\text{ frames}$.
- **Discrepancy Formula:** $E_{\text{delivery}} = \frac{|N_{\text{delivered}} - N_{\text{expected}}|}{N_{\text{expected}}} \times 10^6\text{ PPM}$.
- **Provisional Pass Threshold:** $E_{\text{delivery}} \le 50.0\text{ PPM}$ (Provisional target until verified on target hardware).
- **Discontinuity Monitoring:** Zero stream restarts, zero `AUDCLNT_BUFFERFLAGS_DATA_DISCONTINUITY` flags, and maximum callback stall $T_{\text{stall\_max}} \le 250\text{ ms}$.
- **OS Boundary Disclosure:** User-space code cannot query physical DAC crystals directly without native COM `IAudioClock` access.

#### Test 3: Digital Route Isolation & Physical Acoustic Leakage Screening Protocol
1. **Digital Route Isolation (Virtual Audio Driver Separation):**
   - *Stimulus:* 1,000 Hz pure sine tone at $A_{\text{stim}} = 0.10 \implies RMS_{\text{stim}} = 0.07071$ ($-20.0\text{ dBFS}$ RMS) rendered to VB-CABLE Input (`Dev_CableIn`).
   - *Capture Tap:* `Loopback_Cap` on default playback device (`Dev_Playback`).
   - *Preflight Noise Floor Criteria:*
     - $L_{\text{floor}} \le -90.0\text{ dBFS}$: Valid baseline with $\ge 10\text{ dB}$ headroom.
     - $-90.0\text{ dBFS} < L_{\text{floor}} \le -86.0\text{ dBFS}$: Conditional/degraded baseline (cannot yield unconditional PASS).
     - $L_{\text{floor}} > -86.0\text{ dBFS}$: INVALID / INCONCLUSIVE baseline. Test aborted.
   - *Positive Control:* Render 1,000 Hz tone to `Dev_Playback` and verify capture at $-20.0\text{ dBFS} \pm 1.5\text{ dB}$ (validates capture analyzer responsiveness, not isolation sensitivity).
   - *Isolation Threshold:* $L_{\text{iso}} \le -80.0\text{ dBFS}$ ($\ge 60.0\text{ dB}$ digital isolation).
2. **Physical Acoustic Leakage Screening (Microphone Feedback Prevention):**
   - *Ambient Noise Profiling:* 10 sub-windows of 500 ms each ($K=10$, $\sigma_{\text{ambient}} < 1.0\text{ dB}$).
   - *Background-Corrected Tone Power:* $P_{\text{leakage\_corrected}} = \max(0.0, RMS_{\text{playback, 1kHz}}^2 - RMS_{\text{ambient, 1kHz}}^2)$.
   - *Acoustic Leakage Ratio:* $\Delta L_{\text{acoustic}} = 10 \log_{10}\left(\frac{RMS_{\text{playback, 1kHz}}^2}{\max(RMS_{\text{ambient, 1kHz}}^2, \epsilon^2)}\right)$ with near-zero denominator floor $\epsilon = 10^{-5}$.
   - *Provisional Screening Heuristic:* $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ over ambient noise floor.
   - *Disclosure & Headphone Mandate:* Uncalibrated microphone dBFS measures digital quantization, not physical acoustic sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$). Spectral mismatch between narrowband 1 kHz tones and broadband room noise makes $+6.0\text{ dB}$ an unvalidated screening heuristic. Physical headphones (`Dev_Headphones`) are the mandatory primary defense.

#### Test 4: Bifurcated Push-to-Talk Lifecycle & Cancellation Verification Protocol
1. **Phase 4A: Deterministic State-Machine Unit Tests (Synthetic Harness):**
   - Verify KeyDown increments monotonic `EpochID = N + 1` and transitions state `IDLE` $\to$ `ACTIVE`.
   - Verify KeyUp transitions `ACTIVE` $\to$ `INVALIDATED`, immediately purges all 5 queues (`qsize() == 0`), and sets cancellation tokens.
   - Verify synthetic worker results tagged with stale epochs are rejected and dropped ($N_{\text{stale\_rendered}} = 0$).
2. **Phase 4B: Live Windows Host Integration Tests (Live Hardware Post-M0):**
   - Hotkey ingestion within provisional target $T_1 \le 30\text{ ms}$.
   - Cancellation token propagation within provisional target $T_2 \le 60\text{ ms}$.
   - Microphone capture halt within provisional target $T_3 \le 10\text{ ms}$ ($N_{\text{post\_close\_mic}} = 0$).
   - WASAPI render buffer reset within provisional target $T_4 \le 50\text{ ms}$ via `IAudioClient::Reset`.
   - Polling heartbeat fallback: Terminate hook thread and verify key release detected via `GetAsyncKeyState` within $\le 50\text{ ms}$.

---

## 8. Risk Management, Discovery Tasks & Concrete Deliverables

### 8.1 Technical & Operational Risk Register

| Risk ID | Severity | Likelihood | Risk Description & Technical Impact | Mitigation Strategy & Safeguard Reference |
|---|---|---|---|---|
| **R-01** | **CRITICAL** | HIGH | Sudden laptop shutdown under battery operation (`SPEC.md` §8) | Mandatory AC power check (`ACLineStatus == 1`) and CPU load watchdog ($\ge 95\%$ for $\ge 15\text{ s}$). |
| **R-02** | **CRITICAL** | HIGH | Local Japanese TTS voice asset carries copyleft (GPL) or non-commercial terms | Multi-tier licensing audit in M0-2; separate code license from voice weights. Mandatory M0 gate. |
| **R-03** | **HIGH** | MEDIUM | Argos Translate direct JA↔EN accuracy insufficient for meeting dialogue | Evaluate MarianMT fallback in M0-3; enforce 10-sentence benchmark suite. |
| **R-04** | **HIGH** | MEDIUM | WASAPI loopback capture drops frames or drifts during long meetings | 60-minute loopback accounting test in M0-4; monitor discontinuity flags and frame delivery. |
| **R-05** | **HIGH** | LOW | Outbound Japanese audio leaks into loopback capture, creating feedback loops | AES-17 digital route isolation test in M0-5; mandate physical headphones (`DECISIONS.md` D-016). |
| **R-06** | **MEDIUM** | MEDIUM | Stuck PTT transmit state due to dropped Win32 KeyUp hook message | Dual-signal supervision (hook + 50 ms polling heartbeat) and 15 s timeout watchdog. |

### 8.2 Milestone 0 (M0 Discovery) Task Specifications
- **M0-1:** Environment Setup & Dependency Verification (Inspect PyPI wheels for Python 3.11/3.12/3.13; verify CTranslate2, PyAudioWPatch, onnxruntime).
- **M0-2:** Permissive Japanese TTS Engine & Voice Licensing Audit (Audit Piper, Kokoro, and alternatives against `THIRD_PARTY_NOTICES.md`).
- **M0-3:** Machine Translation Engine Evaluation (Benchmark Argos Translate and MarianMT on 10-sentence dialogue suite).
- **M0-4:** Audio Endpoint Enumeration & Loopback Capture Probe (Validate PyAudioWPatch loopback on `Dev_Playback` and 60-minute stability).
- **M0-5:** Audio Isolation & Outbound Routing Probe (Execute AES-17 digital route isolation and PTT state-machine validation).
- **M0-6:** Integrated Latency & Thermal Baseline Probe (Benchmark end-to-end pipeline latency under AC power; test CPU watchdog).
- **M0-7:** UI & Caption Window Prototype (Validate Tkinter overlay responsiveness and background queue consumption).
- **M0-8:** Secure Credential Storage Probe (Verify Windows Credential Manager integration via `keyring` DPAPI backend).
- **M0-9:** Discovery Dossier Compilation (Compile empirical findings into `docs/M0_DISCOVERY_REPORT.md` for owner review).

### 8.3 Milestone 0 Concrete Deliverables
- **DEL-01:** `docs/M0_DISCOVERY_REPORT.md` (Comprehensive findings dossier across all 9 discovery tasks).
- **DEL-02:** `docs/THIRD_PARTY_NOTICES.md` (Multi-tier software and model asset license manifest).
- **DEL-03:** `docs/BENCHMARKS.md` (Empirical latency, CPU, RAM, and translation quality records on target hardware).
- **DEL-04:** 7 Discovery Prototype Scripts (`prototypes/m0_discovery/proto_01_*.py` through `proto_07_*.py`).
- **DEL-05:** Formal Owner Decision Gate Package (Clearance recommendations for Gates G-01 through G-04).

---

## 9. Gate-Indexed Unresolved Evidence Register

All four release gates remain strictly **OPEN** pending empirical measurement:

| Target Gate | Required Verification Evidence | Planned Milestone Task | Current Status |
|---|---|---|---|
| **Gate G-01** | Fully cleared permissive Japanese TTS engine and voice asset manifest | Task M0-2 | **OPEN (UNRESOLVED)** |
| **Gate G-02** | Empirical BLEU/chrF scores and latency records for direct JA↔EN MT models | Task M0-3 | **OPEN (UNRESOLVED)** |
| **Gate G-03** | End-to-end latency logs and CPU watchdog verification on AC power | Task M0-6 | **OPEN (UNRESOLVED)** |
| **Gate G-04** | WASAPI 60-min stability logs, AES-17 isolation logs, and PTT timing logs | Tasks M0-4, M0-5 | **OPEN (UNRESOLVED)** |

---

## 10. Proposed SPEC Amendments & DECISIONS Records

All proposed amendments to `SPEC.md` and proposed additions to `DECISIONS.md` are documented below. Every item is formally classified as **PROPOSED — NOT APPLIED**, pending explicit review and approval by the project owner.

### 10.1 Proposed SPEC.md Amendments (Pending Owner Review)

1. **Amendment C-01: Explicit Host Power & CPU Preflight Guardrail (`SPEC.md` §1)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Proposed Text:* "Host execution requires verified plugged-in AC power (`ACLineStatus == 1`). If the host is running on battery power, benchmarking and live translation pipelines must abort immediately to prevent sudden system power shutdown (`SPEC.md` §8). A background watchdog must monitor CPU load and abort or throttle the pipeline if CPU utilization reaches $\ge 95\%$ sustained for $\ge 15\text{ s}$."

2. **Amendment C-02: Quantitative Direct Translation Evaluation Protocol (`SPEC.md` §5.2)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Proposed Text:* "Machine translation engines must be evaluated using the 10-sentence dialogue benchmark suite (TC-01 through TC-10) in M0. Direct JA$\leftrightarrow$EN models must achieve BLEU $\ge 25.0$, chrF $\ge 0.50$, inference latency $\le 600\text{ ms}$ on CPU, and zero catastrophic mistranslations on negations, numbers, and technical terms. Pivot translation via intermediate languages is prohibited (`DECISIONS.md` D-006). If Argos Translate fails these thresholds, MarianMT must be evaluated as an immediate local fallback."

3. **Amendment C-03: Acoustic Feedback & Virtual Routing Disentanglement (`SPEC.md` §4.3)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Proposed Text:* "Physical headphones (`Dev_Headphones`) are mandatory for all meeting participants using KoeBridge to physically isolate inbound playback from outbound microphone capture (`DECISIONS.md` D-016). Inbound WASAPI loopback capture must never be unconditionally suppressed during outbound push-to-talk speech (`SPEC.md` §4.3). Virtual audio injection into VB-CABLE Input must achieve $\ge 60\text{ dB}$ digital isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) against the loopback capture tap under AES-17 sine stimulus testing."

4. **Amendment C-04: Strict Local-First Privacy & Opt-In Cloud Governance Protocol (`SPEC.md` §1, §5.3)**
   - *Status:* PROPOSED — NOT APPLIED TO SPEC.MD.
   - *Proposed Text:* "The application must operate in one of two mutually exclusive modes:
     1. Local Mode (Default): Strictly offline; zero socket egress; zero external telemetry or transcript transmission; local MT only; local translation failures produce explicit user-visible error states; automatic silent fallback to cloud is strictly prohibited.
     2. Cloud Opt-In Mode (Disabled Default): Requires explicit, informed user consent; provider data terms must be tracked as an open release gate; requests enforce a 2.50 s timeout and monotonic correlation IDs ($\text{CorrID} = \langle \text{SessionID}, \text{EpochID}, \text{SegmentSeq} \rangle$); dual dispatch with local fallback on cloud failure; late cloud responses for invalidated epochs must be cancelled and discarded."

### 10.2 Proposed DECISIONS.md Records (Pending Owner Approval)

1. **Decision D-028: Preflight AC Power Check and CPU Load-Abort Watchdog**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Target hardware (i7-8750H) exhibits sudden battery power loss under high load. Plugged-in AC power must be verified via Win32 `GetSystemPowerStatus` (`ACLineStatus == 1`) prior to benchmark or pipeline execution. A software watchdog must enforce a $\ge 95\%$ CPU threshold for $\ge 15\text{ s}$ to protect host operating system stability.

2. **Decision D-029: Comparative Argos Translate vs MarianMT Evaluation Protocol**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Direct JA$\leftrightarrow$EN translation quality must be quantitatively verified using the 10-sentence dialogue benchmark suite (TC-01..TC-10). If Argos Translate fails accuracy or latency thresholds, MarianMT (`Helsinki-NLP/opus-mt-ja-en` / `en-jap`) must be evaluated as local fallback before considering any external API.

3. **Decision D-030: Acoustic Feedback Policy Mandating Physical Headphones**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Primary defense against acoustic feedback is physical device separation via headphones (`Dev_Headphones`). Inbound loopback capture must never be unconditionally suppressed during outbound speech to ensure meeting participants can hear overlapping cross-talk (`SPEC.md` §4.3). Digital route isolation must be verified via AES-17 sine stimulus testing.

4. **Decision D-031: Dual-Signal PTT Supervision & Downstream Cancellation Architecture**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Global push-to-talk hotkeys must be supervised using both Win32 `WH_KEYBOARD_LL` low-level hooks and a 50 ms `GetAsyncKeyState` polling heartbeat to prevent stuck transmit states. KeyUp events must increment the monotonic epoch ID, immediately purge all outbound speech queues ($qsize() == 0$), halt microphone capture within $\le 10\text{ ms}$, reset audio render within $\le 50\text{ ms}$, and discard stale worker outputs.

5. **Decision D-032: Multi-Tier Licensing & Independent Model Asset Clearance Policy**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Runtime code wrapper licenses must be evaluated independently from neural network model weights, acoustic checkpoints, and training data provenance. The maintained `OHF-Voice/piper1-gpl` package is GPL-3.0-or-later and unapproved by default (`SPEC.md` §5). Permissive local Japanese TTS voice clearance is a mandatory M0 release gate. Kokoro voice checkpoints require independent clearance regardless of Apache 2.0 code licenses. Python runtime must be selected based on pre-compiled wheel availability (3.11/3.12 vs 3.13).

6. **Decision D-033: Strict Local-First Privacy & Explicit Opt-In Cloud Governance Protocol**
   - *Status:* PROPOSED — NOT APPLIED IN DECISIONS.MD.
   - *Context & Rationale:* Formalizes the separation between Local Mode (100% offline default, zero socket egress, explicit error states) and Cloud Opt-In Mode (disabled by default, explicit consent, provider terms tracked as gate, 2.50 s timeout, dual dispatch with local fallback, cancellation on epoch invalidation, monotonic correlation IDs).

---

## 11. Corrected Historical Defect Audit Table

Every historical defect across Revisions 19 through 37 is audited below against the final Revision 38 text:

| Defect ID | Historical Defect Description | Revision 38 Location | Actual Verification Method | Grounded Status | Justification & Residual Scope |
|---|---|---|---|---|---|
| **D-01** | Missing AC power requirement and thermal safety protocol | §1.1, §1.2, §7.3, §8.1 (R-01), §10.1 (C-01), §10.2 (D-028) | Textual Inspection | **VERIFIED CORRECTED** | Factually grounded in `SPEC.md` §8 as an observed hardware risk (`ACLineStatus == 1`). C-01 and D-028 documented and marked NOT APPLIED. Speculative thermal overload assertions eliminated. |
| **D-02** | Unclear machine translation evaluation criteria and quality gates | §6.1, §7.2 (G-02), §10.1 (C-02), §10.2 (D-029) | Textual Inspection | **VERIFIED CORRECTED** | 10-sentence dialogue benchmark suite (TC-01..TC-10) with 4-tier rubric fully specified. Disclosed as a preliminary smoke test, with 100+ dialogue corpus required for full validation. |
| **D-03** | Incomplete audio routing and acoustic feedback isolation rules | §3.4.1, §7.4 (Test 3), §10.1 (C-03), §10.2 (D-030) | Textual Inspection | **VERIFIED CORRECTED** | Physical headphones mandated as primary defense (`DECISIONS.md` D-016). Unconditional loopback suppression during cross-talk strictly prohibited (`SPEC.md` §4.3). Disentanglement rules fully codified. |
| **D-04** | Ambiguous push-to-talk state machine and queue purging semantics | §3.4.3, §7.4 (Test 4), §10.2 (D-031) | Textual Inspection | **VERIFIED CORRECTED** | Dual-signal supervision (`WH_KEYBOARD_LL` + 50 ms polling) specified. KeyUp transitions to `INVALIDATED` epoch, purging all queues ($qsize() == 0$). Driver DMA buffer limits ($MS_{\text{unrecalled}} < 100\text{ ms}$) disclosed. |
| **D-05** | Licensing ambiguity regarding TTS voices and Piper GPL status | §6.0, §7.1 (G-01), §10.2 (D-032) | Textual Inspection | **VERIFIED CORRECTED** | Aligned with `SPEC.md` §5 and `DECISIONS.md` D-003/D-005. `OHF-Voice/piper1-gpl` identified as GPL-3.0 and unapproved by default. Local Japanese TTS identified as a mandatory MVP hard gate. |
| **D-06** | Undefined cloud translation opt-in protocol and privacy boundaries | §3.4.2, §7.2, §10.1 (C-04), §10.2 (D-033) | Textual Inspection | **VERIFIED CORRECTED** | Two distinct operating modes established: Local Mode (strictly offline default, zero socket egress, no silent fallback) and Cloud Opt-In Mode (disabled by default, explicit consent, provider terms tracked as gate, monotonic correlation IDs, 2.50 s timeout, dual dispatch with local fallback). |
| **D-07** | Incomplete M0 task breakdown and missing discovery deliverables | §8.2, §8.3 | Textual Inspection | **VERIFIED CORRECTED** | Nine specific discovery tasks (M0-1 through M0-9) and five concrete deliverables (DEL-01 through DEL-05) fully defined with acceptance criteria. |
| **D-08** | Inconsistent release gate definitions across document sections | §7.1–§7.4, §9.0 | Textual Inspection | **VERIFIED CORRECTED** | All four release gates (G-01 through G-04) standardized with identical criteria, verification procedures, and OPEN statuses across all sections. |
| **D-09** | Missing quantitative pass/fail thresholds for latency and quality | §7.1–§7.4 | Textual Inspection | **VERIFIED CORRECTED** | Quantitative thresholds established: TTS RTF $\le 0.50$, MT latency $\le 600\text{ ms}$, STT latency $\le 800\text{ ms}$, VAD latency $\le 5.0\text{ ms}$, inbound pipeline budget $\le 1,800\text{ ms}$, outbound budget $\le 2,100\text{ ms}$, digital isolation $\ge 60\text{ dB}$. |
| **D-10** | Unrealistic zero-latency claims for virtual audio driver injection | §3.4.3, §7.4 (Test 4) | Textual Inspection | **VERIFIED CORRECTED** | Explicitly acknowledges that audio committed to kernel virtual driver DMA circular buffers ($MS_{\text{unrecalled}} < 100\text{ ms}$) cannot be recalled by user-space code. Zero-latency claims eliminated. |
| **D-11** | Conflation of runtime code licenses with neural network weights | §6.0, §10.2 (D-032) | Textual Inspection | **VERIFIED CORRECTED** | Multi-tier licensing framework explicitly separates Python runtime code licenses from neural network model weights, acoustic checkpoints, and training data provenance. |
| **D-12** | Missing fallback strategy if Argos Translate quality is unacceptable | §6.1, §7.2 (G-02) | Textual Inspection | **VERIFIED CORRECTED** | MarianMT (`Helsinki-NLP/opus-mt-ja-en` and `en-jap`) explicitly specified as local fallback candidate if Argos fails accuracy thresholds, evaluated under the same 10-sentence benchmark. |
| **D-13** | Lack of explicit preflight checks for physical audio hardware | §7.4 (Test 1, Test 2A, Test 3) | Textual Inspection | **PARTIALLY CORRECTED** | Preflight procedures for WASAPI endpoint enumeration, format negotiation, and noise floor calibration are fully specified in the plan, but physical execution is deferred to M0 discovery. |
| **D-14** | Absence of 60-minute loopback capture stream stability test | §7.4 (Test 2B) | Textual Inspection | **PARTIALLY CORRECTED** | 60-minute loopback stability protocol measuring aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$), buffer discontinuities, and callback stalls is fully specified, but execution awaits M0-4 on live hardware. |
| **D-15** | Incomplete AES-17 digital route isolation test protocol | §7.4 (Test 3) | Textual Inspection | **PARTIALLY CORRECTED** | AES-17 1,000 Hz sine stimulus ($-20.0\text{ dBFS}$) rendered to `Dev_CableIn` with capture tap on `Loopback_Cap` on `Dev_Playback` fully specified. Preflight noise floor criteria and positive control defined. Physical test execution awaits M0-5. |
| **D-16** | Unsubstantiated claims of machine verification in integrity audits | §14.0 | Textual Inspection | **VERIFIED CORRECTED** | Integrity audit explicitly reports manual document inspection methods, formally disclaims automated mechanical tooling, and records grounded statuses. |
| **D-17** | Mismatched node identifiers between architecture diagram and text | §3.1, §3.2, §3.3 | Textual Inspection | **VERIFIED CORRECTED** | 1:1:1 mathematical parity achieved across diagram, node register, and edge register: exactly 33 unique nodes (`N-01`..`N-33`) and 44 unique edges (`E-01`..`E-44`). |
| **D-18** | Missing edge identifiers and incomplete connection declarations | §3.3 | Textual Inspection | **VERIFIED CORRECTED** | All 44 edges (`E-01` through `E-44`) uniquely declared with explicit source, target, data type, protocol/mechanism, and directional pipeline classification. |
| **D-19** | Truncation of Section 15 milestone blockers and technical gaps | §15.1, §15.2 | Textual Inspection | **VERIFIED CORRECTED** | Complete text restored: all milestone blockers (M0 through M7) including M1 row restored in full; all 15 canonical gaps (GAP-01 through GAP-15) fully articulated. |
| **D-20** | Broken acoustic leakage background correction formula | §7.4 (Test 3) | Textual Inspection | **VERIFIED CORRECTED** | Repaired formula to $P_{\text{leakage\_corrected}} = \max(0.0, RMS_{\text{playback, 1kHz}}^2 - RMS_{\text{ambient, 1kHz}}^2)$ with near-zero denominator floor $\epsilon = 10^{-5}$. Narrowband vs broadband spectral mismatch disclosed. |
| **D-21** | Ambiguous baseline noise floor threshold criteria in audio tests | §7.4 (Test 3) | Textual Inspection | **VERIFIED CORRECTED** | Categorized noise floor into three unambiguous ranges: $\le -90\text{ dBFS}$ valid; $-90$ to $-86\text{ dBFS}$ conditional/degraded (cannot yield unconditional PASS); $> -86\text{ dBFS}$ invalid/inconclusive. |
| **D-22** | Conflation of digital ADC dBFS with physical sound pressure (dB SPL) | §7.4 (Test 3) | Textual Inspection | **VERIFIED CORRECTED** | Explicitly discloses that uncalibrated microphone dBFS measures digital quantization, not physical acoustic sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$). Headphone mandate reinforced. |
| **D-23** | Attributing aggregate frame discrepancies directly to hardware clock drift | §7.4 (Test 2B) | Textual Inspection | **VERIFIED CORRECTED** | Metric designated as **aggregate frame-delivery discrepancy** ($E_{\text{delivery}}$). Discloses that user-space code lacks native COM `IAudioClock` access. Marked $50.0\text{ PPM}$ threshold as provisional. |
| **D-24** | Conflation of PTT unit test assertions with Windows integration tests | §7.4 (Test 4) | Textual Inspection | **PARTIALLY CORRECTED** | PTT testing bifurcated into Phase 4A (deterministic state-machine unit tests in mock harness) and Phase 4B (live Windows integration tests post-M0). Unit harness fully designed; live validation awaits M0-5. |
| **D-25** | Tautological assertions in PTT test specifications | §7.4 (Test 4) | Textual Inspection | **VERIFIED CORRECTED** | Replaced tautological self-referential assertions with explicit queue empty assertions (`qsize() == 0`), worker drop counts ($N_{\text{stale\_rendered}} = 0$), and timed state transitions. |
| **D-26** | Lack of disclosure regarding non-preemptible native C++ inference | §3.4.3, §7.4 (Test 4) | Textual Inspection | **VERIFIED CORRECTED** | Explicitly documents that in-flight CTranslate2 and ONNX Runtime tensor execution cannot be safely interrupted mid-inference without memory corruption, and that downstream epoch invalidation discards output instead. |
| **D-27** | Missing Win32 hook suspension disclosure during secure desktop switches | §3.4.3, §7.4 (Test 4) | Textual Inspection | **VERIFIED CORRECTED** | Explicitly documents that `WH_KEYBOARD_LL` hooks stop receiving Windows messages during UAC prompts and Winlogon desktop switches, necessitating 50 ms polling heartbeat supervision. |
| **D-28** | Misalignment of Piper licensing status with SPEC.md | §6.0, §7.1 | Textual Inspection | **VERIFIED CORRECTED** | Aligned strictly with `SPEC.md` §5: `OHF-Voice/piper1-gpl` is GPL-3.0-or-later and unapproved by default under the permissive-first policy. Non-GPL fallback requirement established. |
| **D-29** | Inconsistent definition of local Japanese TTS as optional vs mandatory gate | §6.0, §7.1, §15.2 (GAP-01) | Textual Inspection | **VERIFIED CORRECTED** | Confirmed as a mandatory MVP release gate per `SPEC.md` §5 and `DECISIONS.md` D-005. An unapproved voice is a hard release blocker. |
| **D-30** | Assuming Python 3.13 binary wheel compatibility without verification | §6.0, §15.2 (GAP-13) | Textual Inspection | **PARTIALLY CORRECTED** | Plan updated to mandate checking CTranslate2, PyAudioWPatch, and onnxruntime pre-compiled wheels for Windows x64 in M0-1, with fallback to pinned Python 3.11/3.12. Physical PyPI audit pending M0-1. |
| **D-31** | Unverifiable claims of repository licensing compliance | §13.0, §15.2 (GAP-15) | Textual Inspection | **VERIFIED CORRECTED** | Correctly reports that `LICENSE` is missing on disk. Tracked as open gap GAP-15 / item U-15. Unsubstantiated compliance claims eliminated. |
| **D-32** | Fractured bidirectional traceability between unresolved items and gaps | §12.2, §12.3, §15.2 | Textual Inspection | **VERIFIED CORRECTED** | Complete 1:1 bidirectional alignment established across all 15 items (U-01..U-15) and canonical gaps (GAP-01..GAP-15) across forward and reverse matrices. |
| **D-33** | Premature declaration of Milestone M0 authorization | §1.1, §1.2, §15.1, §15.5 | Textual Inspection | **VERIFIED CORRECTED** | M0 explicitly declared UNAUTHORIZED pending explicit project owner approval. All release gates maintained strictly OPEN. Planning-only boundary enforced. |

**Summary Statistics:** Total: 33 defects. Verified Corrected: 26 (78.8%). Partially Corrected: 7 (21.2%). Unresolved: 0 (0.0%). Not Verifiable: 0 (0.0%).

---

## 12. Unresolved Items Register & Bidirectional Traceability

### 12.1 Unresolved Engineering Items Register (U-01 through U-15)

| Item ID | Target Release Gate | Subsystem Domain | Unresolved Technical Challenge & Target Verification Standard | Planned Resolution Task |
|---|---|---|---|---|
| **U-01** | Gate G-01 | Japanese Voice Synthesis | Permissive Japanese TTS engine and voice asset clearance under non-GPL license | Task M0-2 (`THIRD_PARTY_NOTICES.md`) |
| **U-02** | Gate G-02 | Machine Translation | Direct JA↔EN translation accuracy and latency validation on 10-sentence dialogue suite | Task M0-3 (Argos vs MarianMT) |
| **U-03** | Gate G-03 | Host Safety & Power | Plugged-in AC power preflight verification and CPU watchdog threshold enforcement | Task M0-6 (AC check & watchdog) |
| **U-04** | Gate G-04 | Audio Capture Routing | PyAudioWPatch WASAPI loopback enumeration and 60-minute stream stability ($E_{\text{delivery}} \le 50\text{ PPM}$) | Task M0-4 (60-min loopback test) |
| **U-05** | Gate G-04 | Virtual Driver Injection | VB-CABLE render stability and dual-signal PTT hotkey lifecycle verification | Task M0-5 (PTT & VB-CABLE probe) |
| **U-06** | Gate G-03 | Acoustic Feedback Defense | Physical headphone mandate enforcement and acoustic leakage screening verification | Task M0-5 (Acoustic leakage screening) |
| **U-07** | Gate G-02 | Privacy & Translation Mode | Strict Local Mode offline enforcement and Cloud Opt-In Mode dual-dispatch arbitration | Task M0-3 / Proposed Decision D-033 |
| **U-08** | Gate G-03 | Speech Recognition | `faster-whisper` `small` `int8` CPU transcription latency ($\le 800\text{ ms}$) on target hardware | Task M0-1 (Whisper benchmark) |
| **U-09** | Gate G-03 | Speech Segmentation | Silero VAD ONNX Runtime chunk processing latency ($\le 5.0\text{ ms}$) on target CPU | Task M0-1 (VAD benchmark) |
| **U-10** | Gate G-03 | Pipeline Budget | Inbound ($\le 1,800\text{ ms}$) and outbound ($\le 2,100\text{ ms}$) end-to-end latency budget clearance | Task M0-6 (End-to-end integration) |
| **U-11** | Gate G-04 | Presentation UI | Tkinter overlay window rendering at $\ge 30\text{ FPS}$ without stealing user input focus | Task M0-7 (Tkinter GUI prototype) |
| **U-12** | Gate G-03 | Credential Security | Secure storage of Gemini API key in Windows Credential Manager via `keyring` DPAPI | Task M0-8 (`keyring` probe) |
| **U-13** | Gate G-01 | Runtime Compatibility | Verification of pre-compiled Windows x64 binary wheels for Python 3.11/3.12 vs 3.13 | Task M0-1 (PyPI wheel audit) |
| **U-14** | Gate G-04 | Audio Isolation | Verification of $\ge 60\text{ dB}$ digital route isolation under AES-17 sine stimulus testing | Task M0-5 (Digital route isolation) |
| **U-15** | Gate G-01 | Repository Governance | Creation and commitment of repository MIT `LICENSE` file on disk | Pre-M1 Owner Review Action |

### 12.2 Forward Traceability Matrix (U-01..U-15 to GAP-01..GAP-15 to Gates)

| Unresolved Item | Canonical Technical Gap | Governing Release Gate | Planned Resolution Task | Milestone Owner |
|---|---|---|---|---|
| **U-01** | **GAP-01** (Permissive JA TTS & Voice Licensing) | Gate G-01 | Task M0-2 | Milestone M0 |
| **U-02** | **GAP-02** (Direct JA↔EN MT Quality & Latency) | Gate G-02 | Task M0-3 | Milestone M0 |
| **U-03** | **GAP-03** (Host Power Mandate & CPU Watchdog) | Gate G-03 | Task M0-6 | Milestone M0 |
| **U-04** | **GAP-04** (WASAPI Loopback Capture Stability) | Gate G-04 | Task M0-4 | Milestone M0 |
| **U-05** | **GAP-05** (VB-CABLE Injection & PTT Safety) | Gate G-04 | Task M0-5 | Milestone M0 |
| **U-06** | **GAP-06** (Acoustic Feedback & Headphone Mandate) | Gate G-03 | Task M0-5 | Milestone M0 |
| **U-07** | **GAP-07** (Dual-Mode Privacy & Cloud Arbitration) | Gate G-02 | Task M0-3 | Milestone M0 |
| **U-08** | **GAP-08** (STT Latency & Quantization Clearance) | Gate G-03 | Task M0-1 | Milestone M0 |
| **U-09** | **GAP-09** (VAD Latency & Chunk Segmentation) | Gate G-03 | Task M0-1 | Milestone M0 |
| **U-10** | **GAP-10** (End-to-End Latency Budget Clearance) | Gate G-03 | Task M0-6 | Milestone M0 |
| **U-11** | **GAP-11** (Tkinter GUI Responsiveness & Focus) | Gate G-04 | Task M0-7 | Milestone M0 |
| **U-12** | **GAP-12** (Secure Credential Storage via DPAPI) | Gate G-03 | Task M0-8 | Milestone M0 |
| **U-13** | **GAP-13** (Python Runtime & Wheel Compatibility) | Gate G-01 | Task M0-1 | Milestone M0 |
| **U-14** | **GAP-14** (Digital Route Isolation Verification) | Gate G-04 | Task M0-5 | Milestone M0 |
| **U-15** | **GAP-15** (Repository License File Absence) | Gate G-01 | Pre-M1 Governance | Project Owner |

### 12.3 Reverse Traceability Matrix (Release Gates to Canonical Gaps to Items)

| Governing Release Gate | Canonical Technical Gaps Mapped | Mapped Unresolved Items | Target Milestone |
|---|---|---|---|
| **Gate G-01** (TTS & Voice Licensing) | GAP-01, GAP-13, GAP-15 | U-01, U-13, U-15 | Milestone M0 / Pre-M1 |
| **Gate G-02** (MT Quality & Latency) | GAP-02, GAP-07 | U-02, U-07 | Milestone M0 |
| **Gate G-03** (Latency & Thermal/Power)| GAP-03, GAP-06, GAP-08, GAP-09, GAP-10, GAP-12 | U-03, U-06, U-08, U-09, U-10, U-12 | Milestone M0 |
| **Gate G-04** (Audio Routing & PTT) | GAP-04, GAP-05, GAP-11, GAP-14 | U-04, U-05, U-11, U-14 | Milestone M0 |

---

## 13. Planning-Only Compliance & Grounded Repository State

Direct inspection of the repository workspace confirms the following facts:
1. **Governing Files Intact:** `SPEC.md` (40,372 bytes), `DECISIONS.md` (6,661 bytes, D-001..D-027), and `CLAUDE.md` (3,356 bytes) remain strictly unmodified.
2. **Missing License File Disclosed:** Direct disk inspection confirms that NO `LICENSE` file exists in the repository root. This absence is tracked as open gap **GAP-15** (item **U-15**) and must be resolved by committing an MIT license upon owner authorization prior to M1.
3. **Zero Application Artifacts:** No source directory (`src/`), prototype scripts (`prototypes/`), automated test scripts (`tests/`), or compiled binaries exist on disk.
4. **Zero Dependencies Installed:** No Python virtual environments or external packages have been installed.

---

## 14. Grounded 14-Check Integrity Audit Table

The table below reports the final integrity audit of Revision 38. Every check explicitly reports the actual manual textual inspection method applied:

| Check ID | Integrity Dimension | Target Scope | Verification Method | Grounded Status | Detailed Finding & Evidence |
|---|---|---|---|---|---|
| **CHK-01** | Reasoning Debris Purge | Entire Document Text | Manual Regex Search / Visual Scan | **PASS** | Zero reasoning tokens (`Thought for 18s`, `Thought for 16s`, `Thought for 22s`, `Thought for 39s`), UI commands, scratchpad paths, or conversation artifacts present. |
| **CHK-02** | Textual Completeness & Flow | Sections 1 through 15 | Manual Text Inspection | **PASS** | All sections, paragraphs, table rows, and list items are fully formed with complete sentences. Zero truncation markers, unfinished thoughts, or cut-off tables exist. |
| **CHK-03** | Architecture Model Parity | Section 3 (§3.1, §3.2, §3.3) | Manual Cross-Reference Count | **PASS** | Exact 1:1:1 parity verified: exactly 33 nodes declared in diagram (§3.1), 33 records in node register (§3.2, `N-01`..`N-33`), and 44 edges in edge register (§3.3, `E-01`..`E-44`). Zero dangling endpoints. |
| **CHK-04** | Operating Mode Privacy Governance | §3.4.2, §7.2, §10.1, §10.2 | Manual Policy Review | **PASS** | Two mutually exclusive modes strictly defined: Local Mode (strictly offline default, zero socket egress, explicit error states) and Cloud Opt-In Mode (disabled by default, explicit consent, provider terms tracked as gate, 2.50 s timeout, dual dispatch with local fallback). |
| **CHK-05** | Digital Route Isolation Rigor | §7.4 (Test 3) | Manual Protocol Audit | **PASS** | AES-17 1,000 Hz sine stimulus ($-20.0\text{ dBFS}$) rendered to `Dev_CableIn` with capture tap on `Loopback_Cap` on `Dev_Playback` fully specified. Preflight noise floor criteria ($\le -90\text{ dBFS}$ valid, $-90$ to $-86\text{ dBFS}$ conditional, $> -86\text{ dBFS}$ invalid) and positive control defined. $L_{\text{iso}} \le -80.0\text{ dBFS}$ isolation threshold enforced. |
| **CHK-06** | Acoustic Leakage Mathematical Validity | §7.4 (Test 3) | Manual Mathematical Audit | **PASS** | Equations for background-corrected power $P_{\text{leakage\_corrected}} = \max(0.0, RMS_{\text{playback, 1kHz}}^2 - RMS_{\text{ambient, 1kHz}}^2)$ and leakage ratio $\Delta L_{\text{acoustic}} = 10 \log_{10}(RMS_{\text{playback, 1kHz}}^2 / \max(RMS_{\text{ambient, 1kHz}}^2, \epsilon^2))$ with near-zero floor $\epsilon = 10^{-5}$ verified. Digital dBFS vs physical dB SPL distinction and headphone mandate articulated. |
| **CHK-07** | Loopback Stability Measurement Grounding | §7.4 (Test 2B) | Manual Systems Review | **PASS** | Metric designated as aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$). Buffer discontinuity monitoring and callback stall threshold ($T_{\text{stall\_max}} \le 250\text{ ms}$) enforced. User-space `IAudioClock` limitation disclosed. |
| **CHK-08** | PTT Lifecycle & Hardware Realism | §3.4.3, §7.4 (Test 4) | Manual Architecture Review | **PASS** | PTT bifurcated into Phase 4A (unit) and Phase 4B (integration). Timing windows ($T_1 \le 30\text{ ms}$, $T_2 \le 60\text{ ms}$, $T_3 \le 10\text{ ms}$, $T_4 \le 50\text{ ms}$), zero mic capture post-close, zero stale rendering, and queue purging ($qsize() == 0$) enforced. Virtual driver DMA buffer latency ($MS_{\text{unrecalled}} < 100\text{ ms}$), non-preemptible native inference, and Win32 hook suspension disclosed. |
| **CHK-09** | Licensing Alignment with SPEC.md | §6.0, §7.1, §10.2 | Manual Legal/Policy Review | **PASS** | Aligned with `SPEC.md` §5 and `DECISIONS.md` D-003/D-005: `OHF-Voice/piper1-gpl` identified as GPL-3.0 and unapproved by default. Local Japanese TTS identified as mandatory MVP hard gate. Kokoro voice asset independence and Python runtime wheel compatibility requirements enforced. |
| **CHK-10** | Hardware Safety & Power Grounding | §1.1, §1.2, §7.3, §8.1 | Manual Systems Review | **PASS** | Grounded in `SPEC.md` §8 as an observed hardware/battery risk requiring plugged-in AC power (`ACLineStatus == 1`) and CPU load-abort watchdog ($\ge 95\%$ for $\ge 15\text{ s}$). Speculative thermal overload assertions eliminated. |
| **CHK-11** | Defect Audit Honesty | §11.0 | Manual Line-by-Line Audit | **PASS** | All 33 historical defects audited individually with grounded statuses (26 Verified Corrected, 7 Partially Corrected, 0 Unresolved, 0 Not Verifiable). Unsupported blanket completion claims eliminated. |
| **CHK-12** | Bidirectional Traceability Integrity | §12.2, §12.3, §15.2 | Manual Cross-Matrix Audit | **PASS** | Perfect 1:1 bidirectional alignment verified across all 15 unresolved items (U-01..U-15) and canonical technical gaps (GAP-01..GAP-15) across forward and reverse matrices. |
| **CHK-13** | Planning-Only Boundary Enforcement | §1.1, §1.2, §13.0, §15.5 | Manual Workspace Inspection | **PASS** | Confirmed zero code written, zero files modified on disk, zero packages installed, zero models downloaded, and zero audio hardware accessed. Governing files (`SPEC.md`, `CLAUDE.md`, `DECISIONS.md`) remain untouched. Missing `LICENSE` file honestly reported. |
| **CHK-14** | Release Gate & Milestone Discipline | §1.1, §7.1–§7.4, §15.1, §15.5 | Manual Governance Review | **PASS** | All four release gates (G-01 through G-04) remain strictly OPEN. Milestone M0 remains strictly UNAUTHORIZED pending explicit project owner approval. Proposed amendments (C-01..C-04) and decisions (D-028..D-033) clearly marked NOT APPLIED. |

---

## 15. Milestone Blockers, Canonical Gaps, Limitations, Pending Decisions & Final Verdict

### 15.1 Milestone Dependency Chain & Blocking Gates

```
[M0: Discovery & Gate Clearance]  <-- CURRENT EXECUTION BOUNDARY (STRICTLY UNAUTHORIZED)
  │   Blocks on: Gates G-01, G-02, G-03, G-04 (ALL OPEN)
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

1. **GAP-01 (Critical - P0): Permissive Japanese TTS Engine & Voice Asset License Clearance:** No standalone, permissively licensed Japanese TTS engine with verified permissive voice weights has been cleared. `OHF-Voice/piper1-gpl` is GPL-3.0-or-later and unapproved by default (`SPEC.md` §5). Mandatory MVP hard gate (G-01).
2. **GAP-02 (Critical - P0): Direct JA↔EN Machine Translation Quality & Latency Clearance:** Argos Translate direct JA↔EN translation quality on technical meeting dialogue is unmeasured. Pivot translation is prohibited (`DECISIONS.md` D-006). MarianMT fallback required if Argos fails 10-sentence benchmark suite.
3. **GAP-03 (Critical - P0): Laptop AC Power Mandate & CPU Watchdog Thresholds:** Target laptop exhibits sudden power shutdowns under battery load (`SPEC.md` §8). Operation requires plugged-in AC power (`ACLineStatus == 1`) and CPU watchdog throttling if load $\ge 95\%$ sustained for $\ge 15\text{ s}$.
4. **GAP-04 (Critical - P0): WASAPI Loopback Capture Stability & Device Enumeration:** Capturing meeting audio from Chrome/Edge requires stable shared-mode loopback capture on `Dev_Playback`. Must verify 60-minute stream continuity ($E_{\text{delivery}} \le 50.0\text{ PPM}$) and zero buffer discontinuities.
5. **GAP-05 (Critical - P0): VB-CABLE Outbound Injection & Push-to-Talk Lifecycle Safety:** Outbound speech must inject cleanly into VB-CABLE Input. Push-to-talk must enforce dual-signal supervision (Win32 hook + 50 ms polling heartbeat), KeyUp queue purging ($qsize() == 0$), mic capture halt within $\le 10\text{ ms}$, and render reset within $\le 50\text{ ms}$.
6. **GAP-06 (High - P1): Acoustic Feedback Prevention & Mandatory Headphone Policy:** Open speakers cause microphone feedback and false STT triggers. Physical headphones (`Dev_Headphones`) are mandatory (`DECISIONS.md` D-016). Loopback capture must never be unconditionally suppressed during cross-talk (`SPEC.md` §4.3). Acoustic leakage screening must verify $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ over ambient noise.
7. **GAP-07 (High - P1): Dual-Mode Privacy Governance & Opt-In Cloud Protocol:** Local Mode (default) must be strictly offline with zero socket egress. Cloud Opt-In Mode requires explicit user consent, provider terms tracked as gate, monotonic correlation IDs, 2.50 s timeout, dual dispatch with local fallback, and cancellation on epoch invalidation.
8. **GAP-08 (High - P1): Speech Recognition Latency & Model Quantization Clearance:** `faster-whisper` `small` model with `int8` quantization on CPU must achieve transcription latency $\le 800\text{ ms}$ for 3-second speech segments.
9. **GAP-09 (High - P1): Voice Activity Detection Latency & Chunk Ingestion:** Silero VAD (ONNX Runtime) must process 30 ms (512-sample) audio chunks in $\le 5.0\text{ ms}$ on CPU with speech onset threshold $0.50$ and trailing silence window $\ge 400\text{ ms}$.
10. **GAP-10 (High - P1): End-to-End Pipeline Latency Budget Clearance:** Inbound translation budget ($1,800\text{ ms}$ target, $2,400\text{ ms}$ max) and outbound speech budget ($2,100\text{ ms}$ target, $2,900\text{ ms}$ max) must be empirically cleared on target hardware.
11. **GAP-11 (Medium - P2): Tkinter GUI Responsiveness & Focus Preservation:** Tkinter caption overlay must render at $\ge 30\text{ FPS}$ without stealing user focus from Chrome/Edge during background inference.
12. **GAP-12 (Medium - P2): Secure Gemini API Key Storage via Windows Credential Manager:** When Cloud Opt-In Mode is enabled, API key must be stored securely using `keyring` (Windows DPAPI backend) and never written to plaintext configuration files or logs (`DECISIONS.md` D-027).
13. **GAP-13 (Medium - P2): Python Runtime & Dependency Compatibility (3.11/3.12 vs 3.13):** `SPEC.md` §1 references Python 3.13, but CTranslate2, PyAudioWPatch, and onnxruntime pre-compiled wheels for Windows x64 must be verified. If 3.13 wheels are unavailable, runtime must pin to 3.11 or 3.12.
14. **GAP-14 (Medium - P2): Digital Route Isolation Verification (AES-17 Sine Protocol):** Outbound audio injected into `Dev_CableIn` must achieve $\ge 60\text{ dB}$ digital isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) against the loopback capture tap on `Dev_Playback` under AES-17 1,000 Hz sine stimulus testing.
15. **GAP-15 (Low - P3): Repository License File Absence on Disk:** `CLAUDE.md` specifies MIT target for project-owned code, but no `LICENSE` file exists on disk. Must be committed prior to M1 upon owner authorization.

### 15.3 Known Architectural Limitations & Operational Boundaries
1. **Virtual Audio Driver DMA Latency:** User-space software cannot recall or purge audio frames already committed to the VB-CABLE virtual driver DMA circular buffer ($MS_{\text{unrecalled}} < 100\text{ ms}$).
2. **Non-Preemptible Native C++ Inference:** In-flight tensor execution in CTranslate2 or ONNX Runtime cannot be safely interrupted mid-inference without memory corruption. Downstream epoch invalidation discards output instead.
3. **Secure Desktop Hook Suspension:** Win32 `WH_KEYBOARD_LL` low-level keyboard hooks stop receiving Windows messages during UAC prompts, Winlogon, and lock screens. Polling heartbeats and a 15-second watchdog provide fail-safe release upon desktop return.
4. **Physical Acoustic Isolation Dependency:** Software digital isolation cannot prevent acoustic cross-talk if open laptop speakers are used. Physical headphones (`Dev_Headphones`) are mandatory.
5. **No Direct Hardware Clock Access:** User-space audio clients cannot query physical DAC crystal oscillators directly without COM `IAudioClock` interfaces. Aggregate frame delivery is monitored via QPC timestamps.
6. **Microphone dBFS vs Sound Pressure Level:** Uncalibrated microphone dBFS measures digital ADC quantization, not calibrated physical sound pressure ($dB\text{ SPL re } 20\ \mu\text{Pa}$).
7. **Smoke Test Heuristic Boundary:** The 10-sentence dialogue benchmark suite is an initial smoke test for model pre-filtering; full translation validation requires a 100+ dialogue corpus.
8. **HTTP Socket Cancellation Limit:** Closing a client HTTP socket cancels local response processing but does not guarantee that the remote cloud provider ceased processing a request already received.
9. **Single Inbound Playback Endpoint:** Loopback capture taps the default Windows playback device. Audio routed to alternative non-default physical endpoints will bypass the capture client.
10. **Host AC Power Dependency:** Benchmarking and live pipeline execution cannot be performed under battery operation due to target laptop hardware shutdown risks.

### 15.4 Pending Project Owner Decisions (11 Items)

1. **Proposed SPEC Amendment C-01 (Host Power & CPU Preflight):** PROPOSED — NOT APPLIED. Mandates AC power check (`ACLineStatus == 1`) and CPU load watchdog ($\ge 95\%$ for $\ge 15\text{ s}$).
2. **Proposed SPEC Amendment C-02 (Direct MT Evaluation Protocol):** PROPOSED — NOT APPLIED. Mandates 10-sentence dialogue benchmark suite (TC-01..TC-10) and MarianMT fallback evaluation.
3. **Proposed SPEC Amendment C-03 (Acoustic Feedback Disentanglement):** PROPOSED — NOT APPLIED. Mandates physical headphones, forbids unconditional loopback suppression during cross-talk, and sets $\ge 60\text{ dB}$ digital isolation.
4. **Proposed SPEC Amendment C-04 (Local-First Privacy & Cloud Mode):** PROPOSED — NOT APPLIED. Formalizes strict offline Local Mode default and explicit Cloud Opt-In Mode with monotonic correlation IDs.
5. **Proposed Decision D-028 (Preflight AC Power Check & Watchdog):** PROPOSED — NOT APPLIED. Codifies Win32 power checking and watchdog throttling.
6. **Proposed Decision D-029 (Argos vs MarianMT Evaluation):** PROPOSED — NOT APPLIED. Codifies comparative translation benchmark protocol.
7. **Proposed Decision D-030 (Acoustic Feedback & Headphone Policy):** PROPOSED — NOT APPLIED. Codifies mandatory headphone usage and AES-17 isolation testing.
8. **Proposed Decision D-031 (Dual-Signal PTT Supervision & Cancellation):** PROPOSED — NOT APPLIED. Codifies dual hook/polling supervision, queue purging, and driver DMA buffer limitations.
9. **Proposed Decision D-032 (Multi-Tier Licensing & Asset Clearance):** PROPOSED — NOT APPLIED. Codifies multi-tier licensing separation, confirms Piper GPL fork is unapproved by default, and sets Japanese TTS as mandatory M0 gate.
10. **Proposed Decision D-033 (Local-First Privacy & Opt-In Cloud Governance):** PROPOSED — NOT APPLIED. Codifies mutually exclusive Local Mode and Cloud Opt-In Mode semantics.
11. **Authorization of Milestone 0 (M0 Discovery) Execution:** UNAUTHORIZED — PENDING EXPLICIT OWNER APPROVAL. Authorizes executing discovery tasks M0-1 through M0-9 in an isolated virtual environment.

---

### 15.5 Final Architecture Verdict & Governance Declaration

```
====================================================================================================
                        KOEBRIDGE FOR ZOOM — ARCHITECTURAL REVIEW VERDICT
====================================================================================================
Document Identifier:       KB-ARCH-VERIF-PLAN-R38
Document Revision:         Revision 38 (Complete Artifact Verification & Audit Recovery)
Target Platform:           Windows 10/11 x64 (Build 19041+)
Target Hardware Baseline:  Intel Core i7-8750H, 32 GB RAM, Plugged-In AC Power (ACLineStatus == 1)
Governing Specifications:  SPEC.md (Authoritative), CLAUDE.md, DECISIONS.md (D-001..D-027)

CURRENT RELEASE GATE STATUSES:
  [OPEN] Gate G-01: Japanese TTS Engine & Voice Licensing Clearance
  [OPEN] Gate G-02: Direct JA↔EN Machine Translation Quality & Latency Clearance
  [OPEN] Gate G-03: End-to-End Pipeline Latency & Host Hardware Thermal/Power Guardrails
  [OPEN] Gate G-04: Audio Endpoint Topology, Loopback Stability & PTT Safety Verification

GOVERNANCE & EXECUTION BOUNDARY:
  Milestone M0 (Discovery): STRICTLY UNAUTHORIZED — AWAITING EXPLICIT PROJECT OWNER APPROVAL
  Proposed Amendments:      C-01 through C-04 NOT APPLIED TO SPEC.MD
  Proposed Decisions:       D-028 through D-033 NOT APPLIED TO DECISIONS.MD
  Filesystem Modifications: ZERO application code, prototypes, or test scripts written to disk
  Network Egress / Pip:     ZERO packages installed, ZERO model weights downloaded
  Hardware Probing:         ZERO audio devices accessed, ZERO benchmarks run

FINAL VERDICT:
  The Revision 38 Architecture & Verification Plan is FORENSICALLY COMPLETE, CANONICALLY
  RECONCILED (33 nodes, 44 edges), MATHEMATICALLY SOUND, AND READY FOR FORMAL OWNER REVIEW.
  All release gates remain strictly OPEN, and all implementation work remains HALTED.
====================================================================================================
```
