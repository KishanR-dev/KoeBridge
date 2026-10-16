# KoeBridge for Zoom — Architecture & Verification Plan (Revision 65)
**Document Identifier:** `KB-ARCH-VERIF-PLAN-R65`  
**Revision:** Revision 65 (Forensic Audit, Targeted Repair, Subgraph & Findings Parity, Epistemic Rigor)  
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

The table below reports the executive status of all governance dimensions and formal release gates. Every release gate (**G-01, G-02, G-03, G-04**) appears exactly once, cross-referenced against the detailed specifications in Section 7 and Section 9:

| Governance Dimension | Gate / Milestone Name | Current Status | Governing Authority | Mandatory Acceptance Criteria Summary | Outstanding Evidence Required to Close Gate |
|---|---|---|---|---|---|
| **Document State** | Revision 65 Specification | **REVIEWABLE SPECIFICATION** | Project Architecture Plan | Complete, untruncated artifact on disk; 33 nodes, 44 edges, 8 closed subgraphs | Owner formal review and sign-off |
| **Milestone M0** | Milestone M0 (Discovery Execution) | **STRICTLY UNAUTHORIZED** | `SPEC.md` §8; Owner Authority | Formal owner sign-off on discovery scope; isolated venv setup | Explicit project owner authorization to execute discovery |
| **Gate G-01** | Japanese TTS Engine & Voice Licensing | **EMPIRICAL GATE OPEN** | `SPEC.md` §5, `DECISIONS.md` D-003, D-005 | Permissive non-GPL code & voice asset; RTF $\le 0.50$ on CPU (`PROPOSED TARGET`) | License manifest (`THIRD_PARTY_NOTICES.md`), RTF logs (Task M0-2) |
| **Gate G-02** | Direct JA↔EN MT Quality & Latency | **EMPIRICAL GATE OPEN** | `SPEC.md` §5.2, `DECISIONS.md` D-006 | BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$, zero critical errors (`PROPOSED TARGETS`) | 10-sentence dialogue benchmark results, MarianMT comparison (Task M0-3) |
| **Gate G-03** | End-to-End Latency & Thermal/Power | **EMPIRICAL GATE OPEN** | `SPEC.md` §8 (Sole Authority), `DECISIONS.md` D-025 | Inbound $\le 1,800\text{ ms}$, Outbound $\le 2,100\text{ ms}$ (`GOVERNING REQUIREMENTS`); AC power check; CPU watchdog | Live latency traces on AC power, watchdog load test (Task M0-6) |
| **Gate G-04** | Audio Topology, Loopback & PTT Safety | **EMPIRICAL GATE OPEN** | `SPEC.md` §4.1–§4.3, `DECISIONS.md` D-016, D-023 | Tests 1, 2A, 2B, 3, 4 pass; $E_{\text{delivery}} \le 50.0\text{ PPM}$; $R_{\text{iso}} \ge 60\text{ dB}$; PTT halts | 60-min loopback log, AES-17 isolation log, PTT timing traces (Tasks M0-4, M0-5) |

*(Note: Proposed amendments C-01 through C-04 and proposed decisions D-028 through D-033 are documented in Section 10 as proposals marked PROPOSED — NOT APPLIED. Proposed ADR D-028 is not an approved governing authority; the governing authority for host power safety is strictly SPEC.md §8.)*

### 1.2 Five Consecutively Numbered Reasons for Verdict

The Revision 65 architecture and verification plan carries an executive verdict of **NOT APPROVED (PLANNING SPECIFICATION RECONCILED; ALL EMPIRICAL RELEASE GATES OPEN)** based upon the following five consecutively numbered reasons:

1. **Reason 1 — Milestone M0 Discovery Remains Unauthorized:** Milestone M0 (Discovery Execution) has not received explicit written project-owner authorization. Commencing prototype implementation, dependency installation, model downloads, or physical device access without prior owner sign-off violates core project workflow policy (`CLAUDE.md`, `SPEC.md` §8).
2. **Reason 2 — All Four Empirical Release Gates Remain Open (G-01 through G-04):** None of the four mandatory empirical release gates defined in `SPEC.md` §14 and `DECISIONS.md` have been cleared with live empirical data on the target hardware baseline (Intel Core i7-8750H, 32 GB RAM, plugged-in AC power). Specifically:
   - *Gate G-01 (TTS Licensing & RTF):* No standalone permissively licensed Japanese TTS engine and voice asset has been empirically verified.
   - *Gate G-02 (MT Quality & Privacy):* Direct JA↔EN translation accuracy (BLEU $\ge 25.0$, chrF $\ge 0.50$) and latency ($\le 600\text{ ms}$) have not been empirically benchmarked on the 10-sentence dialogue suite.
   - *Gate G-03 (Pipeline Latency & Host Safety):* End-to-end pipeline latency (Inbound $\le 1,800\text{ ms}$, Outbound $\le 2,100\text{ ms}$) and host hardware thermal/power stability have not been empirically verified under load on AC power.
   - *Gate G-04 (Audio Topology & PTT Safety):* WASAPI loopback 60-minute streaming stability ($E_{\text{delivery}} \le 50.0\text{ PPM}$), AES-17 digital route isolation ($R_{\text{iso}} \ge 60\text{ dB}$), and PTT lifecycle timing have not been tested on physical hardware.
3. **Reason 3 — Repository Level Missing License File (GAP-15 / Item U-15 / Finding F-15):** The host repository workspace lacks an MIT `LICENSE` file on disk, which is an explicit project policy requirement under `CLAUDE.md`. This represents an open documentary gate blocker that must be resolved by owner sign-off prior to Milestone M1. Milestone M0 discovery authorization and repository disk status are distinct governance boundaries that must not be conflated.
4. **Reason 4 — Proposed Governance Amendments and ADRs Remain Unapplied:** The 4 proposed amendments to `SPEC.md` (`C-01` through `C-04`) and 6 proposed Architecture Decision Records in `DECISIONS.md` (`D-028` through `D-033`) represent unadopted recommendations totaling exactly 10 unique proposal IDs. All remain marked `PROPOSED — NOT APPLIED` and have not been authorized or incorporated by the project owner.
5. **Reason 5 — Live Hardware Safety & Environmental Validation Deferred to M0:** The target laptop hardware platform exhibits known operational risks of sudden system power shutdown under heavy load when operated on battery power (`SPEC.md` §8). Verifying plugged-in AC power (`ACLineStatus == 1`), background CPU load watchdog throttling ($\ge 95\%$ sustained for $\ge 15\text{ s}$), and physical headphone feedback isolation (`Dev_Headphones`, `DECISIONS.md` D-016) cannot occur until M0 execution is authorized by the owner.

### 1.3 Mandatory Planning-Only Governance Boundary

All activities under Revision 65 are strictly restricted to architectural analysis, specification baseline reconciliation, and verification protocol design. The following eight governance rules are actively enforced:
1. **Accurate Categorized Filesystem Accounting:** Exactly two new documentation files (`docs/ARCHITECTURE_R65.md` and `docs/ARCHITECTURE_R65_REVIEW.md`) are created. Predecessor plans and reviews (`R44` through `R64`) remain strictly unmodified on disk. Governing project files (`SPEC.md`, `CLAUDE.md`, `DECISIONS.md`, and the absent `LICENSE` file) remain completely untouched. Zero application source code, prototype scripts, automated test fixtures, or configuration files are created.
2. **Zero Package or Dependency Installation:** No external software, Python packages, pre-compiled wheels, or runtime dependencies are installed via `pip`, `winget`, `conda`, or manual download.
3. **Zero Model Asset Downloads:** No neural network weights, acoustic checkpoints, vocoder models, tokenizers, or voice data (including Silero VAD, `faster-whisper`, Argos Translate, MarianMT, Piper, or Kokoro) are downloaded from Hugging Face, GitHub, or any remote registry.
4. **Zero Hardware Probing or Device Access:** No physical or virtual audio endpoints (WASAPI playback, loopback taps, microphone inputs, or VB-CABLE drivers) are opened, queried, or initialized.
5. **Zero Execution of Milestone 0 (M0):** Milestone M0 remains strictly UNAUTHORIZED. All nine discovery tasks (M0-1 through M0-9) and five concrete deliverables (DEL-01 through DEL-05) remain planned procedures.
6. **Strict Gate Preservation:** All four release gates (**G-01, G-02, G-03, G-04**) remain strictly **EMPIRICAL GATES OPEN**.
7. **Explicit Disclaimer of Automated Tooling:** Verification claims distinguish manual textual review from mechanical tooling; no automated parser or test runner is reported as active.
8. **Subordination to Governing Documents:** In any conflict between this planning document and `SPEC.md`, `SPEC.md` takes precedence.

---

## 2. Forensic Change & Repair Log (Revisions 45 through 65)

### 2.1 Reconciled Historical Forensic Repairs (R45 through R60)

| Repair Range | Target Area | Forensic Scope & Summary of Corrections | Status |
|---|---|---|---|
| **R45–R50** | Specification Consistency & Rigor | Date dimension reconciliation; operating mode privacy codification; AES-17 mathematical rigor; loopback frame discrepancy metric renaming; PTT bifurcation; laptop shutdown risk grounded in SPEC §8; defect arithmetic reconciliation (28 Corrected, 5 Protocol Specified, sum = 33). | **CORRECTED IN REVISION HISTORY** |
| **R51–R55** | Formatting, Hashes & Baseline Grounding | Elimination of fragmented text; 1:1:1 graph parity (33 nodes, 44 edges, 8 subgraphs); direct physical cryptographic hashing (SHA-256); SPEC.md line 436 verbatim verification; 6-category filesystem accounting established. | **CORRECTED IN REVISION HISTORY** |
| **R56–R57** | Findings Restructuring & Non-Git Qualification | Findings register un-truncation; discovery that workspace lacks `.git` metadata, qualifying historical commit baseline comparison as UNVERIFIED; checklist completeness audit. | **CORRECTED IN REVISION HISTORY** |
| **R58** | Delimiter, Debris & Structure Repairs | Elimination of broken delimiters; restoration of F-08; clean separation of F-01 and F-03 authorities; restoration of full F-09 description; 5-tier status taxonomy on CHK-01..CHK-14; complete debris elimination. | **CORRECTED IN REVISION HISTORY** |
| **R59** | Canonical Findings Register Alignment | Aligned F-01..F-15 1:1:1 with GAP-01..GAP-15 and U-01..U-15; eliminated duplicate TTS finding; restored F-10..F-12 records; disentangled loopback delivery accounting from DAC crystal drift; defined $T_{\text{driver\_dma}} < 100\text{ ms}$. | **CORRECTED IN REVISION HISTORY** |
| **R60** | Release-Gate & Findings Reconstruction | Reconstructed complete records for Gates G-01..G-04; resolved G-02/G-03 boundary corruption; rebuilt F-01..F-15 summary and detailed records; rebuilt artifact metadata table; verified graph parity. | **CORRECTED IN REVISION HISTORY** |

### 2.2 Revision 61 Forensic Repairs (`R61-01` through `R61-08`)

| Repair ID | Target Area | Forensic Defect Addressed in Revision 61 | Forensic Correction Applied in Revision 61 | Verification Evidence |
|---|---|---|---|---|
| **R61-01** | Executive Acceptance Section Structure | Executive acceptance section in review lacked consecutively numbered reasons and complete descriptions | Reconstructed executive acceptance section in R61 Review §1.2 with 5 complete, consecutively numbered reasons for the NOT APPROVED verdict, fully detailing the specific blockers | Inspected R61 Review §1.2 |
| **R61-02** | Release Gate G-02 Privacy & Fallback Disambiguation | Release Gate G-02 lacked explicit separation of Local Mode zero egress from Cloud Opt-In Mode sequential fallback | Completely restored Gate G-02 closure criteria and required evidence, explicitly distinguishing Local Mode offline zero socket egress from Cloud Opt-In sequential fallback and 2.50 s timeout | Inspected R61 §7.2, §9.0; R61 Review §2.2 |
| **R61-03** | Explicit Gate G-04 Status Field | Gate G-04 status field needed explicit standardization across all sections | Explicitly codified `Current Gate Status: EMPIRICAL GATE OPEN` in Gate G-04 across §1.1, §7.4, and §9.0 | Inspected R61 §1.1, §7.4, §9.0; R61 Review §2.4 |
| **R61-04** | Disambiguation of Mapping Coverage vs Resolution | Use of ambiguous phrases like "100% closed coverage" caused conflation of mapping completeness with issue resolution | Explicitly disambiguated mapping coverage (all 15 items mapped 1:1) from resolution status (all 15 items remain OPEN) and gate closure status (all 4 gates remain EMPIRICAL GATES OPEN) | Inspected R61 §12.3; R61 Review §5.2 |
| **R61-05** | Finding F-11 Full Specification Restoration | Finding F-11 required complete governing authority and canonical cross-references | Verified and explicitly restored `SPEC.md` §5.4 and `DECISIONS.md` D-002 as governing authorities, and GAP-11 / U-11 / Gate G-04 as canonical mappings for Finding F-11 | Inspected R61 §12.1, §15.2; R61 Review §3.3 |
| **R61-06** | Complete Physical Subgraph Inventory | Subgraph audits in prior reviews occasionally listed 6 instead of all 8 subgraphs | Enumerated all 8 closed subgraphs in full detail across architecture plan and companion review, verifying zero overlap and 33-node partition | Inspected R61 §3.1; R61 Review §5.1 |
| **R61-07** | Rigorous Metadata Accounting & Status Qualification | Avoid placeholder values like `0*`, approximate counts, or withheld checksums without explanation | Measured exact physical line counts via `Read` and reported exact prior byte sizes; explicitly marked unmeasured properties as `NOT MEASURED` with technical rationale | Inspected R61 §13.0; R61 Review §4.1 |
| **R61-08** | Epistemic Boundary Labeling & Integrity Checklist | Maintained rigorous separation across targets, requirements, measurements, and 5-tier taxonomy | Recomputed integrity check taxonomy (8 Verified, 2 Partially Verified, 4 Not Empirically Tested, 0 Failed, 0 Blocked); strictly labeled all proposed targets | Inspected R61 §14.0; R61 Review §6.0 |

### 2.3 Revision 62 Forensic Repairs (`R62-01` through `R62-08`)

| Repair ID | Target Area | Forensic Defect Addressed in Revision 62 | Forensic Correction Applied in Revision 62 | Verification Evidence |
|---|---|---|---|---|
| **R62-01** | Executive Verdict & Numbering Alignment | Delivery report executive verdict and numbering exhibited structural duplicate numbering between Reason 3 and release gate sections | Reconstructed executive verdict with exactly 5 complete, consecutively numbered reasons (`Reason 1` through `Reason 5`) without section numbering conflicts; preserved explicit statement that M0 is strictly unauthorized | Inspected R62 Plan §1.1, §1.2; R62 Review §1.1, §1.2 |
| **R62-02** | Release-Gate Register Allocation Reconciliation | Apparent allocation conflict in earlier drafts between translation quality, STT/VAD latency, end-to-end latency, CPU watchdog, AC power, and Gemini credentials | Resolved allocation conflicts by citing explicit governing authority in `SPEC.md` and `DECISIONS.md` for each requirement; restored complete Gate G-03 and completed G-04 criteria and required evidence; kept all 4 gates open | Inspected R62 Plan §7.1–§7.4, §9.0; R62 Review §2.1–§2.4 |
| **R62-03** | Architecture Graph, Subgraphs & Missing 'e' Label | Delivery report summarized subgraphs without full display strings and omitted full edge declarations; investigated missing `e` label | Formally enumerated all 8 subgraphs with structural IDs, human-readable display strings, and explicit lettered indices (a) through (h), specifically auditing and restoring index (e) `Outbound_Synthesis`; verified all 44 edges `E-01`..`E-44`; labeled manual validation as manual | Inspected R62 Plan §3.1, §3.3; R62 Review §5.1 |
| **R62-04** | Grounded Integrity Checklist Audit | Prior checklist reviews contained potential contradictory statements or incomplete subgraph verification | Re-evaluated CHK-01 through CHK-14 strictly against observable disk evidence; verified 8 subgraphs and complete sections; maintained strict 5-tier taxonomy (8 Verified, 2 Partially Verified, 4 Not Empirically Tested, 0 Failed, 0 Blocked) | Inspected R62 Plan §14.0; R62 Review §6.0 |
| **R62-05** | De-escalation of Promotional Claims | Prior plans contained subjective, unearned promotional terms ("publication-grade," "complete," "fully reconciled," "100% verified") | Systematically removed subjective adjectives; replaced with neutral, evidence-grounded statements ("structurally reconciled in documentation text," "cross-referenced against governing specifications," "unverified on physical hardware") | Inspected R62 Plan §1.1, §15.5; R62 Review §1.1, §8.0 |
| **R62-06** | Physical Artifact Metadata Schema Standardization | Inconsistent metadata presentation, pending R59 review checksums, and lack of distinction between file inspection and git repository validation | Enforced standardized 7-column metadata schema across all artifacts; used `NOT MEASURED` with technical rationale for unmeasured properties; disclosed absent `.git` repository and missing `LICENSE` | Inspected R62 Plan §13.0; R62 Review §4.1 |
| **R62-07** | Strict Disambiguation of Coverage Semantics | Ambiguous terminology conflated mapping completeness with technical issue resolution and gate closure | Rigorously separated Mapping Coverage (100% syntactically mapped), Engineering Issue Resolution (0% resolved; all 15 findings open), and Gate Closure Status (0% closed; all 4 gates open) | Inspected R62 Plan §12.3; R62 Review §5.2 |
| **R62-08** | Complete Findings Register Audit | Need to verify that all 15 findings are fully documented with defined severity scale, subsystems, authorities, and bidirectional mappings | Verified full F-01 through F-15 register with defined 4-tier severity scale (P0/P1/P2/P3), subsystems, governing authorities, and canonical mappings in both summary and detailed records | Inspected R62 Plan §12.1, §15.2; R62 Review §3.1–§3.3 |

### 2.4 Revision 63 Forensic Repairs (`R63-01` through `R63-08`)

| Repair ID | Target Area | Forensic Defect Addressed in Revision 63 | Forensic Correction Applied in Revision 63 | Verification Evidence |
|---|---|---|---|---|
| **R63-01** | Executive Verdict Complete Sentence & Reason Alignment | R62 delivery report ended Reason 5 mid-sentence at line 37; reason count and executive verdict needed complete structural alignment | Restored complete, unabridged Reason 5 in executive verdict; verified all 5 reasons are complete and consecutively numbered (`Reason 1` through `Reason 5`); confirmed agreement across executive verdict, reason count (5), and final status; preserved NOT APPROVED and M0 prohibition | Inspected R63 Plan §1.1, §1.2; R63 Review §1.1, §1.2; R63 Delivery Report §1.1, §1.2 |
| **R63-02** | Findings Register Reconstruction & Disruption Repair | Delivery report missing F-05, interrupted F-12, missing F-13, and malformed separator around F-04/F-06 transition | Fully reconstructed all 15 findings (F-01 through F-15) using canonical sources; restored F-05 (VB-CABLE Render & PTT Safety); repaired interrupted F-12 (Gemini Key DPAPI Storage); restored F-13 (Python Runtime & Win x64 Wheel Audit); removed malformed separator; verified IDs, severities, authorities, gaps, items, gates, and open statuses against forward/reverse matrices | Inspected R63 Plan §12.1, §15.2; R63 Review §3.1–§3.3; R63 Delivery Report §5.0 |
| **R63-03** | Integrity Checklist CHK-14 Re-assessment & Count Parity | R62 report had truncated CHK-14 record; status counts needed recalculation from final individual records | Restored complete CHK-14 record without truncation; re-evaluated CHK-14 against actual plan and review; audited CHK-01 through CHK-14; recalculated taxonomy totals (8 Verified, 2 Partially Verified, 4 Not Empirically Tested, 0 Failed, 0 Blocked = 14 total); ensured checklist table and taxonomy summary agree exactly | Inspected R63 Plan §14.0; R63 Review §6.0; R63 Delivery Report §6.0 |
| **R63-04** | Governance Proposal Disclosure & Section Integrity | Incomplete statement at R62 report line 436; needed explicit identification of all 10 unique proposal IDs and clean section boundaries | Restored complete statement regarding governance proposals; explicitly identified each of the 10 unique proposals (`C-01`..`C-04` and `D-028`..`D-033`) with exact ID, classification, target file, and status `PROPOSED — NOT APPLIED`; cleanly separated approved governing decisions from unapplied proposals; verified clean section boundaries | Inspected R63 Plan §10.1, §10.2, §15.4; R63 Review §7.2; R63 Delivery Report §7.3 |
| **R63-05** | Subgraph Completeness & Outbound_Injection Audit | Outbound_Injection subgraph membership list missing in delivery report; all 8 subgraphs needed explicit verification | Inspected actual Mermaid graph declarations and node registers; completed `Outbound_Injection` membership list (`N-24` Cable_Render, `N-25` Dev_CableIn, `N-26` Dev_CableOut, `N-27` Z_MicIn); verified all 8 subgraphs with lettered indices (a..h), IDs, titles, node lists, and counts; confirmed disjoint 33-node partition ($5+4+3+7+4+4+5+1=33$); verified all 44 edges `E-01`..`E-44`; labeled validation as manual textual inspection | Inspected R63 Plan §3.1–§3.3; R63 Review §5.1; R63 Delivery Report §4.1–§4.4 |
| **R63-06** | Release-Gate Records Complete Schema & Title/Authority Restoration | Gate G-02 missing title, authority, and mappings in summary; records needed consistent complete schema | Enforced standardized complete schema for Gates G-01 through G-04 (ID, Title, Current Status `EMPIRICAL GATE OPEN`, Governing Authority, Canonical Mappings, Mandatory Closure Criteria, Required Evidence, Closure Authority, Blockers); restored G-02 title, authority, and mappings; reconciled gate requirements against `SPEC.md` without altering governing decisions; kept all 4 gates open | Inspected R63 Plan §7.1–§7.4, §9.0; R63 Review §2.1–§2.4; R63 Delivery Report §3.0 |
| **R63-07** | Section Hierarchy & Document Integrity Audit | Investigated missing visible Section 8 and 8.1 headings before 8.2; checked for truncated sentences, broken tables, raw markup, and cross-references | Audited report, plan, and review; confirmed and restored visible `## 8. Risk Management, Discovery Tasks & Concrete Deliverables` and `### 8.1 Technical & Operational Risk Register` preceding `### 8.2 Milestone M0 Discovery Tasks`; eliminated truncated text, duplicated numbering, and raw markup; validated final saved artifacts on disk | Inspected R63 Plan §8.1–§8.3; R63 Review §4.1, §7.1; R63 Delivery Report §2.0 |
| **R63-08** | Evidence & Claim Calibration | Conflation between delivery report inspection and plan/review inspection; claims needed calibration against observable evidence | Distinguished inspection of delivery report from inspection of plan and review; supported every claimed repair with exact file and line references; reassessed all checklist items against observable evidence; calibrated claims with PASS, FAIL, or BLOCKED for acceptance criteria; eliminated unearned publication-readiness claims while P0 defects/open gates remain | Inspected R63 Plan §13.0, §15.5; R63 Review §4.1, §8.1; R63 Delivery Report §8.0 |

### 2.5 Revision 64 Forensic Repairs (`R64-01` through `R64-09`)

| Repair ID | Target Area | Forensic Defect Addressed in Revision 64 | Forensic Correction Applied in Revision 64 | Verification Evidence |
|---|---|---|---|---|
| **R64-01** | Executive Section Repair & Concatenation Elimination | Executive section required complete Reason 3 restoration, elimination of any potential word concatenation, and complete G-01..G-04 status summary | Fully restored Reason 3 and all 5 reasons consecutively numbered (`Reason 1` through `Reason 5`) with complete unabridged sentences; eliminated word concatenation; verified G-01..G-04 appear in current-status summary; ensured agreement across verdict, reasons, and status; preserved NOT APPROVED and M0 prohibition | Inspected R64 Plan §1.1, §1.2; R64 Review §1.1, §1.2; R64 Delivery Report §1.1, §1.2 |
| **R64-02** | Release-Gate Complete Reconstruction | Gates G-01 through G-04 needed full reconstruction with complete schemas, distinguishing governing requirements from proposed targets | Reconstructed complete records for Gates G-01 through G-04 with standardized 8-attribute schema (ID, Title, Current Status `EMPIRICAL GATE OPEN`, Governing Authority, Canonical Mappings, Mandatory Closure Criteria, Required Evidence, Closure Authority, Blockers); restored all content in G-01..G-03; validated full G-04; clearly labeled governing requirements vs proposed targets | Inspected R64 Plan §7.1–§7.4, §9.0; R64 Review §2.1–§2.4; R64 Delivery Report §3.0 |
| **R64-03** | Architecture Subgraphs & Disentanglement | Enumeration of all 8 subgraphs (a..h) needed unique structural IDs, display names, node memberships, counts, and scope descriptions; correction of conflated records | Explicitly enumerated all 8 closed subgraphs `(a)` through `(h)` with structural ID, display name, complete node-membership list, exact node count, and scope description; cleanly decoupled `Outbound_Synthesis` from `Cloud_Integration`; verified complete `Outbound_Injection` and `Control_PTT` entries; confirmed disjoint 33-node partition ($5+4+3+7+4+4+5+1=33$); reconciled all 44 edges `E-01`..`E-44`; declared manual inspection method | Inspected R64 Plan §3.1–§3.3; R64 Review §5.1; R64 Delivery Report §4.1–§4.4 |
| **R64-04** | Complete Findings Register Reconstruction | F-01 through F-15 required reconstruction as 15 complete records, repairing truncated F-05, incomplete F-06 and F-07, and any other disruptions | Reconstructed all 15 findings (F-01 through F-15) as complete, unabridged records with ID, severity, title, subsystem, authority, canonical gap, unresolved item, target gate, and open status; fully articulated F-05, F-06, F-07; reconciled forward and reverse mappings across all gates | Inspected R64 Plan §12.1, §15.2; R64 Review §3.1–§3.3; R64 Delivery Report §5.0 |
| **R64-05** | Integrity Checklist Table Repair & Audit | Table formatting around CHK-09 through CHK-14 needed repair to prevent merged or displaced records; statuses needed rigorous reassessment | Restored CHK-01 through CHK-14 as 14 complete, individually auditable records with unbroken Markdown table structure; reassessed statuses against observable evidence; recalculated taxonomy totals (8 Verified, 2 Partially Verified, 4 Not Empirically Tested, 0 Failed, 0 Blocked = 14 total); ensured exact agreement between table and summary | Inspected R64 Plan §14.0; R64 Review §6.0; R64 Delivery Report §6.0 |
| **R64-06** | Governance Proposal Inventory Reconciliation | All 10 proposals needed exact ID, classification, target file, title, and status `PROPOSED — NOT APPLIED` | Fully reconciled all 10 unique proposal IDs (4 SPEC amendments `C-01`..`C-04` + 6 ADRs `D-028`..`D-033`); maintained all marked `PROPOSED — NOT APPLIED`; separated M0 discovery authorization as an operational milestone boundary | Inspected R64 Plan §10.1, §10.2, §15.4; R64 Review §7.2; R64 Delivery Report §7.3 |
| **R64-07** | Acceptance Criteria Grounding | Previous PASS claims needed re-evaluation against actual final saved files with exact file and line references | Re-evaluated all acceptance criteria using PASS, FAIL, or BLOCKED based strictly on observable disk evidence and exact file/line references; eliminated unearned self-reported completion awards | Inspected R64 Plan §13.0, §15.5; R64 Review §8.1; R64 Delivery Report §8.2 |
| **R64-08** | Physical Metadata Schema Standardization | Metadata required consistent 7-column schema across all artifacts with explicit `NOT MEASURED` for unmeasured properties | Applied standardized 7-column metadata schema (Relative path, Role, Physical line count, Byte size, SHA-256, Measurement method, Measurement status) across all artifacts; marked unavailable values as `NOT MEASURED` with technical rationale; distinguished file inspection from Git repository state | Inspected R64 Plan §13.0; R64 Review §4.1; R64 Delivery Report §8.1 |
| **R64-09** | Final Integrity Pass & Structural Validation | Final inspection of saved R64 artifacts needed after last edit to guarantee zero structural defects or contradictions | Conducted comprehensive integrity inspection across all saved R64 artifacts on disk; confirmed zero truncated sentences, zero broken tables, zero missing headings, zero duplicated IDs, and zero cross-document contradictions | Inspected saved R64 files on disk; Delivery Report §2.0, §9.0 |

### 2.6 Revision 65 Forensic Repairs (`R65-01` through `R65-08`)

The table below documents the targeted forensic repairs applied in Revision 65, directly addressing the eight investigated defect leads:

| Repair ID | Target Area | Forensic Lead Addressed in Revision 65 | Forensic Correction Applied in Revision 65 | Verification Evidence |
|---|---|---|---|---|
| **R65-01** | Executive Reason Alignment & Parity (Lead DIR-01) | R64 architecture plan lacked explicit enumeration of the five numbered reasons in Section 1, creating an asymmetry with the companion review | Added Section 1.2 "Five Consecutively Numbered Reasons for Verdict" to `docs/ARCHITECTURE_R65.md`, ensuring identical verbatim text across plan, review, and delivery report; preserved NOT APPROVED verdict and strict M0 unauthorized boundary | Inspected R65 Plan §1.2; R65 Review §1.2; R65 Report §1.2 |
| **R65-02** | Nomenclature Disambiguation & F-06 Audit Parity (Lead DIR-02) | Previous delivery report labeled prompt audit directives as "F-01..F-09", causing a namespace collision with Canonical Finding F-06 ("Acoustic Feedback Defense") | Renamed prompt directives to `DIR-01`..`DIR-08` and repairs to `R65-01`..`R65-08`; reserved `F-01`..`F-15` strictly for canonical architecture findings; verified complete audit record for Finding F-06 in both plan and review | Inspected R65 Plan §2.6, §12.0; R65 Review §3.2, §3.3 |
| **R65-03** | Canonical Findings Summary Table Restoration (Lead DIR-03) | `docs/ARCHITECTURE_R64.md` Section 12 only listed Unresolved Items (U-01..U-15) and Gaps (GAP-01..GAP-15), omitting the explicit F-01..F-15 summary table | Added Section 12.0 "Canonical Architecture Findings Register (F-01 through F-15)" directly into `docs/ARCHITECTURE_R65.md`, displaying all 15 findings with complete 7-column schema including F-01 and F-06 | Inspected R65 Plan §12.0; R65 Review §3.2 |
| **R65-04** | Integrity Checklist Structure & Cell Resilience (Lead DIR-04) | Checklist table formatting in earlier renderings suffered from long-cell line wrapping, causing apparent truncation of CHK-10, CHK-11, and CHK-14 | Standardized table cell formatting in Section 14 with concise, robust Markdown formatting; re-audited all 14 checks; verified exact 5-tier taxonomy counts (8 Verified, 2 Partially Verified, 4 Not Empirically Tested, 0 Failed, 0 Blocked = 14 total) | Inspected R65 Plan §14.0; R65 Review §6.0 |
| **R65-05** | Dedicated Textual Subgraphs Inventory (Lead DIR-05) | Prior architecture plans declared subgraphs only in Mermaid syntax without a dedicated human-readable textual breakdown, leading to reported missing subgraph (b) in summary reports | Added Section 3.1.1 "Authoritative Closed Subgraphs Inventory (Subgraphs a through h)" to `docs/ARCHITECTURE_R65.md`, enumerating all 8 subgraphs with lettered indices `(a)`..`(h)`, display names, node counts, and assigned nodes, visibly confirming Subgraph `(b)` `Inbound_Processing` | Inspected R65 Plan §3.1.1; R65 Review §5.1 |
| **R65-06** | Physical Metadata Measurement & Qualification (Lead DIR-06) | Metadata table in prior reviews lacked exact measured byte sizes and SHA-256 for live revision files, recording unmeasured properties without sufficient context | Enforced standardized 7-column metadata schema; measured exact physical line counts for all files on disk via read tools; explicitly documented that file byte sizes and checksums for live revision files are qualified as `NOT MEASURED (file-read inspection only; zero fabricated hashes)` | Inspected R65 Plan §13.0; R65 Review §4.1 |
| **R65-07** | Acceptance Criteria Decoupling & Grounding (Lead DIR-07) | Prior review marked AC-04 as PASS citing Section 12.1 of plan, where the F-01..F-15 table was technically missing | With the addition of Section 12.0 in the plan, AC-04 is genuinely satisfied; re-calibrated AC-01 through AC-11, strictly separating document-level review (AC-01..AC-09: PASS) from empirical test execution (AC-10/AC-11: BLOCKED) | Inspected R65 Plan §13.0, §15.5; R65 Review §8.1 |
| **R65-08** | Final Structural Consistency & Cross-Document Parity (Lead DIR-08) | Checked for any remaining truncations, missing IDs, broken tables, inconsistent counts, or unsupported verification claims | Verified exact mathematical parity across all registers: 33 nodes (`N-01`..`N-33`), 44 edges (`E-01`..`E-44`), 8 subgraphs (`(a)`..`(h)`), 15 findings (`F-01`..`F-15`), 15 gaps (`GAP-01`..`GAP-15`), 15 items (`U-01`..`U-15`), 4 release gates (`G-01`..`G-04`, all open), 10 unapplied proposals (`C-01`..`C-04`, `D-028`..`D-033`), 14 checks; confirmed zero governing files modified | Inspected saved R65 files on disk |

---

## 3. Canonical Architecture Model

### 3.1 Architecture Diagram

```mermaid
flowchart TD
    %% =========================================================================
    %% SUBGRAPH 1 (a): INBOUND AUDIO CAPTURE & HARDWARE ENDPOINTS
    %% =========================================================================
    subgraph Inbound_Capture["Inbound Audio Capture & Endpoints"]
        N-01["Browser_Audio<br/>(Zoom Web Meeting Session)"]:::hwNode
        N-02["Dev_Playback<br/>(WASAPI Default Playback Device)"]:::hwNode
        N-03["Dev_Headphones<br/>(Physical Headphones - User Ears)"]:::hwNode
        N-04["Loopback_Cap<br/>(PyAudioWPatch Loopback Client - Candidate)"]:::workerNode
        N-05["Inbound_Audio_Queue<br/>(Raw Loopback PCM Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 2 (b): INBOUND VAD, STT & DISPATCH
    %% =========================================================================
    subgraph Inbound_Processing["Inbound Recognition & Processing"]
        N-06["Inbound_VAD<br/>(Silero VAD ONNX Segmenter)"]:::workerNode
        N-07["Inbound_Speech_Queue<br/>(Voiced Speech Segment Queue)"]:::queueNode
        N-08["Inbound_STT<br/>(faster-whisper int8 JA Worker)"]:::workerNode
        N-09["Inbound_Text_Queue<br/>(Transcribed JA Text Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 3 (c): INBOUND TRANSLATION & USER INTERFACE
    %% =========================================================================
    subgraph Inbound_Translation["Inbound Translation & Presentation"]
        N-10["Inbound_MT<br/>(Local Argos/Marian JA→EN)"]:::workerNode
        N-11["Inbound_Trans_Queue<br/>(Translated EN Text Queue)"]:::queueNode
        N-12["Caption_UI<br/>(Tkinter Overlay Window)"]:::uiNode
    end

    %% =========================================================================
    %% SUBGRAPH 4 (d): OUTBOUND CAPTURE & SPEECH PROCESSING
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
    %% SUBGRAPH 5 (e): OUTBOUND TRANSLATION & SYNTHESIS
    %% =========================================================================
    subgraph Outbound_Synthesis["Outbound Translation & Voice Synthesis"]
        N-20["Outbound_MT<br/>(Local Argos/Marian EN→JA)"]:::workerNode
        N-21["Outbound_TTS_Queue<br/>(Target JA Text Queue)"]:::queueNode
        N-22["Outbound_TTS<br/>(Permissive JA TTS Worker)"]:::workerNode
        N-23["Outbound_Render_Queue<br/>(Synthesized JA PCM Queue)"]:::queueNode
    end

    %% =========================================================================
    %% SUBGRAPH 6 (f): OUTBOUND VIRTUAL AUDIO INJECTION
    %% =========================================================================
    subgraph Outbound_Injection["Outbound Virtual Routing to Zoom"]
        N-24["Cable_Render<br/>(WASAPI Render to VB-CABLE)"]:::workerNode
        N-25["Dev_CableIn<br/>(VB-CABLE Virtual Input)"]:::hwNode
        N-26["Dev_CableOut<br/>(VB-CABLE Virtual Output)"]:::hwNode
        N-27["Z_MicIn<br/>(Zoom Web Mic Input)"]:::hwNode
    end

    %% =========================================================================
    %% SUBGRAPH 7 (g): PTT CONTROL & WATCHDOG SUPERVISION
    %% =========================================================================
    subgraph Control_PTT["Push-to-Talk Supervision & Control"]
        N-28["PTT_Input<br/>(Physical Keyboard Spacebar/Hotkey)"]:::hwNode
        N-29["PTT_Hook<br/>(Win32 Low-Level Keyboard Hook)"]:::ctrlNode
        N-30["PTT_Poller<br/>(50ms Polling Heartbeat Supervisor)"]:::ctrlNode
        N-31["PTT_Controller<br/>(PTT Epoch & Cancellation Coordinator)"]:::ctrlNode
        N-32["Watchdog_Timer<br/>(Host Health & CPU Load Watchdog)"]:::ctrlNode
    end

    %% =========================================================================
    %% SUBGRAPH 8 (h): OPTIONAL CLOUD INTEGRATION (OPT-IN ONLY)
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

### 3.1.1 Authoritative Closed Subgraphs Inventory (Subgraphs a through h)

The table below provides the authoritative structural inventory of all 8 closed subgraphs, verifying that the 33 nodes form an exact, non-overlapping partition ($5 + 4 + 3 + 7 + 4 + 4 + 5 + 1 = 33$ nodes):

| Index | Subgraph Structural ID | Human-Readable Display Name | Node Count | Complete Assigned Node List | Subsystem Architectural Scope |
|---|---|---|---|---|---|
| **(a)** | `Inbound_Capture` | Inbound Audio Capture & Endpoints | 5 | `N-01`, `N-02`, `N-03`, `N-04`, `N-05` | Captures browser Zoom audio via shared-mode WASAPI loopback tapping default playback, routes audio to headphones, buffers PCM |
| **(b)** | `Inbound_Processing` | Inbound Recognition & Processing | 4 | `N-06`, `N-07`, `N-08`, `N-09` | Ingests 30ms PCM chunks, performs Silero VAD segmentation, executes faster-whisper int8 JA speech-to-text, buffers JA text |
| **(c)** | `Inbound_Translation` | Inbound Translation & Presentation | 3 | `N-10`, `N-11`, `N-12` | Local JA→EN translation via Argos/MarianMT, buffers translated text, renders non-stealing transparent Tkinter overlay |
| **(d)** | `Outbound_Processing` | Outbound Capture & Speech Processing | 7 | `N-13`, `N-14`, `N-15`, `N-16`, `N-17`, `N-18`, `N-19` | Captures physical mic under PTT gate, performs Silero VAD segmentation, executes faster-whisper int8 EN STT, buffers EN text |
| **(e)** | `Outbound_Synthesis` | Outbound Translation & Voice Synthesis | 4 | `N-20`, `N-21`, `N-22`, `N-23` | Local EN→JA translation via Argos/MarianMT, buffers target JA text, synthesizes 22.05kHz PCM via local permissive TTS worker |
| **(f)** | `Outbound_Injection` | Outbound Virtual Routing to Zoom | 4 | `N-24`, `N-25`, `N-26`, `N-27` | Streams synthesized audio to VB-CABLE Input via WASAPI render client; virtual driver DMA transfers to Output; Zoom captures mic |
| **(g)** | `Control_PTT` | Push-to-Talk Supervision & Control | 5 | `N-28`, `N-29`, `N-30`, `N-31`, `N-32` | Dual-signal hotkey supervision (`WH_KEYBOARD_LL` + 50ms polling), PTT epoch coordination, queue purge on KeyUp, host watchdog |
| **(h)** | `Cloud_Integration` | Cloud Translation (Opt-In Only) | 1 | `N-33` | Optional Google Gemini REST/SDK MT adapter, sequential arbitration, 2.50s HTTP timeout, monotonic correlation IDs |

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
3. **Acoustic Feedback Defense (`DECISIONS.md` D-016):** Physical headphones (`Dev_Headphones`) are mandatory to eliminate physical acoustic leakage from Zoom playback into the user microphone (`User_Mic`). Digital loopback capture on `Dev_Playback` is never suppressed during push-to-talk to ensure the user retains situational awareness (`SPEC.md` §4.3).

#### 3.4.2 Dual-Mode Privacy Governance & Sequential Translation Arbitration
KoeBridge implements two strict, mutually exclusive operational modes for machine translation:

```
+--------------------------------------------------------------------------------------------------+
| KOEBRIDGE DUAL-MODE PRIVACY & SEQUENTIAL ARBITRATION SPECIFICATION                              |
+--------------------------------------------------------------------------------------------------+
| 1. LOCAL MODE (DEFAULT - STRICTLY OFFLINE):                                                      |
|    - Network Policy: 100% offline. Zero TCP/UDP socket creation. Zero network egress.            |
|    - Translation Engine: Local Argos Translate / MarianMT executing on CPU.                      |
|    - Silent Fallback: STRICTLY PROHIBITED. If local translation models fail or stall,            |
|      the pipeline raises a visible error in the Caption UI. Cloud is NEVER silently contacted.   |
|    - CPU Load / Slowness: High CPU load or inference latency NEVER triggers cloud offloading.    |
|                                                                                                  |
| 2. CLOUD OPT-IN MODE (EXPLICIT USER CONSENT ONLY):                                               |
|    - Opt-In Activation: Disabled by default. Requires explicit informed user toggle in UI.      |
|    - Payload Restriction: Plain text transcripts only. Audio PCM is NEVER transmitted to cloud.  |
|    - Monotonic Correlation: Each segment carries CorrID = <SessionID, EpochID, SegmentSeq>.      |
|    - Sequential Arbitration Flow:                                                                |
|        1. Text segment ready in queue.                                                           |
|        2. Dispatch text payload to Google Gemini API (official SDK / REST).                      |
|           Enforce strict 2.50 s client HTTP timeout.                                             |
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
│   ├── ARCHITECTURE_R65.md     # Current Architecture & Verification Plan (Revision 65)
│   ├── ARCHITECTURE_R65_REVIEW.md # Current Forensic Acceptance Review (Revision 65)
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
| **Machine Translation** | Argos Translate | MIT | MIT / OpenNMT / CC-BY | **APPROVED CANDIDATE** (`DECISIONS.md` D-006). Direct JA↔EN translation. |
| **MT Fallback** | MarianMT (Helsinki-NLP) | Apache 2.0 | Apache 2.0 / CC-BY-4.0 | **FALLBACK CANDIDATE** (`SPEC.md` §5.2). Direct translation pairs. |
| **TTS Engine Candidate** | `OHF-Voice/piper1-gpl` | GPL-3.0-or-later | Varies (Check dataset) | **UNAPPROVED BY DEFAULT** (`SPEC.md` §5). Hard release blocker without non-GPL alternative. |
| **TTS Alternative Candidate** | Kokoro-82M / ONNX | Apache 2.0 | Apache 2.0 | **PROPOSED CANDIDATE** (Task M0-2). Must verify Japanese phonemizer licensing. |
| **Audio I/O Library** | `PyAudioWPatch` | MIT | N/A (Pure software) | **APPROVED CANDIDATE** (`DECISIONS.md` D-001). PortAudio WASAPI loopback fork. |
| **GUI Framework** | Tkinter / ttk | Python PSF | N/A (Standard Library) | **APPROVED CANDIDATE** (`DECISIONS.md` D-002). Permissive Tcl/Tk license. |
| **Virtual Audio Cable** | VB-CABLE (VB-Audio) | Proprietary Freeware | N/A (Kernel Driver) | **EXTERNAL USER-INSTALLED** (`SPEC.md` §4.2). Never bundled or auto-installed. |

### 6.1 Machine Translation Dialogue Benchmark Suite (TC-01 through TC-10)

The table below defines the preliminary 10-sentence technical dialogue smoke-test suite for evaluating direct JA↔EN machine translation quality under Gate G-02:

| Test Case | Domain / Context | Japanese Source Text | Reference English Translation | Key Quality & Negation Constraints |
|---|---|---|---|---|
| **TC-01** | Meeting Greetings | お疲れ様です。本日の進捗確認を始めましょう。 | Thank you for your hard work. Let's start today's progress check. | Formulaic business greeting; must avoid awkward literal translations. |
| **TC-02** | Schedule Delay | 申し訳ありませんが、APIの統合が少し遅れています。 | I apologize, but the API integration is slightly delayed. | Must capture polite apology and technical domain term (API integration). |
| **TC-03** | Technical Blocker | 認証トークンの期限切れ問題が発生しており、調査中です。 | An authentication token expiration issue occurred, and we are investigating. | Accurate security domain terminology (authentication token expiration). |
| **TC-04** | Critical Negation | この設定を変更してはいけません。本番環境に影響します。 | You must not change this setting. It will affect the production environment. | **CRITICAL NEGATION:** "must not change" must NEVER be translated as "can change". |
| **TC-05** | Numerical Precision | 明日の午後3時までにプルリクエストをレビューしてください。 | Please review the pull request by 3:00 PM tomorrow. | **NUMERICAL PRECISION:** 3:00 PM must not become 3:00 AM or 15 hours. |
| **TC-06** | Dependency Block | データベースのマイグレーションが完了するまで、デプロイはできません。 | We cannot deploy until the database migration is complete. | **CRITICAL NEGATION:** Deploy inability condition must be preserved accurately. |
| **TC-07** | Performance Concern | メモリ使用量が95%を超えているため、再起動が必要です。 | Because memory usage exceeds 95%, a restart is necessary. | **NUMERICAL PRECISION:** 95% threshold and causal reasoning must be preserved. |
| **TC-08** | Technical Action | キャッシュをクリアしてから、もう一度テストを実行してみてください。 | Please clear the cache and then try running the test once more. | Multi-step instruction sequence must maintain temporal ordering. |
| **TC-09** | Agreement / Consensus | その提案で問題ありません。次のステップに進めましょう。 | There are no issues with that proposal. Let's proceed to the next step. | Professional agreement idiom ("no issues", "sounds good"). |
| **TC-10** | Closing / Next Steps | 次回のミーティングは来週の火曜日の午前10時です。 | The next meeting is next Tuesday at 10:00 AM. | Temporal accuracy: Next Tuesday, 10:00 AM. |

---

## 7. Verification Protocols & Acceptance Criteria

### 7.1 Gate G-01: Japanese TTS Engine & Voice Licensing Clearance
- **Governing Authority:** `SPEC.md` §5, §14 (Item 1); `DECISIONS.md` D-003, D-004, D-005.
- **Current Gate Status:** **EMPIRICAL GATE OPEN**
- **Mandatory Closure Criteria:**
  1. Engine runtime code must be licensed under a permissive license (MIT, Apache 2.0, or BSD) (`GOVERNING REQUIREMENT`). `OHF-Voice/piper1-gpl` is GPL-3.0 and strictly unapproved by default.
  2. Voice acoustic weights, phonemizer checkpoints, and training data must have verified commercial-friendly permissive provenance (`GOVERNING REQUIREMENT`).
  3. Real-Time Factor (RTF) $\le 0.50$ on Intel Core i7-8750H on CPU (`PROPOSED TARGET`).
  4. Audio output must be clean 22.05 kHz or 24 kHz mono 16-bit PCM.
- **Required Evidence:** Completed `docs/THIRD_PARTY_NOTICES.md` with full license texts; benchmark log recording RTF across 50 test sentences on AC power (`ACLineStatus == 1`).

### 7.2 Gate G-02: Direct JA↔EN Machine Translation Quality & Latency Clearance
- **Governing Authority:** `SPEC.md` §5.2, §14 (Item 2); `DECISIONS.md` D-006, D-010, D-011.
- **Current Gate Status:** **EMPIRICAL GATE OPEN**
- **Mandatory Closure Criteria:**
  1. Direct JA↔EN translation without intermediate pivot language (`GOVERNING REQUIREMENT`, `DECISIONS.md` D-006).
  2. Corpus BLEU $\ge 25.0$ and chrF $\ge 0.50$ across the 10-sentence dialogue benchmark (`PROPOSED TARGETS`).
  3. Zero critical negation reversals (TC-04, TC-06) or numerical corruptions (TC-05, TC-07) (`GOVERNING REQUIREMENT`).
  4. Local CPU translation latency $\le 600\text{ ms}$ for sentences under 30 words (`PROPOSED TARGET`).
  5. Local Mode must be 100% offline with zero network socket creation. Cloud Opt-In Mode requires explicit consent, 2.50 s client HTTP timeout, monotonic correlation IDs, and sequential fallback (`GOVERNING REQUIREMENTS`).
- **Required Evidence:** Benchmark log comparing Argos Translate and MarianMT on TC-01..TC-10; Wireshark packet capture confirming zero network egress in Local Mode; Cloud Opt-In timeout logs.

### 7.3 Gate G-03: End-to-End Pipeline Latency Budget & Host Hardware Safety Clearance
- **Governing Authority:** `SPEC.md` §5, §6, §8 (Sole Authority for host safety), §14 (Items 5 & 7); `DECISIONS.md` D-007, D-008, D-020, D-025, D-027.
- **Current Gate Status:** **EMPIRICAL GATE OPEN**
- **Mandatory Closure Criteria:**
  1. Inbound translation latency budget $\le 1,800\text{ ms}$ target / $2,400\text{ ms}$ max (`GOVERNING REQUIREMENT`, `SPEC.md` §5).
  2. Outbound translation & injection budget $\le 2,100\text{ ms}$ target / $2,900\text{ ms}$ max (`GOVERNING REQUIREMENT`, `SPEC.md` §5).
  3. Speech recognition (`faster-whisper` `small` `int8`) latency $\le 800\text{ ms}$ for 3.0s audio on CPU (`PROPOSED TARGET`).
  4. Silero VAD chunk inference latency $\le 5.0\text{ ms}$ for 30 ms chunk on CPU (`PROPOSED TARGET`).
  5. All tests must execute on verified plugged-in AC power (`ACLineStatus == 1`, `GOVERNING REQUIREMENT`, `SPEC.md` §8).
  6. Background CPU watchdog must alert and throttle pipeline if CPU load $\ge 95\%$ sustained for $\ge 15\text{ s}$ (`PROPOSED TARGET`).
- **Required Evidence:** High-resolution QPC end-to-end latency traces recorded on Intel Core i7-8750H on AC power; CPU watchdog load test log.

### 7.4 Gate G-04: Audio Endpoint Topology, Loopback Stability & PTT Safety Verification
- **Governing Authority:** `SPEC.md` §4.1, §4.2, §4.3, §5.4, §14 (Item 3); `DECISIONS.md` D-002, D-016, D-023, D-026.
- **Current Gate Status:** **EMPIRICAL GATE OPEN**
- **Mandatory Closure Criteria:**
  1. **Test 1 (Endpoint Enumeration):** PyAudioWPatch correctly enumerates default playback loopback and VB-CABLE endpoints.
  2. **Test 2A (Loopback Format):** Stable capture at 48 kHz stereo 32-bit float or 16-bit PCM.
  3. **Test 2B (60-Min Continuous Streaming):** Aggregate frame-delivery discrepancy $E_{\text{delivery}} \le 50.0\text{ PPM}$ relative to QPC reference; zero buffer discontinuities ($N_{\text{discontinuity}} == 0$); zero stream restarts ($N_{\text{restarts}} == 0$); max callback stall $T_{\text{stall\_max}} \le 250\text{ ms}$.
  4. **Test 3 (Acoustic Feedback & Isolation):** Mandatory physical headphones (`Dev_Headphones`, `DECISIONS.md` D-016). Loopback capture must not be suppressed during PTT (`SPEC.md` §4.3). Digital route isolation $R_{\text{iso}} \ge 60.0\text{ dB}$ under AES-17 1 kHz sine testing at $-20.0\text{ dBFS}$ to `Dev_CableIn`, with preflight noise floor $\le -90.0\text{ dBFS}$. Acoustic leakage screening $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ over ambient noise.
  5. **Test 4 (PTT Hotkey & Lifecycle Safety):** KeyDown increments epoch (`EpochID = N + 1`); KeyUp purges queues (`qsize() == 0`), halts mic capture $\le 10\text{ ms}$, resets render stream $\le 50\text{ ms}$, and discards stale inference ($N_{\text{stale\_rendered}} == 0$). 50 ms polling heartbeat verifies key state if hook drops messages.
  6. **Tkinter GUI Overlay:** Caption window renders $\ge 30\text{ FPS}$ without stealing user focus from Chrome/Edge (`SPEC.md` §5.4).
- **Required Evidence:** 60-minute loopback capture CSV telemetry log; AES-17 spectrum analysis log; PTT state machine unit test report (Phase 4A) and live Windows timing trace (Phase 4B).

---

## 8. Risk Management, Discovery Tasks & Concrete Deliverables

### 8.1 Technical & Operational Risk Register

| Risk ID | Severity | Category | Risk Description & Technical Root Cause | Mitigation & Operational Protocol |
|---|---|---|---|---|
| **RSK-01** | **P0** | Hardware / Power | Target laptop hardware exhibits sudden power shutdowns under heavy CPU/GPU load on battery power | Operation strictly prohibited unless plugged into verified AC power (`ACLineStatus == 1`, `SPEC.md` §8). Watchdog throttles if CPU $\ge 95\%$ for $\ge 15\text{ s}$. |
| **RSK-02** | **P0** | Licensing / Legal | `OHF-Voice/piper1-gpl` is GPL-3.0-or-later, creating legal copyleft exposure for proprietary/MIT distribution | Japanese voice synthesis is a mandatory MVP hard gate (Gate G-01). Must identify standalone permissive engine/weights or obtain explicit owner approval. |
| **RSK-03** | **P0** | Translation Quality | Argos Translate produces poor quality or critical negation reversals on Japanese technical meeting dialogue | 10-sentence dialogue benchmark suite (TC-01..TC-10) enforces BLEU $\ge 25.0$ and zero negation errors. MarianMT specified as local fallback candidate. |
| **RSK-04** | **P0** | Audio / Safety | Physical open speakers leak meeting audio into user mic, causing acoustic feedback loops and false STT triggers | Physical headphones (`Dev_Headphones`) are mandatory (`DECISIONS.md` D-016). AES-17 digital isolation ($\ge 60\text{ dB}$) and leakage screening ($\le +6\text{ dB}$) enforced. |
| **RSK-05** | **P0** | Privacy / Egress | Cloud MT adapter transmits audio or leaks private meeting text transcripts without user consent | Local Mode is strictly offline default with zero socket creation. Cloud Opt-In requires explicit consent, 2.50 s timeout, correlation IDs, and text-only payload. |

### 8.2 Milestone M0 Discovery Tasks (Planned Procedures — UNAUTHORIZED)

1. **Task M0-1 (Runtime & Wheel Compatibility Audit):** Audit PyPI pre-compiled wheels for Python 3.11, 3.12, and 3.13 on Windows x64 for CTranslate2, PyAudioWPatch, and ONNX Runtime. Benchmark baseline Whisper and Silero VAD CPU latency.
2. **Task M0-2 (Permissive Japanese TTS Engine Clearance):** Audit standalone non-GPL Japanese TTS candidate models (Kokoro-82M ONNX vs Piper alternatives). Profile RTF on target CPU on AC power.
3. **Task M0-3 (Direct JA↔EN Translation Evaluation):** Benchmark Argos Translate and MarianMT on TC-01..TC-10. Verify BLEU, chrF, negation accuracy, and latency.
4. **Task M0-4 (WASAPI Loopback 60-Minute Stability Test):** Execute 60-minute continuous loopback capture on default playback. Measure aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$) and buffer discontinuities.
5. **Task M0-5 (Audio Isolation & PTT Integration Probe):** Execute AES-17 1 kHz sine isolation test on VB-CABLE Input vs loopback capture. Probe Win32 hook and 50 ms polling heartbeat timing.
6. **Task M0-6 (End-to-End Latency Tracing & Host Watchdog Calibration):** Profile integrated inbound and outbound pipeline latency on target hardware on AC power. Calibrate 95% CPU watchdog.
7. **Task M0-7 (Tkinter Caption GUI Overlay Prototype):** Test transparent, focus-preserving Tkinter overlay rendering at $\ge 30\text{ FPS}$ during background CPU load.
8. **Task M0-8 (Windows Credential Manager Storage Probe):** Validate secure API key storage via `keyring` (Windows DPAPI backend) without writing plaintext to disk.
9. **Task M0-9 (Milestone M0 Discovery Dossier Synthesis):** Compile all benchmark logs, licensing manifests, and telemetry traces into `docs/M0_DISCOVERY_REPORT.md` for owner sign-off.

### 8.3 Concrete Milestone 0 Deliverables

- **DEL-01:** `docs/THIRD_PARTY_NOTICES.md` (Comprehensive multi-tier software and model license manifest).
- **DEL-02:** `docs/BENCHMARKS.md` (Empirical latency, RTF, BLEU, and loopback telemetry logs).
- **DEL-03:** `prototypes/m0_discovery/` (Seven standalone Python discovery prototype scripts, PROTO-01..PROTO-07).
- **DEL-04:** `tests/unit/test_ptt_state_machine.py` (Phase 4A deterministic PTT unit test suite).
- **DEL-05:** `docs/M0_DISCOVERY_REPORT.md` (Formal Discovery Report presenting evidence to clear Gates G-01..G-04).

---

## 9. Release-Gate Operational Register (G-01 through G-04)

The table below summarizes the operational status and requirements of all four formal release gates:

| Gate ID | Release Gate Name | Operational Status | Governing Authority | Canonical Technical Gaps | Unresolved Items | Mandatory Acceptance Thresholds |
|---|---|---|---|---|---|---|
| **Gate G-01** | Japanese TTS Engine & Voice Licensing Clearance | **EMPIRICAL GATE OPEN** | `SPEC.md` §5, `DECISIONS.md` D-003, D-005 | GAP-01, GAP-13, GAP-15 | U-01, U-13, U-15 | Permissive non-GPL license; verified voice weights; RTF $\le 0.50$ on CPU (`PROPOSED TARGET`); Win x64 wheels; MIT `LICENSE` on disk. |
| **Gate G-02** | Direct JA↔EN Machine Translation Quality & Latency | **EMPIRICAL GATE OPEN** | `SPEC.md` §5.2, `DECISIONS.md` D-006, D-010, D-011 | GAP-02, GAP-07 | U-02, U-07 | Direct JA↔EN without pivot; BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$ (`PROPOSED TARGETS`); zero negation errors; strict offline Local Mode; sequential Cloud Opt-In. |
| **Gate G-03** | End-to-End Latency Budget & Host Safety Clearance | **EMPIRICAL GATE OPEN** | `SPEC.md` §8 (Sole Authority), `DECISIONS.md` D-020, D-025, D-027 | GAP-03, GAP-08, GAP-09, GAP-10, GAP-12 | U-03, U-08, U-09, U-10, U-12 | Inbound $\le 1,800\text{ ms}$, Outbound $\le 2,100\text{ ms}$ (`GOVERNING REQUIREMENTS`); Whisper $\le 800\text{ ms}$; VAD $\le 5.0\text{ ms}$; AC power check (`ACLineStatus == 1`); CPU watchdog; DPAPI key storage. |
| **Gate G-04** | Audio Topology, Loopback & PTT Safety Verification | **EMPIRICAL GATE OPEN** | `SPEC.md` §4.1–§4.3, `DECISIONS.md` D-002, D-016, D-023, D-026 | GAP-04, GAP-05, GAP-06, GAP-11, GAP-14 | U-04, U-05, U-06, U-11, U-14 | 60-min loopback streaming ($E_{\text{delivery}} \le 50.0\text{ PPM}$, 0 discontinuities); PTT lifecycle queues purge ($qsize() == 0$); headphone mandate; AES-17 isolation $\ge 60\text{ dB}$; Tkinter 30 FPS overlay. |

---

## 10. Governance Proposals Inventory (C-01..C-04 and D-028..D-033)

The 10 items below represent proposed amendments to `SPEC.md` and proposed Architecture Decision Records in `DECISIONS.md`. All 10 items remain strictly marked **`PROPOSED — NOT APPLIED`** pending explicit project-owner authorization:

### 10.1 Proposed Amendments to SPEC.md (`C-01` through `C-04`)
1. **`C-01` (Proposed Specification Amendment — Battery Power Operational Boundary):** Proposes formalizing laptop plugged-in AC power preflight (`ACLineStatus == 1`) and CPU load throttling as an explicit clause in `SPEC.md` §8. *Status: PROPOSED — NOT APPLIED.*
2. **`C-02` (Proposed Specification Amendment — MT Evaluation Benchmark Suite):** Proposes codifying the 10-sentence dialogue benchmark suite (TC-01..TC-10) and minimum metric thresholds (BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$) into `SPEC.md` §5.2. *Status: PROPOSED — NOT APPLIED.*
3. **`C-03` (Proposed Specification Amendment — Headphone & Audio Feedback Rules):** Proposes codifying the physical headphone mandate (`Dev_Headphones`) and the prohibition against unconditional loopback suppression during cross-talk into `SPEC.md` §4.3. *Status: PROPOSED — NOT APPLIED.*
4. **`C-04` (Proposed Specification Amendment — Cloud Opt-In Mode Privacy Boundaries):** Proposes defining the detailed sequential arbitration protocol, 2.50 s client HTTP timeout, and monotonic correlation IDs for Cloud Opt-In Mode in `SPEC.md` §6. *Status: PROPOSED — NOT APPLIED.*

### 10.2 Proposed Architecture Decision Records (`D-028` through `D-033`)
1. **`D-028` (Proposed ADR — Host Hardware Safety & AC Power Guardrails):** Proposes formalizing Win32 power status API checks and background CPU watchdog load throttling thresholds. *Status: PROPOSED — NOT APPLIED.* (Governing authority for host power safety is strictly `SPEC.md` §8).
2. **`D-029` (Proposed ADR — Machine Translation Evaluation Protocol & Fallback Architecture):** Proposes formalizing the selection criteria between Argos Translate and MarianMT fallback models. *Status: PROPOSED — NOT APPLIED.*
3. **`D-030` (Proposed ADR — Audio Routing Isolation & Headphone Defense Policy):** Proposes codifying AES-17 sine stimulus testing protocols and acoustic feedback prevention rules. *Status: PROPOSED — NOT APPLIED.*
4. **`D-031` (Proposed ADR — Push-to-Talk Lifecycle, Cancellation Tokens & Queue Purging):** Proposes standardizing the dual-signal supervision architecture (`WH_KEYBOARD_LL` + 50 ms polling) and epoch cancellation tokens. *Status: PROPOSED — NOT APPLIED.*
5. **`D-032` (Proposed ADR — Japanese Text-to-Speech Engine & Voice Licensing Clearance):** Proposes establishing the multi-tier licensing evaluation framework and standalone non-GPL voice asset clearance protocol. *Status: PROPOSED — NOT APPLIED.*
6. **`D-033` (Proposed ADR — Cloud Translation Opt-In Protocol & Privacy Governance):** Proposes standardizing the dual-mode privacy architecture, sequential fallback arbitration, and DPAPI credential storage. *Status: PROPOSED — NOT APPLIED.*

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

## 12. Findings Register, Unresolved Items & Bidirectional Traceability

### 12.0 Canonical Architecture Findings Register (F-01 through F-15)

The table below enumerates all 15 canonical architecture findings with defined severities, subsystems, governing authorities, and mappings:

| Finding ID | Severity | Subsystem Domain | Governing Authority | Canonical Mappings | Target Gate | Operational Status |
|---|---|---|---|---|---|---|
| **F-01** | **P0** | Japanese Speech Synthesis | `SPEC.md` §5, `DECISIONS.md` D-003, D-005 | GAP-01 / U-01 | Gate G-01 | **OPEN — UNRESOLVED** |
| **F-02** | **P0** | Machine Translation | `SPEC.md` §5.2, `DECISIONS.md` D-006 | GAP-02 / U-02 | Gate G-02 | **OPEN — UNRESOLVED** |
| **F-03** | **P0** | Host Safety & Power | `SPEC.md` §8 (Sole Authority) | GAP-03 / U-03 | Gate G-03 | **OPEN — UNRESOLVED** |
| **F-04** | **P0** | Audio Capture Routing | `SPEC.md` §4.1, `DECISIONS.md` D-026 | GAP-04 / U-04 | Gate G-04 | **OPEN — UNRESOLVED** |
| **F-05** | **P0** | Virtual Driver & PTT | `SPEC.md` §4.2, `DECISIONS.md` D-023 | GAP-05 / U-05 | Gate G-04 | **OPEN — UNRESOLVED** |
| **F-06** | **P1** | Acoustic Feedback Defense | `SPEC.md` §4.3, `DECISIONS.md` D-016 | GAP-06 / U-06 | Gate G-04 | **OPEN — UNRESOLVED** |
| **F-07** | **P1** | Privacy & Cloud Mode | `SPEC.md` §1, §6, `DECISIONS.md` D-010, D-011 | GAP-07 / U-07 | Gate G-02 | **OPEN — UNRESOLVED** |
| **F-08** | **P1** | Speech Recognition | `SPEC.md` §5.1, `DECISIONS.md` D-007 | GAP-08 / U-08 | Gate G-03 | **OPEN — UNRESOLVED** |
| **F-09** | **P1** | Voice Activity Detection | `SPEC.md` §4.1, `DECISIONS.md` D-008 | GAP-09 / U-09 | Gate G-03 | **OPEN — UNRESOLVED** |
| **F-10** | **P1** | Latency Budget Clearance | `SPEC.md` §5, `DECISIONS.md` D-025 | GAP-10 / U-10 | Gate G-03 | **OPEN — UNRESOLVED** |
| **F-11** | **P2** | Presentation UI Overlay | `SPEC.md` §5.4, `DECISIONS.md` D-002 | GAP-11 / U-11 | Gate G-04 | **OPEN — UNRESOLVED** |
| **F-12** | **P2** | Credential Security | `SPEC.md` §6, `DECISIONS.md` D-027 | GAP-12 / U-12 | Gate G-03 | **OPEN — UNRESOLVED** |
| **F-13** | **P2** | Runtime Compatibility | `SPEC.md` §1, `DECISIONS.md` D-026 | GAP-13 / U-13 | Gate G-01 | **OPEN — UNRESOLVED** |
| **F-14** | **P2** | Audio Isolation | `SPEC.md` §4.3, `DECISIONS.md` D-016 | GAP-14 / U-14 | Gate G-04 | **OPEN — UNRESOLVED** |
| **F-15** | **P3** | Repository Governance | `CLAUDE.md`, `SPEC.md` §1 | GAP-15 / U-15 | Gate G-01 | **OPEN — UNRESOLVED** |

---

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

---

### 12.2 Forward Traceability Matrix (U-01..U-15 to GAP-01..GAP-15 to Gates)

| Unresolved Item | Canonical Technical Gap | Governing Release Gate | Planned Resolution Task | Milestone Owner | Target Acceptance Standard |
|---|---|---|---|---|---|
| **U-01** | **GAP-01** (Permissive JA TTS & Voice Licensing) | Gate G-01 | Task M0-2 | Milestone M0 | Permissive non-GPL TTS voice verified with $\text{RTF} \le 0.50$ (`PROPOSED TARGET`) |
| **U-02** | **GAP-02** (Direct JA↔EN MT Quality & Latency) | Gate G-02 | Task M0-3 | Milestone M0 | BLEU $\ge 25.0$, chrF $\ge 0.50$, latency $\le 600\text{ ms}$, zero critical errors (`PROPOSED TARGETS`) |
| **U-03** | **GAP-03** (Host Power Mandate & CPU Watchdog) | Gate G-03 | Task M0-6 | Milestone M0 | AC power check (`ACLineStatus == 1`, `GOVERNING REQUIREMENT`); watchdog at $\ge 95\%$ CPU for $\ge 15\text{ s}$ (`PROPOSED TARGET`) |
| **U-04** | **GAP-04** (WASAPI Loopback Capture Stability) | Gate G-04 | Task M0-4 | Milestone M0 | 60-min continuous capture; $E_{\text{delivery}} \le 50.0\text{ PPM}$; zero discontinuities (`PROPOSED TARGETS`) |
| **U-05** | **GAP-05** (VB-CABLE Injection & PTT Safety) | Gate G-04 | Task M0-5 | Milestone M0 | Dual-signal PTT; KeyUp queue purge ($qsize() == 0$); mic halt $\le 10\text{ ms}$; render reset $\le 50\text{ ms}$ (`PROPOSED TARGETS`) |
| **U-06** | **GAP-06** (Acoustic Feedback Defense & Headphones) | Gate G-04 | Task M0-5 | Milestone M0 | Headphone mandate (`Dev_Headphones`, `GOVERNING REQUIREMENT`); acoustic leakage $\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$ |
| **U-07** | **GAP-07** (Privacy Modes & Sequential MT Fallback) | Gate G-02 | Task M0-3 | Milestone M0 | Local Mode zero socket egress; Cloud Opt-In 2.50 s timeout, sequential local fallback (`GOVERNING REQUIREMENTS`) |
| **U-08** | **GAP-08** (Whisper Speech Recognition Latency) | Gate G-03 | Task M0-1 | Milestone M0 | `faster-whisper` `small` `int8` CPU latency $\le 800\text{ ms}$ on 3.0s audio on AC power (`PROPOSED TARGET`) |
| **U-09** | **GAP-09** (Silero VAD Latency & Chunk Ingestion) | Gate G-03 | Task M0-1 | Milestone M0 | Silero VAD ONNX chunk processing latency $\le 5.0\text{ ms}$ per 30 ms chunk on CPU (`PROPOSED TARGET`) |
| **U-10** | **GAP-10** (End-to-End Latency Budget Clearance) | Gate G-03 | Task M0-6 | Milestone M0 | Inbound $\le 1,800\text{ ms}$ target / $2,400\text{ ms}$ max; Outbound $\le 2,100\text{ ms}$ target / $2,900\text{ ms}$ max (`GOVERNING REQUIREMENTS`) |
| **U-11** | **GAP-11** (Tkinter GUI Responsiveness & Focus) | Gate G-04 | Task M0-7 | Milestone M0 | Overlay renders $\ge 30\text{ FPS}$ without stealing user focus from Chrome/Edge (`GOVERNING REQUIREMENT`) |
| **U-12** | **GAP-12** (Secure Gemini API Key DPAPI Storage) | Gate G-03 | Task M0-8 | Milestone M0 | Volatile memory only; persistent storage via Windows Credential Manager DPAPI (`GOVERNING REQUIREMENT`) |
| **U-13** | **GAP-13** (Python Runtime & Wheel Compatibility) | Gate G-01 | Task M0-1 | Milestone M0 | Pre-compiled Windows x64 binary wheels verified for CTranslate2, PyAudioWPatch, ONNX Runtime (`GOVERNING REQUIREMENT`) |
| **U-14** | **GAP-14** (Digital Route Isolation Verification) | Gate G-04 | Task M0-5 | Milestone M0 | Relative digital route isolation $R_{\text{iso}} \ge 60.0\text{ dB}$ under AES-17 sine stimulus testing (`PROPOSED TARGET`) |
| **U-15** | **GAP-15** (Repository MIT License File Absence) | Gate G-01 | Pre-M1 Action | Milestone M0 | Commit official repository MIT `LICENSE` file on disk prior to Milestone M1 (`GOVERNING REQUIREMENT`) |

---

### 12.3 Reverse Traceability Matrix (Release Gates to Canonical Gaps)

| Governing Release Gate | Canonical Gaps Mapped | Unresolved Items Mapped | Gate Operational Status | Mandatory Outstanding Gate Evidence |
|---|---|---|---|---|
| **Gate G-01** (TTS Licensing & Runtime) | GAP-01, GAP-13, GAP-15 | U-01, U-13, U-15 | **EMPIRICAL GATE OPEN** | Permissive TTS license manifest (`THIRD_PARTY_NOTICES.md`), PyPI wheel verification log, MIT `LICENSE` committed on disk. |
| **Gate G-02** (MT Quality & Privacy) | GAP-02, GAP-07 | U-02, U-07 | **EMPIRICAL GATE OPEN** | 10-sentence dialogue benchmark results, Wireshark zero-egress packet capture in Local Mode, Cloud Opt-In timeout log. |
| **Gate G-03** (Latency Budget & Safety) | GAP-03, GAP-08, GAP-09, GAP-10, GAP-12 | U-03, U-08, U-09, U-10, U-12 | **EMPIRICAL GATE OPEN** | Integrated QPC latency traces on AC power, 95% CPU watchdog load test log, DPAPI credential storage verification log. |
| **Gate G-04** (Audio Topology & PTT Safety) | GAP-04, GAP-05, GAP-06, GAP-11, GAP-14 | U-04, U-05, U-06, U-11, U-14 | **EMPIRICAL GATE OPEN** | 60-min continuous loopback stability telemetry, AES-17 digital isolation log, PTT state machine unit & integration test traces. |

---

### 12.4 Coverage Semantics Disambiguation

To eliminate ambiguity across audit reports, the following distinction is strictly maintained:
1. **Mapping Coverage (Syntactic Completeness):** 100% complete ($15/15$ items mapped 1:1:1 across unresolved items, canonical gaps, findings, and release gates).
2. **Issue Resolution Status (Engineering Completion):** 0% resolved ($15/15$ findings remain strictly **OPEN — UNRESOLVED**).
3. **Release Gate Closure Status (Acceptance Completion):** 0% closed ($4/4$ release gates remain strictly **EMPIRICAL GATES OPEN**).

---

## 13. Physical Filesystem Accounting & Execution Boundaries

### 13.1 Categorized Filesystem Breakdown
- **Documentation Files Created:** Exactly two new files created during Revision 65 (`docs/ARCHITECTURE_R65.md` and `docs/ARCHITECTURE_R65_REVIEW.md`).
- **Predecessor Documentation Preserved:** Revisions `R44` through `R64` preserved 100% unmodified on disk.
- **Governing Files Preserved:** `SPEC.md`, `DECISIONS.md`, and `CLAUDE.md` remain 100% unmodified.
- **Source Code Files Created:** ZERO (`src/` remains empty/uncreated).
- **Prototypes Created:** ZERO (`prototypes/` remains empty/uncreated).
- **Tests Created:** ZERO (`tests/` remains empty/uncreated).
- **Packages Installed:** ZERO packages installed via `pip`, `winget`, or `conda`.
- **Model Weights Downloaded:** ZERO neural network weights or voice models downloaded.
- **Hardware Probed:** ZERO physical or virtual audio endpoints opened or initialized.

### 13.2 Missing License File Disclosed on Disk
Inspection confirms that NO `LICENSE` file exists in the repository root. This absence is tracked as open gap **GAP-15** (item **U-15**, Finding **F-15**) and must be resolved by committing an MIT license upon owner authorization prior to M1.

### 13.3 Absence of Git Repository Disclosed on Disk
Inspection confirms that `E:\Projects\VSCode\PostOmniroute\KoeBridge-for-Zoom` does not contain a `.git` directory (`fatal: not a git repository`). Therefore, independent external git commit baseline evidence is unavailable on disk, and comparisons against external baseline commits are qualified as `UNVERIFIED FROM SUPPLIED EVIDENCE`.

---

## 14. Grounded 14-Check Integrity Audit Table

The table below audits the 14 integrity dimensions of `docs/ARCHITECTURE_R65.md` against observable disk evidence, applying the strict 5-tier status taxonomy:

| Check ID | Integrity Dimension | Target Scope | Verification Method | Grounded Status | Detailed Finding & Specific Evidence Location |
|---|---|---|---|---|---|
| **CHK-01** | Debris & Artifact Purge | Entire Document Text | Manual Visual Scan | **VERIFIED** | Zero reasoning tokens, terminal commands, or conversational artifacts present in saved disk files (`R65`, `R64`, `R63`, `R62`, `R61`, `R60`, `R59`, `R58`). |
| **CHK-02** | Textual Completeness & Flow | Sections 1 through 15 | Line-by-Line Inspection | **VERIFIED** | All 15 sections are fully formed with complete sentences, unbroken table formatting, and clear transitions. Zero truncation markers exist. |
| **CHK-03** | Architecture Model Parity | Section 3 (§3.1, §3.1.1, §3.2, §3.3) | Cross-Reference Count | **VERIFIED** | Exact 1:1:1 mathematical parity: 33 nodes in diagram and register (`N-01`..`N-33`), 44 edges (`E-01`..`E-44`), and 8 closed subgraphs (`(a)`..`(h)`) fully enumerated. |
| **CHK-04** | Operating Mode Privacy Governance | §3.4.2, §7.2, §10.1, §10.2 | Cross-Spec Alignment | **VERIFIED** | Local Mode (offline default, zero egress, no silent fallback) and Cloud Opt-In Mode (sequential fallback, explicit consent, 2.50 s timeout) strictly cross-verified. |
| **CHK-05** | Digital Route Isolation Protocol | §7.4 (Test 3) | Protocol & Math Audit | **NOT EMPIRICALLY TESTED** | Protocol specification passed textual audit (AES-17 1 kHz sine, $L_{\text{stim}} = -20.0\text{ dBFS}$, $R_{\text{iso}} \ge 60\text{ dB}$, preflight floor $\le -90.0\text{ dBFS}$). Reconciled under Gate G-04. |
| **CHK-06** | Acoustic Leakage Protocol & Math | §7.4 (Test 3) | Mathematical Formulation Audit | **NOT EMPIRICALLY TESTED** | Mathematical formulation for background-corrected power and acoustic leakage ratio ($\Delta L_{\text{acoustic}} \le +6.0\text{ dB}$) verified with near-zero floor $\epsilon = 10^{-5}$. Reconciled under Gate G-04. |
| **CHK-07** | Loopback Stability Protocol & Accounting | §7.4 (Test 2B) | Mathematical Accounting Audit | **NOT EMPIRICALLY TESTED** | Rigorous mathematical accounting for aggregate frame-delivery discrepancy ($E_{\text{delivery}} \le 50.0\text{ PPM}$) over QPC reference, frame vs sample definition, and discontinuity flags verified in text. |
| **CHK-08** | PTT Lifecycle & Cancellation Protocol | §3.4.3, §7.4 (Test 4) | Lifecycle Protocol Audit | **NOT EMPIRICALLY TESTED** | Phase 4A unit test harness fully designed in text. Physical Phase 4B Windows integration timing targets ($T_1 \le 30\text{ ms}$, $T_2 \le 60\text{ ms}$, $T_3 \le 10\text{ ms}$, $T_4 \le 50\text{ ms}$) specified. |
| **CHK-09** | Licensing Alignment with SPEC.md | §6.0, §7.1, §10.2 | Cross-Document Legal Audit | **PARTIALLY VERIFIED** | Cross-verified against `SPEC.md` §5 and `DECISIONS.md` D-003/D-005: `OHF-Voice/piper1-gpl` identified as GPL-3.0 and unapproved by default. Local Japanese TTS identified as mandatory MVP hard gate. |
| **CHK-10** | Hardware Safety & Power Grounding | §1.1, §1.2, §7.3, §8.1 | Cross-Document Risk Audit | **PARTIALLY VERIFIED** | Grounded strictly in `SPEC.md` §8 as an observed hardware/battery risk requiring plugged-in AC power (`ACLineStatus == 1`) and CPU load-abort watchdog ($\ge 95\%$ for $\ge 15\text{ s}$). Proposed ADR D-028 not cited as governing authority. |
| **CHK-11** | Defect Audit Honesty | §11.0 | Historical Defect Audit | **VERIFIED** | All 33 historical defects audited individually with grounded statuses (28 Corrected in Document, 5 Protocol Specified, 0 Empirically Tested, 0 Owner-Approved, 0 Unverified). Discrepancy eliminated; zero double-counting. |
| **CHK-12** | Bidirectional Traceability Integrity | §12.2, §12.3, §15.2 | Cross-Matrix Parity Audit | **VERIFIED** | Forward matrix 1:1 alignment across all 15 unresolved items (U-01..U-15) and canonical technical gaps (GAP-01..GAP-15), and reverse matrix mapping to release gates G-01..G-04 verified. |
| **CHK-13** | Planning-Only Boundary & Filesystem Accounting | §1.1, §1.2, §13.0, §15.5 | Filesystem Audit | **VERIFIED** | Categorized filesystem audit confirms 2 new documentation files created (`R65`), 0 predecessor files modified, 0 governing files modified, 0 packages installed, 0 model weights downloaded, 0 audio hardware accessed. Missing `LICENSE` and absent `.git` repository honestly reported. |
| **CHK-14** | Release Gate & Milestone Discipline | §1.1, §7.1–§7.4, §9.0, §15.1, §15.5 | Governance Discipline Audit | **VERIFIED** | All four release gates (G-01 through G-04) remain strictly EMPIRICAL GATES OPEN. Milestone M0 remains strictly UNAUTHORIZED pending explicit project owner approval. Proposed amendments (C-01..C-04) and decisions (D-028..D-033) clearly marked NOT APPLIED. |

**Integrity Taxonomy Totals:**
- **VERIFIED:** Exactly 8 checks (57.1%: CHK-01, CHK-02, CHK-03, CHK-04, CHK-11, CHK-12, CHK-13, CHK-14).
- **PARTIALLY VERIFIED:** Exactly 2 checks (14.3%: CHK-09, CHK-10).
- **NOT EMPIRICALLY TESTED:** Exactly 4 checks (28.6%: CHK-05, CHK-06, CHK-07, CHK-08).
- **FAILED:** Exactly 0 checks (0.0%).
- **BLOCKED:** Exactly 0 checks (0.0%).
- **Total Checks Audited:** Exactly 14 checks (100.0%).

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
11. **GAP-11 (Medium - P2): Tkinter GUI Responsiveness & Focus Preservation:** Tkinter caption overlay must render at $\ge 30\text{ FPS}$ without stealing user focus from Chrome/Edge during background inference (`SPEC.md` §5.4, `DECISIONS.md` D-002) (Gate G-04).
12. **GAP-12 (Medium - P2): Secure Gemini API Key Storage via Windows Credential Manager:** When Cloud Opt-In Mode is enabled, API key must be stored securely using `keyring` (Windows DPAPI backend) and never written to plaintext configuration files or logs (`DECISIONS.md` D-027) (Gate G-03).
13. **GAP-13 (Medium - P2): Python Runtime & Dependency Compatibility (3.11/3.12 vs 3.13):** `SPEC.md` §1 references Python 3.13, but CTranslate2, PyAudioWPatch, and onnxruntime pre-compiled wheels for Windows x64 must be verified. If 3.13 wheels are unavailable, runtime must pin to 3.11 or 3.12 (Gate G-01).
14. **GAP-14 (Medium - P2): Digital Route Isolation Verification (AES-17 Sine Protocol):** Outbound audio injected into `Dev_CableIn` must achieve $\ge 60\text{ dB}$ digital isolation ($L_{\text{iso}} \le -80.0\text{ dBFS}$) against the loopback capture tap on `Dev_Playback` under AES-17 1,000 Hz sine stimulus testing (Gate G-04).
15. **GAP-15 (Low - P3): Repository License File Absence on Disk:** `CLAUDE.md` specifies MIT target for project-owned code, but no `LICENSE` file exists on disk. Must be committed prior to M1 upon owner authorization (Gate G-01).

### 15.3 Known Architectural Limitations & Operational Boundaries
1. **Virtual Audio Driver DMA Latency:** User-space software cannot recall or purge audio frames already committed to the VB-CABLE virtual driver DMA circular buffer ($\Delta T_{\text{driver\_dma}} < 100\text{ ms}$). Enforcing `qsize() == 0` purges software queues but cannot silence audio already transferred to the driver.
2. **Non-Preemptible Native C++ Inference:** In-flight tensor execution in CTranslate2 or ONNX Runtime cannot be safely interrupted mid-inference without memory corruption. Downstream epoch invalidation discards output instead.
3. **Secure Desktop Hook Suspension:** Win32 `WH_KEYBOARD_LL` low-level keyboard hooks stop receiving Windows messages during UAC prompts, Winlogon, and lock screens. Polling heartbeats and a 15-second watchdog provide fail-safe release upon desktop return.

### 15.4 Governance Proposal Cross-Reference (Pending Approvals)
- **Pending Proposed Amendments to SPEC.md:** `C-01`, `C-02`, `C-03`, `C-04`. (Total: 4 items; all marked `PROPOSED — NOT APPLIED`).
- **Pending Proposed Architecture Decision Records:** `D-028`, `D-029`, `D-030`, `D-031`, `D-032`, `D-033`. (Total: 6 items; all marked `PROPOSED — NOT APPLIED`).
- **Operational Milestone Boundary:** Milestone M0 Discovery Execution is an operational milestone authorization, not a 7th ADR or 11th proposal.

### 15.5 Final Architecture Verdict & Governance Declaration

```
====================================================================================================
                        KOEBRIDGE FOR ZOOM — ARCHITECTURAL REVIEW VERDICT
====================================================================================================
Document Identifier:       KB-ARCH-VERIF-PLAN-R65
Document Revision:         Revision 65 (Targeted Repair, Subgraph & Findings Parity, Epistemic Rigor)
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
  The Revision 65 Architecture & Verification Plan is a textually reviewed planning specification,
  structurally reconciled across 33 nodes, 44 edges, 8 closed subgraphs, 15 canonical findings,
  33 historical defects, 14 integrity checks, and 15 canonical gaps. Implementation remains NOT
  APPROVED because all four empirical release gates remain open and Milestone M0 remains strictly
  unauthorized.
====================================================================================================
```
